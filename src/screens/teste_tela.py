from asyncio import create_task, get_running_loop, run
from enum import Enum, EnumType
import re
from threading import Thread
from time import sleep
from typing import TypedDict
import pandas as pd
from textual.app import ComposeResult
from textual.containers import Container
from textual.events import Mount
from textual.messages import Layout
from textual.screen import Screen
from textual.widgets import DataTable, Header, Label

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


class TesteTela(Screen):
    CSS_PATH="../../assets/css/teste-styles.tcss"
    completo = False
    resultados: list[TesteResultado] = []

    def _on_mount(self, event: Mount) -> None:
        atual = 0
        engine = AiEngine()
        label = self.query_one(Label)

        def gerar_relatorio():
            rows = []
            
            for resultado in self.resultados:
                rows.append(
                    [
                        resultado["pergunta"],
                        resultado["acuracia"],
                        resultado["estado"].value,
                        resultado["resposta"],
                    ]
                )
                
            data = pd.DataFrame(rows, columns=["pergunta", "acuracia", "estado", "resposta"])
            data.to_csv("assets/relatorio.csv")

        def terminar():
            # sleep(2)
            self.completo = True
            self.refresh(recompose=True)
            gerar_relatorio()

        def adicionar_resultado(resultado: TesteResultado):
           
            self.resultados.append(resultado)
            
        def mostrar_teste():
            label.content = f"teste {atual + 1} em execução"
            label.refresh()

        async def testar():
            # sleep(10)
            nonlocal atual
            label.content = "testando"

            for i, teste in enumerate(testes):
                mostrar_teste()
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
                }
                adicionar_resultado(resultado)
                atual = i

            terminar()

        # loop =get_running_loop()
        # loop.create_task(testar())
        self.run_worker(testar(), start=True, thread=True)

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
            tabela = DataTable()

            tabela.add_columns("pergunta", "acuracia", "estado", "resposta")

            for resultado in self.resultados:
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
