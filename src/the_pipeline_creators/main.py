#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

# Ajuste o caminho conforme sua estrutura
from the_pipeline_creators.crew import PipelineCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Executa a crew para projetar e implementar o pipeline de engenharia de dados.
    """
    inputs = {
        'finalidade_do_pipeline': (
            "Você deve implementar um pipeline de engenharia de dados padrão para tratar e validar dados de clientes brasileiros contidos em um arquivo CSV chamado `clientes_bruto.csv`. "
            "O pipeline deve ser implementado com as bibliotecas Pandas (transformações), Pydantic (validação) e Pytest (testes). "
            "Além disso, um script de testes com Pytest deve ser criado para validar as transformações e regras do pipeline. "
            "O pipeline deve incluir as seguintes etapas obrigatórias:\n\n"
            "1. **Leitura dos dados**: carregar os dados do arquivo `clientes_bruto.csv`.\n"
            "2. **Padronização dos nomes de colunas**: transformar os nomes para minúsculas e formato `snake_case`.\n"
            "3. **Correção dos tipos de dados**: converter colunas como datas para `datetime` e valores monetários para `float`.\n"
            "4. **Tratamento de valores ausentes**: preencher valores nulos; use 0 ou média para colunas numéricas e 'Desconhecido' para categóricas.\n"
            "5. **Remoção de duplicatas**: eliminar registros duplicados com base na chave primária `id_cliente`.\n"
            "6. **Validação de dados**: aplicar regras como idade > 0, email com formato válido, UF presente na lista oficial de estados brasileiros.\n"
            "7. **Registro de falhas de validação**: salvar linhas inválidas no arquivo `outputs/clientes_invalidos.csv`.\n"
            "8. **Exportação dos dados validados**: salvar os dados finais no arquivo `outputs/clientes_processados.parquet`, prontos para análise de negócio.\n\n"
            "Certifique-se de que todo o pipeline seja modular e testável. "
            "Utilize logs e mensagens claras para identificar falhas durante a execução. "
            "Gere também o script de testes `test_pipeline.py`, cobrindo os principais pontos do pipeline com Pytest."
        ),
        "csv_path": "inputs/raw/ETL_Agreement.csv"
    }


    try:
        print("Iniciando a execução da Crew para o pipeline de engenharia de dados...")
        PipelineCrew().crew().kickoff(inputs=inputs)
        print("\nExecução da Crew concluída. Verifique os arquivos de saída gerados (design, código, etc.).")
    except Exception as e:
        import traceback
        print(f"Ocorreu um erro ao executar a crew: {e}")
        print(traceback.format_exc())

def train():
    """
    Treina a crew por um número de iterações.
    Nota: O treinamento eficaz requer um arquivo com dados de entrada e saídas esperadas.
    """
    inputs = {
        'finalidade_do_pipeline': 'Refinar pipeline de limpeza de clientes CSV para Parquet.', 
        'current_year': str(datetime.now().year)
    }
    if len(sys.argv) < 3:
        print("Uso: python main.py train <n_iterations> <filename>")
        sys.exit(1)
    n_iterations = int(sys.argv[1])
    filename = sys.argv[2]
    print(f"Iniciando treinamento por {n_iterations} iterações usando o arquivo '{filename}'...")
    try:
        PipelineCrew().crew().train(n_iterations=n_iterations, filename=filename, inputs=inputs)
        print("\nTreinamento concluído.")
    except Exception as e:
        import traceback
        print(f"Ocorreu um erro durante o treinamento da crew: {e}")
        print(traceback.format_exc())

def replay():
    """
    Reexecuta a crew a partir de uma task_id específica (útil para debug).
    """
    if len(sys.argv) < 2:
        print("Uso: python main.py replay <task_id>")
        sys.exit(1)
    task_id = sys.argv[1]
    print(f"Tentando reexecutar a partir da task_id: {task_id}")
    try:
        PipelineCrew().crew().replay(task_id=task_id)
        print("\nReplay concluído.")
    except Exception as e:
        import traceback
        print(f"Ocorreu um erro durante o replay da crew: {e}")
        print(traceback.format_exc())

def test():
    """
    Testa a execução da crew por N iterações e retorna os resultados.
    """
    inputs = {
        'finalidade_do_pipeline': 'Testar pipeline de limpeza de clientes CSV para Parquet.', 
        'current_year': str(datetime.now().year)
    }
    if len(sys.argv) < 3:
        print("Uso: python main.py test <n_iterations> [openai_model_name]")
        print("     [openai_model_name] é opcional e pode não ser usado se Ollama estiver configurado.")
        sys.exit(1)
    n_iterations = int(sys.argv[1])
    openai_model_name = sys.argv[2] if len(sys.argv) > 2 else "Não Especificado (usando LLM configurado)"
    print(f"Iniciando teste por {n_iterations} iterações...")
    if openai_model_name != "Não Especificado (usando LLM configurado)":
        print(f"Nota: O argumento 'openai_model_name' ({openai_model_name}) pode ser ignorado se Ollama estiver configurado na crew.")
    try:
        results = PipelineCrew().crew().test(n_iterations=n_iterations, openai_model_name=openai_model_name, inputs=inputs)
        print("\nTeste concluído. Resultados:")
        print(results) # Imprime os resultados do teste
    except Exception as e:
        import traceback
        print(f"Ocorreu um erro durante o teste da crew: {e}")
        print(traceback.format_exc())

COMMANDS = {
    "run": run,
    "train": train,
    "replay": replay,
    "test": test,
}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print("Uso: python main.py <comando> [argumentos...]")
        print("Comandos disponíveis: run, train, replay, test")
        sys.exit(1)

    command = sys.argv[1]
    original_argv = sys.argv.copy()
    sys.argv = sys.argv[1:]

    COMMANDS[command]()

    sys.argv = original_argv