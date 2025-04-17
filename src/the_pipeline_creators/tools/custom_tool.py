from pathlib import Path
from typing import Type
import logging
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

logger = logging.getLogger(__name__)


class CodeWriterToolInput(BaseModel):
    filename: str = Field(
        ...,
        description="Nome do arquivo com caminho relativo, ex: 'outputs/pipeline_dados.py'"
    )
    content: str = Field(
        ...,
        description="Conteúdo textual completo a ser escrito no arquivo."
    )


class CodeWriterTool(BaseTool):
    """
    Grava texto em disco durante a execução da Crew.
    Use para criar scripts, requirements.txt, README.md, etc.
    Sempre sobrescreve o arquivo destino (não faz append).
    """

    name: str = "Code Writer Tool"
    description: str = (
        "Escreve ou sobrescreve arquivos de texto (scripts Python, README, etc.). "
        "Recebe JSON {'filename': <str>, 'content': <str>}."
    )
    args_schema: Type[BaseModel] = CodeWriterToolInput

    def _run(self, filename: str, content: str) -> str:
        if not content.strip():
            raise ValueError("Conteúdo vazio não é permitido.")

        path = Path(filename)
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            # escrita atômica
            tmp_path = path.with_suffix(".tmp")
            tmp_path.write_text(content, encoding="utf-8")
            tmp_path.replace(path)

            logger.info("[CodeWriterTool] Arquivo salvo: %s", path)
            return f"Sucesso: Conteúdo escrito no arquivo '{path}'."
        except Exception as e:
            logger.error("Erro ao salvar '%s': %s", path, e)
            return f"Erro ao salvar '{path}': {e}"
