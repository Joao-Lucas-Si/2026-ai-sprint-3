from asyncio import create_task, get_running_loop, run
from enum import Enum, EnumType
import re
import sys
from threading import Thread
from time import sleep
from typing import Callable, TypedDict
import pandas as pd
from textual.app import ComposeResult
from textual.containers import Container
from textual.events import Mount
from textual.messages import Layout
from textual.screen import Screen
from textual.widgets import DataTable, Header, Label

from src.ai.engine.memory import contar_tokens
from src.ai.client.instancia import instanciarAi
from src.ai.engine.ai_engine import AiEngine


class CasoTeste(TypedDict):
    input: str
    palavras_chaves: list[str]


testes: list[CasoTeste] = [
    {
        "input": "Quais carregadores estão disponíveis neste momento?",
        "palavras_chaves": ["disponivel", "carregador", "posto", "ocupado"],
    },
    {
        "input": "Minha recarga foi interrompida, o que aconteceu?",
        "palavras_chaves": [
            "recarga",
            "limite",
            "desconexão",
            "verifique",
            "suporte técnico",
        ],
    },
    {
        "input": "Como iniciar uma sessão de carregamento?",
        "palavras_chaves": ["iniciar", "conecte", "cabo", "recarga", "carregador"],
    },
    {
        "input": "Meu pagamento foi feito mas o carregador não funciona?",
        "palavras_chaves": [
            "pagamento",
            "verifique",
            "conectado",
            "problema",
            "suporte técnico",
        ],
    },
    {
        "input": "O carregador não reconheceu meu veículo, o que eu faço?",
        "palavras_chaves": [
            "compatibilidade",
            "verifique",
            "problema",
            "suporte técnico",
        ],
    },
]


class TesteEstado(Enum):
    ADEQUADA = "adequada"
    PARCIAL = "parcialmente adequada"
    INADEQUADA = "inadequada"


class TesteResultado(TypedDict):
    estado: TesteEstado
    resposta: str
    pergunta: str
    acuracia: float
    # tokens: float

class ModelResultados(TypedDict):
    resultado: list[TesteResultado]
    model: str

atual = 0

def testar(*, adicionar_resultado: Callable[[TesteResultado], None], mostrar_teste: Callable[[int, str], None], engine: AiEngine, ):
    global atual
   

    for i, teste in enumerate(testes):
        mostrar_teste(i, teste["input"])
        resposta = engine.responder(teste["input"])
        acuracia = 0

        for palavra in teste["palavras_chaves"]:
            if palavra in resposta:
                acuracia += 1

        acuracia = acuracia / len(teste["palavras_chaves"])
        estado: TesteEstado
        if acuracia >= 0.7:
            estado = TesteEstado.ADEQUADA
        elif acuracia >= 0.4:
            estado = TesteEstado.PARCIAL
        else:
            estado = TesteEstado.INADEQUADA

        resultado: TesteResultado = {
            "pergunta": teste["input"],
            "resposta": resposta,
            "acuracia": acuracia,
            "estado": estado,
            # "tokens": contar_tokens(resposta)
        }
        adicionar_resultado(resultado)
        atual = i

class TesteTela(Screen):
    CSS_PATH="../../assets/css/teste-styles.tcss"
    completo = False
    resultados: list[ModelResultados] = []

    def _on_mount(self, event: Mount) -> None:
        atual = 0
        engine = AiEngine()
        label = self.query_one(Label)

        def gerar_relatorio(i: int):
            rows = []
            
            for resultado in self.resultados[i]["resultado"]:
                rows.append(
                    [
                        resultado["pergunta"],
                        resultado["acuracia"],
                        resultado["estado"].value,
                        resultado["resposta"],
                    ]
                )
                
            data = pd.DataFrame(rows, columns=["pergunta", "acuracia", "estado", "resposta"])
            data.to_csv(f"assets/relatorio-{self.resultados[i]["model"]}.csv")

        def terminar():
            # sleep(2)
            self.completo = True
            self.refresh(recompose=True)

            gerar_relatorio(0)

        def adicionar_resultado(resultado: ModelResultados):
           
            self.resultados.append(resultado)
            
        async def testarModels():
            # sleep(10)
            # label.content = "testando"
            models =  ["gemini-3.5-flash-lite", "gemini-3.1-flash-lite"] if  len(sys.argv) >= 3 and sys.argv[2] == "comparativo" else  ["gemini-3.5-flash-lite"]
            resultados: list[ModelResultados]  = []
            for i in range(len(models)):
                modelResultado: ModelResultados = {
                    "model": models[i],
                    "resultado": []
                }
                def nomearTeste(j: int, teste: str):
                    label.content = f"modelo {models[i]} respondendo {j + 1}º teste(\"{teste}\")"

                testar(adicionar_resultado=lambda resultado: modelResultado["resultado"].append(resultado), engine=AiEngine(models[i]), mostrar_teste=nomearTeste)
                adicionar_resultado(modelResultado)
                gerar_relatorio(i)
            terminar()

        # loop =get_running_loop()
        # loop.create_task(testar())
        self.run_worker(testarModels(), start=True, thread=True)

    def quebraLinhas(self, texto: str) -> list[str]:
        linhas = [""]
        palavras = texto.replace("\n", "").split(" ")
        largura = 100
        for palavra in palavras:
            if len(linhas[-1]) + len(palavra) > largura:
                linhas.append(palavra)
            else:
                linhas[-1] += " " + palavra
        return linhas

    def compose(self) -> ComposeResult:
        yield Header()

        if self.completo:
            for model in self.resultados:
                yield Label(model["model"], )
                tabela = DataTable()

                tabela.add_columns("pergunta", "acuracia", "estado", "resposta")
                for resultado in model["resultado"]:
                    linhas = self.quebraLinhas(resultado["resposta"])
                    tabela.add_row(
                        resultado["pergunta"],
                        resultado["acuracia"],
                        resultado["estado"].value,
                        "\n".join(linhas),
                        height=len(linhas),
                    )
                yield tabela
        else:
            with Container(id="container-teste"):
                yield Label("aplicando os testes", )
