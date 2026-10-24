# Sprint 3 - chat ai

## Depêndencias

### ambiente

- python:3.13.13
- venv

### bibliotecas

requests
textual
pydantic
google-genai
pandas
python-dotenv
langchain
langchain-ollama
langchain-google-genai
langchain_classic
tiktoken
streamlit
gradio
pymupdf
chromadb
ragas
langchain-community

### ais e modelos

#### gemini

para caso de uso com gemini, estas são as depêndencias

- ai: gemini
- api: google ai studio (obtenção de chave e uso da api)
- modelo: gemini-3.1-flash-lite

#### ollama

para casos de uso com o ollama, basta ter ele instalado em sua maquina e escolher o seu modelo de preferência, não definimos nenhuma stack obrigátoria para o ollama, é de sua escolha

## estrutura de pasta

```
└── 📁sprint 2
    └── 📁evals
        ├── ragas.py
    └── 📁assets
        └── 📁css # pasta para estilos usados pelo textual
            ├── styles.tcss
            ├── teste-styles.tcss
        └── 📁prompts # pasta para system prompts
            └── 📁v1 # prompts antigos
                ├── analise_pergunta.md # system prompt para analise e classificação da pergunta do usuário
                ├── relatorio.md # system prompt para analise e relatorio dos postos disponiveis
                ├── system_prompt.md # system prompt final, que se comunica com o usuário e se utiliza dos dados das outras duas ais
            └── 📁v2 # prompts da versão 2
                └── 📁 analise # system prompt para analise e classificação da pergunta do usuário
                    ├── extra.md
                    ├── identidade.md
                    ├── objetivo.md
                    ├── regras.md
                └── 📁 relatorio # system prompt para analise e relatorio dos postos disponiveis
                    ├── identidade.md
                    ├── objetivo.md
                    ├── regras.md
                └── 📁 system_prompt  # system prompt final, que se comunica com o usuário e se utiliza dos dados das outras duas ais
                    ├── extra.md
                    ├── identidade.md
                    ├── regras.md
                ├── base.md # prompt base usado como template
            └── 📁v3 # prompts novos
                └── 📁 analise # system prompt para analise e classificação da pergunta do usuário
                    ├── extra.md
                    ├── identidade.md
                    ├── objetivo.md
                    ├── regras.md
                └── 📁 system_prompt  # system prompt final, que se comunica com o usuário e se utiliza dos dados das outras ais
                    ├── extra.md
                    ├── identidade.md
                    ├── regras.md
                ├── base.md # prompt base usado como template
        ├── relatorio.csv # arquivo com os resultados dos testes
        ├── relatorio-gemini-3.1-flash-lite.csv # arquivo com os resultados dos testes do modelo gemini 3.1 flash lite
        ├── relatorio-gemini-3.5-flash-lite.csv # arquivo com os resultados dos testes do modelo gemini 3.5 flash lite
    └── 📁docs # documentos
        ├── relatorio_evolucao.pdf # relatorio de evolução
        ├── relatorio_modelos.md # relatorio comparativo entre modelos
        ├── relatorio_rag.md
    └── 📁data
        └── 📁knowledge_base
            ├── BASE DE CONHECIMENTO TÉCNICA(RAG).pdf
    └── 📁src
        └── 📁ai # pasta para todos os códigos referentes a ai
            └── 📁client # pasta pata criação de um cliente de comunicação com a ai
                └── 📁adapter # pasta para diferentes implementações de ia variando de acordo com o modelo e a forma de uso
                    ├── ai_adapter.py # classe abstrata para cliente de ai
                    ├── gemini_genai_adapter.py # adaptador para gemini atráves da biblioteca google-genai
                    ├── gemini_requests_adapter.py # adaptador para gemini através de requests
                    ├── ollama_request.py # adptador para ollama
                    ├── langchain_adapter.py
                ├── instancia.py # instancia de ai, ele verifica a situação do env e escolher se o modelo será gemini ou ollama
            └── 📁engine
                ├── ai_engine.py # classe para uso principal da ia, diferente do client, que são comunicações diretas e genericas, o engine implementa comunicação especifica para o objetivo do projeto e uso de multiplas ais em uma mesma respostas
                ├── memory.py # gerenciamento de mémoria da ai
            └── 📁rag # codigo para rags
                ├── loader.py
                ├── prompt_rag.py
                ├── retriever.py
                ├── vector_store.py
                ├── embeddings.py
                ├── chucking.py
            ├── evalutor.py
            ├── guardrails.py
        └── 📁screens # pasta para as telas do sistema
            ├── main_screen.py # tela de interação
            ├── teste_tela.py # tela de teste
        ├── dados.py
        ├── schema.py
    ├── .env # arquivo env principal, não virá junto ao clone do projeto, você deve criar e seguir os arquivos de exemplo para executar o projeto
    ├── .env.example.gemini # exemplo de arquivo env para usar gemini
    ├── .env.example.ollama # exemplo de arquivo env para usar ollama
    ├── .gitignore
    ├── main.py # arquivo de execução principal
    ├── README.md
    └── requirements.txt
```

## Execusão

para rodar o projeto, primeiro é necessário clonar o projeto em sua maquina

```
git clone https://github.com/Joao-Lucas-Si/2026-ai-sprint-3.git
```

após isso, entre na pasta criada

```
cd 2026-ai-sprint-3

```

antes de executar o projeto, primeiro é neccessário garantir que as depêndencias de ai se encontram funcionando, a primeira é o gemini, a ai usada diretamente nesse projeto, e o ollama, a ia usada para o embedding do rags

### gemini

para uso do gemini, entre no google ai studio, crie uma conta, e procure gerar uma chave da api, sendo ela a padrão, ou uma criada junto a um projeto

com a ai pronta, crie um arquivo .env no diretório principal, e siga os arquivos de exemplos como .env.example

```
CHAVE_GEMINI=<sua chave de api do gemini>
```

### ollama

devido algums problemas com o ollama cloud para embeds, é preciso tanto ter ele em sua maquina quanto ter a chave do ollama cloud, siga as instruções do [site oficial](https://ollama.com/download): 

após ter o ollama em sua maquina, inicie o servidor e rode com o modelo de embeddings, cada comando em um terminal distinto


```base
ollama serve

ollama pull nomic-embed-text
```

depois insira sua chave do ollama cloud dentro do .env
```
OLLAMA_API_KEY=<sua chave do ollama cloud>
```

com a ai pronta, crie um arquivo .env no diretório principal, e siga os arquivos de exemplos como .env.example.gemini ou .env.example.ollama.

com o arquivo .env criado e configurado, crie e entre em um ambiente python e atualize as dependencias

```
python -m venv venv

# para linux
source venv/bin/activate
# para wnindows
./venv/Scripts/Activate.ps1

pip install -r requirements.txt
```

rode o projeto python, há duas formas principais, rodar com streamlit ativará o chat em modo interação, onde mensagem podem ser enviadas, ou usar o arquivo teste.py para ativar o modo teste, onde prompts pré definidos são executados e depois mostrados como estatisticas

modo interação

```
streamlit run main.py
```

modo teste

```
python teste.py
```

dentro do modo teste há um modo alternativo, que é o modo comparativo, que pega dois modelos e executa os mesmos testes para cada um, para ativar esse modo, siga o código abaixo:

```
python teste.py --comparativo
```
