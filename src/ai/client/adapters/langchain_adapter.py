import os
from typing import Literal

from langchain_classic.memory.chat_memory import BaseChatMemory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory
from src.rag.retriever import rag_indexar
from src.dados import Mensagem, Papel
from src.ai.client.adapters.ai_adapter import AiAdapter, system_prompts
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.memory import ConversationTokenBufferMemory
# from langchain_classic.runnables import 

retriever = rag_indexar()

class LangChainAdapter(AiAdapter):
    def __init__(self, model: str  = "gemini-3.1-flash-lite") -> None:
        self.model = ChatGoogleGenerativeAI(
            model=model,
            api_key=os.getenv("CHAVE_GEMINI"),
            
        )
        self.memory: BaseChatMemory = ConversationTokenBufferMemory(llm=self.model, max_token_limit=400)
   
    def chamarDiretamente(self, prompt: str,historico: list[Mensagem] = [],  system: system_prompts = "system_prompt", formato: dict | None = None, dados: dict = {}, *, mensagem_direta: str, usar_context: bool = False) -> str:
        
        self.model.max_output_tokens = 300
        self.model.temperature = 0.4
        self.model.top_p = 0.5 
        if formato:
            self.model.response_schema = formato
            self.model.response_mime_type = "application/json"
        else:
            self.model.response_mime_type = "text/plain"
            self.model.response_schema  = None
        # base = open("assets/prompt/templates/base.md").read()
        # return base
        
        def formatar_contexto(docs) -> str:
            partes = []
            for i, doc in enumerate(docs, 1):
                fonte = doc.metadata.get("source", "doc")
                pg = doc.metadata.get("page", "?")
                partes.append(f"[Trecho {i} — {fonte}, pág. {pg+1}]\n{doc.page_content}")
            # print("\n\n---\n\n".join(partes))
            return "\n\n---\n\n".join(partes)

        template = ChatPromptTemplate( [
            ("system", self.base_system_prompt),
            #  MessagesPlaceholder("history"),
            *[( "ai" if mensagem.role == Papel.CHAT else "human", mensagem.conteudo) for mensagem in historico],
            ("human", f"""\
<contexto>
{{contexto}}
</contexto>             
{prompt}""" if usar_context else prompt)
            # MessagesPlaceholder("input")
        ], )
        
        # return sys.argv[1]
        # message = model.invoke(sys.argv[1])
        if usar_context:
            contexto = formatar_contexto(retriever.invoke(mensagem_direta)).replace("{", "\\{{").replace("}", "\\}}")
            template = template.partial(contexto=contexto)
        chain =  template  | self.model |  StrOutputParser()
        # return contexto
        # if usar_memoria:
        #     chain = RunnableWithMessageHistory(chain, get_session_history=  lambda : self.memory.chat_memory, input_messages_key="prompt", history_messages_key="history" )
        input = self.obter_system_prompt_params(system) | dados
        # print(chain)
        message = chain.invoke(input)
        # if usar_memoria:
        #     # print(template.messages[-1].content)
        #     self.memory.save_context(inputs={"human": template.messages[-1].}, outputs={"ai": message })  # pyright: ignore[reportAttributeAccessIssue]
        # print(message)
        return message