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

from evals.ragas import avaliar_rag
from src.ai.engine.memory import contar_tokens
from src.ai.client.instancia import instanciarAi
from src.ai.engine.ai_engine import AiEngine



class CasoTeste(TypedDict):
    input: str
    contexto: str
    # palavras_chaves: list[str]

testes: list[CasoTeste] = [
    {
        "input": "quais são os passos para encerrar uma sessão",
        "contexto": "Como encerrar uma sessão",
    },
    {
        "input": "o que a tarifa pode incluir?",
        "contexto": "Como interpretar o preço",
    },
    {
        "input":"o que cada padrão de cor presente na luz do equipamento quer dizer?",
        "contexto": "As cores e os padrões luminosos",
    },
    {
        "input": "quais os sinais de um cabo danificado?",
        "contexto": "Cabo ou conector danificado",
    },
    {
        "input": "minha sessão foi interrompida",
        "contexto": "A sessão foi interrompida inesperadamente",
    }
]

class TesteResultado(TypedDict):
    # estado: TesteEstado
    resposta: str
    pergunta: str
    relevancia: float
    fidelidade: float
    contexto: str
    # tokens: float

class ModelResultados(TypedDict):
    resultado: list[TesteResultado]
    model: str

atual = 0

def testar(*, adicionar_resultado: Callable[[TesteResultado], None], mostrar_teste: Callable[[int, str], None], engine: AiEngine, ):
    global atual
   

    for i, teste in enumerate(testes):
        mostrar_teste(i, teste["input"])
        
        avaliado = avaliar_rag(teste["input"], teste["contexto"], engine)
        
        resultado: TesteResultado = {
            "pergunta": teste["input"],
            "relevancia": avaliado[0]["relevancia"],
            "fidelidade": avaliado[0]["fidelidade"],
            "contexto": avaliado[0]["contexto"],
            "resposta": avaliado[0]["resposta"]
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
                        resultado["relevancia"],
                        resultado["fidelidade"],
                        resultado["resposta"],
                    ]
                )
                
            data = pd.DataFrame(rows, columns=["pergunta", "relevancia", "fidelidade", "resposta"])
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
            models =  ["gemini-3.5-flash-lite", "gemini-3.1-flash-lite"] if  len(sys.argv) >= 2 and sys.argv[1] == "--comparativo" else  ["gemini-3.1-flash-lite"]
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

                tabela.add_columns("pergunta", "answer_relevancy", "faithfulness", "resposta")
                for resultado in model["resultado"]:
                    #resultado["resposta"]
                    linhas = self.quebraLinhas(resultado["resposta"])
                    tabela.add_row(
                        resultado["pergunta"],
                        resultado["relevancia"],
                        resultado["fidelidade"],
                        # resultado["estado"].value,
                        "\n".join(linhas),
                        height=len(linhas),
                    )
                yield tabela
        else:
            with Container(id="container-teste"):
                yield Label("aplicando os testes", )
