import json
import sys
from src.rag.retriever import rag_indexar
from src.ai.engine.memory import TokenMemory
from src.ai.guardrails import Input_Guardrail
from src.ai.client.instancia import instanciarAi
from src.dados import Mensagem, Papel, exemplos
from src.schema import AnalisePostos, AnaliseResposta


class AiEngine:
    def __init__(self, model: str =  "gemini-3.1-flash-lite") -> None:
        self.client = instanciarAi(model)
        self.memory = TokenMemory()
    def responder(self, prompt: str):
        guardrail = Input_Guardrail(prompt)
        
        
        if len(guardrail.validar_input()) > 0:
            return "Pergunta rejeitada pelo sistemas"
   
        classificacao = self.client.chamarDiretamente(
            prompt,
            
            system="analise_pergunta",
            formato=AnaliseResposta.model_json_schema(),
            mensagem_direta=prompt
        )


        prompt_final = """
[classificação]
{classificacao}

[input do usuário]
{prompt}
        """
        resposta_final = self.client.chamarDiretamente(
            prompt_final,
            system="system_prompt",
            historico=self.memory.chat_message(),
            dados={
                "classificacao": classificacao.replace("{", "\\{{").replace("}", "\\}}"),
                # "analise": analise.replace("{", "\\{{").replace("}", "\\}}"),
                "prompt": prompt,
            },
            mensagem_direta=prompt,
            usar_context=True
        )
        
        self.memory.save_context(Mensagem(prompt, Papel.USUARIO))
        self.memory.save_context(Mensagem(resposta_final, Papel.CHAT))
        
        return  resposta_final 
