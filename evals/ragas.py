import os
from typing import cast

from datasets import Dataset
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama, OllamaEmbeddings
from ragas import evaluate
from ragas.dataset_schema import EvaluationResult
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.llms import LangchainLLMWrapper
from ragas.metrics import faithfulness, answer_relevancy
from src.rag.embeddings import embed
from src.rag.retriever import rag_indexar
from src.ai.engine.ai_engine import AiEngine


def avaliar():
    retriever = rag_indexar()
    # Configurar o RAGAS para usar o Ollama (sem custo)
    print("avaliando")
    ragas_llm = LangchainLLMWrapper(
        ChatGoogleGenerativeAI(
            model="gemini-3.1-flash-lite",
            api_key=os.getenv("CHAVE_GEMINI"),
        )
    )
    ragas_embs = LangchainEmbeddingsWrapper(embed())
    faithfulness.llm = ragas_llm
    answer_relevancy.llm = ragas_llm
    answer_relevancy.embeddings = ragas_embs

    perguntas = [
        "quais são os passos para encerrar uma sessão",
        "o que a tarifa pode incluir?",
        "o carregador esta disponivel, mas classificado como ocupado",
        "minha pré reserva não foi confirmada",
        "minha sessão foi interrompida",
        # "quais os Tipos textuais segundo Werlich (1973)? cite a página",
        # "qual o conteudo em 1.Gêneros textuais como práticas sócio-históricas",
        # "o que há em 2. Novos gêneros e velhas bases",
        # "quais as observações em 4. Algumas observações sobre os tipos textuais",
        # "faça um resumo de 7. Observações finais "
    ]
    contextos = [
        "Como encerrar uma sessão",
        "Como interpretar o preço",
        "Carregador disponível, mas ocupado",
        "A pré-reserva não foi confirmada",
        "A sessão foi interrompida inesperadamente",
    ]
    try:
        engine = AiEngine()
        print("respondendo")

        def responder(j, i):
            print(i)
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
        print(resultado.to_pandas())
    except Exception as e:
        print(e)
