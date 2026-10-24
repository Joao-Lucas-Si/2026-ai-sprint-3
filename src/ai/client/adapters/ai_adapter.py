from abc import ABC, abstractmethod
import os
from typing import Callable, Literal, Optional

from src.dados import Mensagem

system_prompts = Literal["system_prompt", "analise_pergunta", "relatorio"]

class AiAdapter(ABC):

    def __init__(self, model: str) -> None:
        super().__init__()
        self.model = model

    @property
    def base_system_prompt(self):
        return open("assets/prompts/v2/base.md").read()
        
    def obter_system_prompt_params(self, system: system_prompts) -> dict:
        versao_atual = 2

        params = ["identidade", "persona", "objetivo", "regras", "extra"]

        result = {}

        for param in params:
            path = f"assets/prompts/v{versao_atual}/{system}/{param}.md"
            if os.path.exists(path):
                result[param] = open(path).read()
            else:
                result[param] = ""
        return result


    @abstractmethod
    def chamarDiretamente(self, prompt: str,historico: list[Mensagem] = [],  system: system_prompts="system_prompt",  formato: Optional[dict] = None, dados: dict = {}, *, mensagem_direta: str, usar_context: bool = False) -> str:
        pass
    
    

    # @abstractmethod
    # def chamarStream(self, observador: Callable[[str], None], prompt: str, historico: list[Mensagem] = [], system: system_prompts="assets/prompts/system_prompt.md") -> str:
    #     pass
    
    