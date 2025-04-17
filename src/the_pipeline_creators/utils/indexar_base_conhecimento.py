# indexar_base_conhecimento.py
import os
import shutil
from crewai_tools import RagTool

print("--- INICIANDO SCRIPT DE INDEXAÇÃO DA BASE DE CONHECIMENTO ---")

# --- Configurações ---
KNOWLEDGE_DIR = "./knowledge/pandas_in_action"  # Diretório com os PDFs
PERSISTENT_DB_PATH = "./db" # Escolha um nome claro para o diretório do índice
COLLECTION_NAME = "pandas_in_action_book_v1"      # Nome para a coleção no ChromaDB (ajuda a organizar)
EMBEDDING_MODEL = "nomic-embed-text"           # Modelo de embedding (Ollama)
OLLAMA_BASE_URL = "http://localhost:11434"
# Opcional: LLM para uso interno do RagTool (pode usar um menor se não for para sumarizar)
# rag_llm = ChatOllama(model="llama3:8b", base_url=OLLAMA_BASE_URL) # Ex: modelo menor

# --- Controle de Reindexação ---
# !! CUIDADO !! Mude para True APENAS se quiser apagar o índice antigo e recriar tudo.
FORCE_REINDEX = True
# !! CUIDADO !!

if __name__ == "__main__":

    if not os.path.exists(KNOWLEDGE_DIR):
        print(f"[ERRO] Diretório da base de conhecimento não encontrado: {KNOWLEDGE_DIR}")
        exit(1)

    if FORCE_REINDEX and os.path.exists(PERSISTENT_DB_PATH):
        print(f"[AVISO] FORCE_REINDEX=True. Apagando índice existente em: {PERSISTENT_DB_PATH}")
        try:
            shutil.rmtree(PERSISTENT_DB_PATH)
            print("[INFO] Índice antigo apagado com sucesso.")
        except OSError as e:
            print(f"[ERRO] Não foi possível apagar o diretório do índice antigo: {e}")
            exit(1)

    if os.path.exists(PERSISTENT_DB_PATH) and not FORCE_REINDEX:
        print(f"[INFO] Índice já existe em: {PERSISTENT_DB_PATH}")
        print("[INFO] Para forçar a reindexação (ex: após atualizar PDFs), execute com FORCE_REINDEX = True.")
        print("--- Script de Indexação Concluído (Nenhuma Ação Necessária) ---")
        exit(0)

    print(f"[INFO] Criando ou atualizando índice em: {PERSISTENT_DB_PATH}")
    print(f"[INFO] Lendo arquivos de: {KNOWLEDGE_DIR}")
    print(f"[INFO] Usando modelo de embedding: {EMBEDDING_MODEL}")

    try:
        # Inicializa o RagTool para indexar, especificando onde salvar (persist_directory)
        # e a fonte dos dados (data_source)
        pandas_knowledge_indexer = RagTool(
            persist_directory=PERSISTENT_DB_PATH,
            collection_name=COLLECTION_NAME,
            data_source=KNOWLEDGE_DIR, # Fonte dos dados a serem indexados
            data_type="directory",     # Indica que a fonte é um diretório
            config={
                'embedder': {
                    'provider': 'ollama',
                    'config': {
                        'model': EMBEDDING_MODEL,
                        'base_url': OLLAMA_BASE_URL
                    }
                },
                # O LLM pode ser necessário internamente pelo EmbedChain/RagTool
                'llm': {
                    'provider': 'ollama',
                    'config': {
                        'model': 'qwen2.5:14b', # Ou use um modelo menor como 'llama3:8b'
                        'base_url': OLLAMA_BASE_URL
                    }
                },
            }
        )
        # A própria inicialização com 'data_source' e 'persist_directory' deve
        # realizar a leitura, chunking, embedding e salvamento no ChromaDB.

        print("-" * 50)
        print(f"[SUCESSO] Indexação concluída!")
        print(f"[INFO] Banco de dados vetorial salvo em: {PERSISTENT_DB_PATH}")
        print("-" * 50)

    except Exception as e:
        print(f"[ERRO FATAL] Ocorreu um erro durante a indexação: {e}")
        # Considerar remover o diretório parcialmente criado em caso de erro
        # if os.path.exists(PERSISTENT_DB_PATH):
        #     print(f"[INFO] Removendo diretório de índice potencialmente corrompido...")
        #     shutil.rmtree(PERSISTENT_DB_PATH)

    print("--- Script de Indexação Finalizado ---")