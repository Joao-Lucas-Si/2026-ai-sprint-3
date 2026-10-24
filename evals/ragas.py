import os
from typing import cast

from datasets import Dataset
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama, OllamaEmbeddings
from ragas import RunConfig, evaluate
from ragas.dataset_schema import EvaluationResult
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.llms import LangchainLLMWrapper
from ragas.metrics import faithfulness, answer_relevancy
from src.ai.client.adapters.langchain_adapter import criar_model
from src.rag.embeddings import embed
from src.rag.retriever import rag_indexar
from src.ai.engine.ai_engine import AiEngine


def avaliar(model = "gemini-3.1-flash-lite"):
    retriever = rag_indexar()
    # Configurar o RAGAS para usar o Ollama (sem custo)
    print("avaliando")
    ragas_llm = LangchainLLMWrapper(ChatOllama(model="gemma4:cloud", base_url="https://ollama.com", temperature=0))
    ragas_embs = LangchainEmbeddingsWrapper(embed())
    faithfulness.llm = ragas_llm
    answer_relevancy.llm = ragas_llm
    answer_relevancy.embeddings = ragas_embs

    perguntas = [
        "quais são os passos para encerrar uma sessão",
        "o que a tarifa pode incluir?",
        "o carregador esta disponivel, mas classificado como ocupado",
        "quais os sinais de um cabo danificado?",
        "minha sessão foi interrompida",
    ]
    contextos = [
        "Como encerrar uma sessão",
        "Como interpretar o preço",
        "Carregador disponível, mas ocupado",
        "Cabo ou conector danificado",
        "A sessão foi interrompida inesperadamente",
    ]
    try:
        engine = AiEngine(model)
        print("respondendo")

        def responder(j, i):
            print(f"executando teste - {i + 1}")
            return engine.responder(j)

        dados_avaliacao = {
            "question": [*perguntas],
            "answer": [responder(i, j) for j, i in enumerate(perguntas)],
            "contexts": [
                [d.page_content for d in retriever.invoke(c)] for c in contextos
            ],
        }
        print("respondidos")
        resultado = cast(
            EvaluationResult,
            evaluate(
                Dataset.from_dict(dados_avaliacao),
                metrics=[faithfulness, answer_relevancy],
                run_config=RunConfig(timeout=2000 * 20)
                # embeddings= ragas_embs,
                # llm=ChatGoogleGenerativeAI(
                #     model="gemini-3.1-flash-lite",
                #     api_key=os.getenv("CHAVE_GEMINI"),
                # )
                # llm=ChatOllama(
                #     model="gemma4:cloud",
                #     base_url="https://ollama.com",
                #     num_predict=250,
                #     temperature=0,
                # ),
            ),
        )
        selecionados = resultado.to_pandas()[["user_input", "answer_relevancy", "faithfulness"]]
        selecionados.rename(mapper={
            "user_input": "pergunta",
            "answer_relevancy": "relevancia",
            "faithfulness": "fidelidade"
        })
        print(selecionados)
    except Exception as e:
        print(e)
