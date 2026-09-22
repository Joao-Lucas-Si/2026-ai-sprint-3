from abc import ABC, abstractmethod
from typing import Callable, Literal, Optional

from src.dados import Mensagem

system_prompts = Literal["assets/prompts/v1/system_prompt.md", "assets/prompts/v1/analise_pergunta.md", "assets/prompts/v1/relatorio.md"]

class AiAdapter(ABC):

    def __init__(self, model: str) -> None:
        super().__init__()
        self.model = model

    @abstractmethod
    def chamarDiretamente(self, prompt: str,historico: list[Mensagem] = [],  system: system_prompts="assets/prompts/v1/system_prompt.md",  formato: Optional[dict] = None, dados: dict = {}) -> str:
        pass
    
    

    # @abstractmethod
    # def chamarStream(self, observador: Callable[[str], None], prompt: str, historico: list[Mensagem] = [], system: system_prompts="assets/prompts/system_prompt.md") -> str:
    #     pass
    
    