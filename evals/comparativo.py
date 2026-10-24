from evals.ragas import avaliar

def avaliar_comparativo():
    models =  ["gemini-3.5-flash-lite", "gemini-3.1-flash-lite"]

    for model in models:
        print(f"executando testes para {model}")
        
        avaliar(model)