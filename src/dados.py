from enum import Enum
import random
from typing import Self

from pydantic import BaseModel, ConfigDict





def exemplos():
    global salvos
    if len(salvos) == 0:
        salvos = gerar_exemplos()
        
    return salvos
        
    

def gerar_exemplos():
    def gerar_carregadores():
        return [Carregador(capacidade=random.randint(10, 50), numero=random.randint(1, 100), disponivel=random.randint(200, 1000), ocupado=random.randint(0,10) > 7) for i in range(random.randint(1, 4))]
    posto1 = Posto()
    posto1.nome = "posto shopping tamboré"
    posto1.carregadores = gerar_carregadores()

    posto2 = Posto()
    posto2.nome = "posto do aeroporto"
    posto2.carregadores = gerar_carregadores()

    posto3 = Posto()
    posto3.nome = "posto ipiranga"
    posto3.carregadores = gerar_carregadores()

    posto4 = Posto()
    posto4.nome = "posto do villa lobos"
    posto4.carregadores = gerar_carregadores()
    
    return [posto1, posto2, posto3, posto4]

class Carregador(BaseModel):
    model_config = ConfigDict(use_attribute_docstrings=True)
    capacidade: int = 0
    """capacidade de carregamento por hora"""
    disponivel: int = 0
    """quantidade de energia disponivel"""
    ocupado: bool = False
    """estado de ocupação do carregador"""
    numero: int
    """número de identificação do carregador"""
    

class Posto(BaseModel):
    model_config = ConfigDict(use_attribute_docstrings=True)
    nome: str = ""
    
    carregadores: list[Carregador] = []


class Papel(Enum):
    USUARIO = "user"
    CHAT = "chat"


class Mensagem():
    conteudo: str
    role: Papel
    def __init__(self, conteudo: str, role: Papel = Papel.USUARIO) -> None:
        self.conteudo = conteudo
        self.role = role


class MensagemChat(Mensagem):
    pensamento: str

    def __init__(self, conteudo: str, pensamento: str = "") -> None:
        super().__init__(conteudo, Papel.CHAT)
        self.pensamento = pensamento


salvos: list[Posto] = []