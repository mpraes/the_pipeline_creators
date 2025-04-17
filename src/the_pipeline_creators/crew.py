from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from the_pipeline_creators.tools.custom_tool import CodeWriterTool
from crewai_tools import RagTool
from langchain_ollama import ChatOllama
import os
from dotenv import load_dotenv
loaded = load_dotenv() # Guarde o resultado para verificar

# ---- DEBUG ----
print("-" * 20, "DEBUG ENV VARS", "-" * 20)
print(f".env carregado: {loaded}") # Deve imprimir True se encontrou o .env
print(f"LLM_MODEL lido: {os.getenv('LLM_MODEL')}")
print(f"OLLAMA_BASE_URL lido: {os.getenv('OLLAMA_BASE_URL')}")
print("-" * 50)
# ---- FIM DEBUG ----

# --- Configurações (lidas do .env) ---
LLM_MODEL = os.getenv("LLM_MODEL", "qwen2.5:14b") # Fornece um padrão opcional
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
PERSISTENT_DB_PATH = os.getenv("PERSISTENT_DB_PATH", "./db")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "pandas_action_book_v1")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")

# --- Inicialização do LLM ---
llm = ChatOllama(model=LLM_MODEL, base_url=OLLAMA_BASE_URL, temperature=0.2)

# --- Carregamento da Ferramenta RAG (APENAS CARREGAR) ---
print("[INFO] Configurando RAGTool para CARREGAR índice persistente...")

if not os.path.exists(PERSISTENT_DB_PATH):
    print(f"[ERRO FATAL] Diretório do índice RAG não encontrado: {PERSISTENT_DB_PATH}")
    print("[AÇÃO] Execute o script 'indexar_base_conhecimento.py' primeiro!")
    exit(1)


try:
    # Inicializa o RagTool APENAS para carregar o índice existente
    pandas_knowledge_tool = RagTool(
        persist_directory=PERSISTENT_DB_PATH,       # Indica DE ONDE carregar
        collection_name=COLLECTION_NAME,            # Indica QUAL coleção carregar
        # *** NÃO PASSE data_source ou data_type aqui ***
        config={
            'embedder': { # Precisa ser o mesmo usado na indexação para buscar corretamente
                'provider': 'ollama',
                'config': {
                    'model': EMBEDDING_MODEL,
                    'base_url': OLLAMA_BASE_URL
                }
            },
            'llm': {
                'provider': 'ollama',
                'config': {
                    'model': LLM_MODEL,
                    'base_url': OLLAMA_BASE_URL
                }
            },
        },
        # summarize=False # Mantenha se não quiser sumarização na busca
    )

    # Defina a descrição da ferramenta para os agentes
    pandas_knowledge_tool.description = ("Consulta informações específicas, melhores práticas, exemplos de código ou explicações sobre a biblioteca Pandas, buscando diretamente no conteúdo do livro 'Pandas in Action'. Use quando precisar de detalhes sobre funções, métodos ou conceitos avançados de Pandas.")

    print(f"[INFO] RAGTool carregada com sucesso do índice: {PERSISTENT_DB_PATH}")

except Exception as e:
    print(f"[ERRO FATAL] Falha ao carregar RAG tool do índice persistente: {e}")
    exit(1)

# 1. Instancie a ferramenta sem root_dir (ou implemente o parâmetro na classe)
code_writer = CodeWriterTool()              # <= fix

# ------------------------------------------------------------------------------
@CrewBase
class PipelineCrew():
    agents_config = "config/agents.yaml"
    tasks_config  = "config/tasks.yaml"
    
    # 2️⃣ registro global para o mapeador YAML → classe
    tools = [CodeWriterTool]

    # ---------------------------------------------------------------- agents --
    @agent
    def arquiteto(self) -> Agent:
        return Agent(
            config=self.agents_config['arquiteto'],
            verbose=True,
            llm=f"ollama/{llm.model}",
            allow_delegation=False,
            tools=[pandas_knowledge_tool]
        )

    @agent
    def engenheiro(self) -> Agent:
        return Agent(
            config=self.agents_config['engenheiro'],
            verbose=True,
            llm=f"ollama/{llm.model}",
            allow_delegation=False,
            tools=[code_writer, pandas_knowledge_tool]
        )

    @agent
    def tester(self) -> Agent:
        return Agent(
            config=self.agents_config['tester'],
            verbose=True,
            llm=f"ollama/{llm.model}",
            allow_delegation=False,
            tools=[code_writer, pandas_knowledge_tool]
        )

    @agent
    def revisor(self) -> Agent:
        return Agent(
            config=self.agents_config['revisor'],
            verbose=True,
            llm=f"ollama/{llm.model}",
            allow_delegation=False,
            tools=[code_writer, pandas_knowledge_tool]
        )

    # ---------------------------------------------------------------- tasks --
    @task
    def design_pipeline_task(self) -> Task:
        return Task(
            config=self.tasks_config['design_pipeline_task'],
            agent=self.arquiteto(),
            output_file="outputs/pipeline_design.md"
        )

    @task
    def implement_pipeline_task(self) -> Task:
        return Task(
            config=self.tasks_config['implement_pipeline_task'],
            agent=self.engenheiro(),
            context=[self.design_pipeline_task()],
            output_file="outputs/pipeline_dados.py"
        )

    @task
    def write_tests_task(self) -> Task:
        return Task(
            config=self.tasks_config['write_tests_task'],
            agent=self.tester(),
            context=[
                self.implement_pipeline_task(),
                self.design_pipeline_task()   # <= fix
            ],
            output_file="outputs/test_pipeline.py"
        )
    
    @task
    def review_code_task(self) -> Task:
        return Task(
            config=self.tasks_config['review_code_task'],
            agent=self.revisor(),
            context=[
                self.implement_pipeline_task(),
                self.design_pipeline_task(),   # <= fix
                self.write_tests_task()
            ],
            output_file="outputs/CODE_REVIEW.md"
        )

    # ---------------------------------------------------------------- crew --
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
