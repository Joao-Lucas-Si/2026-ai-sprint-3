
def avaliar():
    # Configurar o RAGAS para usar o Ollama (sem custo)
    print("avaliando")
    ragas_llm = LangchainLLMWrapper(ChatOllama(model="gemma4:cloud", temperature=0))
    ragas_embs = LangchainEmbeddingsWrapper(OllamaEmbeddings(model="nomic-embed-text"))
    faithfulness.llm = ragas_llm
    answer_relevancy.llm = ragas_llm
    answer_relevancy.embeddings = ragas_embs
    
    perguntas = [
        # "quais os Tipos textuais segundo Werlich (1973)? cite a página",
        # "qual o conteudo em 1.Gêneros textuais como práticas sócio-históricas",
        # "o que há em 2. Novos gêneros e velhas bases",
        # "quais as observações em 4. Algumas observações sobre os tipos textuais",
        # "faça um resumo de 7. Observações finais "
    ]
    dados_avaliacao = {
        "question": [*perguntas],
        "answer": [main_pipeline(i) for i in perguntas],
        "contexts": [
            # [d.page_content for d in retriever.invoke("Tipos textuais segundo Werlich (1973)")],
            # [d.page_content for d in retriever.invoke("1.Gêneros textuais como práticas sócio-históricas")],
            # [d.page_content for d in retriever.invoke("o que há em 2. Novos gêneros e velhas bases?")],
            # [d.page_content for d in retriever.invoke("4. Algumas observações sobre os tipos textuais")],
            # [d.page_content for d in retriever.invoke("7. Observações finais")],
        ],
    }
    resultado = cast(
        EvaluationResult,
        evaluate(
            Dataset.from_dict(dados_avaliacao),
            metrics=[faithfulness, answer_relevancy],
            embeddings=embed(),
            llm=ChatOllama(
    model="gemma4:cloud", base_url="https://ollama.com", num_predict=250, temperature=0
)
        ),
    )
    print(resultado.to_pandas()[["question", "faithfulness", "answer_relevancy"]])
