# Classificação 
## Tipo
- Duvida
- Suporte
- Critica
- Comentario
## Tema
- Pagamento: qualquer assunto relacionado ao pagamento
- carregamento: Qualquer assunto relacionado ao carregador 
- posto: qualquer assunto referente a escolha de postos

## O JSON deve ter
- tipo
- Tema
- intenção principal
- palavras_chaves
- resumo

## Formato do JSON
- input recebido: "É a minha primeira vez utilizando este sistema, como faço para efetuar o pagamento?"
\{{
    "Tipo": "Duvida",
    "tema": "Pagamento",
    "Intencao_principal": "Aconselhar sobre o funcionamento do pagamento",
    "palavras_chaves": ["sistema","pagamento","efetuar"],
    "Resumo": "Usuario informa que não sabe como efetuar o pagamento"
\}}
- input recebido:"Quero fazer uma critica sobre a quantidade de vagas disponiveis em cada posto, achei inaceitável o pouco espaço que temos disponivel"
\{{
    "Tipo": "Critica",
    "tema": "Posto",
    "Intencao_principal": "Fazer uma queixa sobre as vagas disponiveis",
    "palavras_chaves": ["critica","posto","vagas_disponiveis"],
    "Resumo": "Usuario que fazer uma critica acerca das vagas disponiveis em cada posto"
\}}
- input recebido:"preciso que me ajude com o carregador, parece que não esta funcionando ou sei lá"
\{{
    "Tipo": "suporte",
    "tema": "Carregamento",
    "Intencao_principal": "suporte necessario para arrumar o carregador em uso",
    "palavras_chaves":["preciso","ajude","carregador","funcionando"],
    "Resumo": "Usuario requer o suporte para arrumar uma falha em um dos carregadores"
\}}