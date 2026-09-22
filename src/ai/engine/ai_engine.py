import json
import sys
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
        #     "Tipo": "Duvida",
        # "tema": "Pagamento",
        # "Intencao_principal": "Aconselhar sobre o funcionamento do pagamento",
        # "palavras_chaves": ["sistema","pagamento","efetuar"]
        # "Resumo": "Usuario informa que não sabe como efetuar o pagamento"
        classificacao = self.client.chamarDiretamente(
            prompt,
            
            system="analise_pergunta",
            formato=AnaliseResposta.model_json_schema(),
        )
        postosStr = "\n".join(
            [
                x.model_dump_json().replace("{", "\\{{").replace("}", "\\}}")
                for x in exemplos()
            ]
        )
        # return classificacao
        prompt_relatorio = """
[postos]
{postosStr}
[input do usuário]
{prompt}
        """

        # return prompt_relatorio

        analise = self.client.chamarDiretamente(
            prompt_relatorio,
            system="relatorio",
            historico=self.memory.chat_message(),
            dados={"postosStr": postosStr, "prompt": prompt},
            formato=AnalisePostos.model_json_schema()
        )

        prompt_final = """
[classificação]
{classificacao}
[analise]
{analise}

[input do usuário]
{prompt}
        """
        resposta_final = self.client.chamarDiretamente(
            prompt_final,
            system="system_prompt",
            historico=self.memory.chat_message(),
            dados={
                "classificacao": classificacao.replace("{", "\\{{").replace("}", "\\}}"),
                "analise": analise.replace("{", "\\{{").replace("}", "\\}}"),
                "prompt": prompt,
            },
        )
        
        self.memory.save_context(Mensagem(prompt, Papel.USUARIO))
        self.memory.save_context(Mensagem(resposta_final, Papel.CHAT))
        
        return  resposta_final 
