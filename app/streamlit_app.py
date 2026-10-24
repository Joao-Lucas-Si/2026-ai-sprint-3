def rodar_streamlit():
    from src.ai.engine.ai_engine import AiEngine
    import streamlit as st

    from dotenv import load_dotenv

    load_dotenv()
    engine = AiEngine()

    st.set_page_config(page_title="Equipe 101 - EnergyAi", page_icon="🤖")
    st.title("Assistente EnergyAi - Equipe 101")
    st.caption(f"Modelo: gemini-3.1-flash-lite")

    # Histórico na sessão do Streamlit
    if "mensagens" not in st.session_state:
        st.session_state.mensagens = []

    for msg in st.session_state.mensagens:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if pergunta := st.chat_input("Digite sua mensagem..."):
        st.session_state.mensagens.append({"role": "user", "content": pergunta})
        with st.chat_message("user"):
            st.markdown(pergunta)

        with st.chat_message("assistant"):
            resposta = engine.responder(pergunta)
            # resposta = chain.invoke({"pergunta": pergunta})
            st.markdown(resposta)

        st.session_state.mensagens.append({"role": "assistant", "content": resposta})
