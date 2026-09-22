# Sprint 3 - chat ai

## Depêndencias

### ambiente

- python:3.13.13
- venv

### bibliotecas

- requests
- textual
- pydantic
- google-genai
- langchain
- pandas
- dotenv

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
    └── 📁assets
        └── 📁css # pasta para estilos usados pelo textual
            ├── styles.tcss
            ├── teste-styles.tcss
        └── 📁prompts # pasta para system prompts
            └── 📁v1 # prompts antigos
                ├── analise_pergunta.md # system prompt para analise e classificação da pergunta do usuário
                ├── relatorio.md # system prompt para analise e relatorio dos postos disponiveis
                ├── system_prompt.md # system prompt final, que se comunica com o usuário e se utiliza dos dados das outras duas ais
            └── 📁v2 # prompts novos
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
        ├── relatorio.csv # arquivo com os resultados dos testes
        ├── relatorio-gemini-3.1-flash-lite.csv # arquivo com os resultados dos testes do modelo gemini 3.1 flash lite
        ├── relatorio-gemini-3.5-flash-lite.csv # arquivo com os resultados dos testes do modelo gemini 3.5 flash lite
    └── 📁docs # documentos
        ├── relatorio.pdf # relatorio de evolução
        ├── relatorio_modelos.md # relatorio comparativo entre modelos
    └── 📁src
        └── 📁ai # pasta para todos os códigos referentes a ai
            └── 📁client # pasta pata criação de um cliente de comunicação com a ai
                └── 📁adapter # pasta para diferentes implementações de ia variando de acordo com o modelo e a forma de uso
                    ├── ai_adapter.py # classe abstrata para cliente de ai
                    ├── gemini_genai_adapter.py # adaptador para gemini atráves da biblioteca google-genai
                    ├── gemini_requests_adapter.py # adaptador para gemini através de requests
                    ├── ollama_request.py # adptador para ollama
                ├── instancia.py # instancia de ai, ele verifica a situação do env e escolher se o modelo será gemini ou ollama
            └── 📁engine
                ├── ai_engine.py # classe para uso principal da ia, diferente do client, que são comunicações diretas e genericas, o engine implementa comunicação especifica para o objetivo do projeto e uso de multiplas ais em uma mesma respostas
                ├── memory.py # gerenciamento de mémoria da ai
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
git clone https://github.com/Joao-Lucas-Si/sprint-2-ai.git
```

após isso, entre na pasta criada

```
cd sprint-2-ai

```

antes de executar o projeto, primeiro é neccessário garantir que as depêndencias de ai se encontram funcionando, siga as intruções de acordo com sua escolha de ai, o projeto foi feito pensando no gemini, mas o ollama é uma opção caso não seja possivel usar a api da google.

### gemini

para uso com gemini, entre no google ai studio, crie uma conta, e procure gerar uma chave da api, sendo ela a padrão, ou uma criada junto a um projeto

com a ai pronta, crie um arquivo .env no diretório principal, e siga os arquivos de exemplos como .env.example

```
CHAVE_GEMINI=<sua chave de api do gemini>
```

com o arquivo .env criado e configurado, crie e entre em um ambiente python e atualize as dependencias

```
python -m venv venv

# para linux
source venv/bin/activate
# para wnindows
./venv/Scripts/Activate.ps1

pip install -r requirements.txt
```

rode o projeto python, há duas formas principais, rodar o arquivo diretamente ativará o chat em modo interação, onde mensagem podem ser enviadas, ou usar a flag --teste para ativar o modo teste, onde prompts pré definidos são executados e depois mostrados como estatisticas

modo interação

```
python main.py
```

modo teste

```
python main.py --teste
```

dentro do modo teste há um modo alternativo, que é o modo comparativo, que pega dois modelos e executa os mesmos testes para cada um, para ativar esse modo, siga o código abaixo:

```
python main.py --teste comparativo
```

## Teste

para aplicar os testes decidimos reduzir os nove exemplos da tarefa anterior para 5, focando nas testes voltados a suporte e recomendação, devido a não ser possível aplicar testes relacionados a pagamento e histórico de usuário no contexto em que esse projeto foi desenvolvido atualmente, só sendo quando fomos implementar a ai no projeto final.

o teste funciona enviando uma pergunta pré definida para a ia e depois verificando se há as palavras chaves corretas presentes, a tabela abaixo classifica os inputs feitos no teste e suas palavras chaves

| input                                                   | palavras chaves                                             |
| ------------------------------------------------------- | ----------------------------------------------------------- |
| Quais carregadores estão disponíveis neste momento?     | disponivel, carregador, posto, ocupado                      |
| Minha recarga foi interrompida, o que aconteceu?        | recarga, limite,desconexão,verifique,suporte técnico        |
| Como iniciar uma sessão de carregamento?                | iniciar, conecte, cabo, recarga, carregador                 |
| Meu pagamento foi feito mas o carregador não funciona?  | pagamento, verifique, conectado, problema , suporte técnico |
| O carregador não reconheceu meu veículo, o que eu faço? | compatibilidade, verifique, problema, suporte técnico       |

para a classificação e avaliação de respostas, usamos uma métrica de acuracia, um número decimal de 0 a 1 que estabelece o quão apropriado a resposta era, a acuracia é calculada a partir da quantidade de palavras chaves encontradas nas respostas. fora da acuracia, há o estado, que é a classificação final da resposta, que é derivado da acuracia, seguinto a formula da tabela abaixo:

| acuracia necessária | estado                |
| ------------------- | --------------------- |
| de 0.7 a 1          | adequada              |
| de 0.4 a 0.7        | parcialmente adequada |
| de 0 a 0.4          | inadequada            |

| pergunta                                                | acuracia | estado                | resposta                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| ------------------------------------------------------- | -------- | --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Quais carregadores estão disponíveis neste momento?     | 0.75     | adequada              | Olá. Como assistente da EnergyAI, verifiquei o status da nossa rede de carregadores para você. No momento, possuímos 13 dos 15 carregadores monitorados disponíveis para uso. Recomendo os seguintes postos por apresentarem capacidade plena (100% de disponibilidade): _ **Posto Shopping Tamboré:** Todos os 4 carregadores estão livres. _ **Posto Ipiranga:** Todos os 4 carregadores estão livres. Os postos do **Aeroporto** e do **Villa Lobos** também possuem carregadores liberados, porém, em cada um deles, há um equipamento ocupado no momento. Se precisar de mais alguma informação ou auxílio com algum desses pontos, estou à disposição.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| Minha recarga foi interrompida, o que aconteceu?        | 0.6      | parcialmente adequada | Olá. Compreendo a sua situação. Como assistente do sistema, verifiquei o status operacional e buscarei esclarecer o ocorrido. A interrupção de uma recarga pode ocorrer por diversos fatores técnicos ou operacionais. Embora não possamos determinar a causa exata sem uma análise detalhada da sessão específica, as causas mais comuns incluem: 1. **Erro de comunicação:** Uma falha momentânea no protocolo de ""handshake"" (comunicação inicial) entre o veículo e o carregador. 2. **Limite de tempo ou carga:** O término do ciclo de recarga programado ou o limite de energia estabelecido na sessão. 3. **Proteção térmica ou elétrica:** Uma interrupção preventiva do próprio sistema para garantir a segurança da rede e do seu veículo caso tenha sido detectada alguma variação fora dos parâmetros normais. **Orientações para solução:** _ **Verifique o painel do veículo:** Confirme se existe alguma mensagem de erro exibida no painel do próprio carro. _ **Procedimento de reconexão:** Desconecte o cabo, aguarde cerca de 30 segundos e inicie um novo ciclo de recarga. \* **Troca de carregador:** Caso a falha persista, sugiro que tente utilizar um dos carregadores listados como disponíveis. Atualmente, os carregadores **16, 41, 62, 37, 2, 94, 3, 6, 45, 72, 66 e 31** encontram-se operacionais e prontos para uso. Por questões de segurança, evite forçar repetidamente a conexão se o erro persistir. Caso o problema continue em diferentes postos, recomendo que verifique a integridade do cabo de carregamento do seu veículo. Estou monitorando o sistema. Se precisar de assistência adicional ou identificar um padrão na falha, por favor, me informe. |
| Como iniciar uma sessão de carregamento?                | 1        | adequada              | Para iniciar uma sessão de carregamento em um dos nossos postos, siga este procedimento padrão: 1. **Verifique a disponibilidade:** Certifique-se de que o carregador escolhido esteja com a luz indicativa de ""Disponível"" (geralmente na cor verde). No momento, os carregadores recomendados são: **62, 47, 81, 92, 35, 44 e 89**. 2. **Conexão Física:** Estacione seu veículo próximo ao carregador e conecte o cabo de recarga firmemente à porta do seu veículo. Certifique-se de que o encaixe esteja completo e sem folgas. 3. **Interface do Usuário:** Dirija-se à tela (totem) do carregador. Siga as instruções apresentadas no visor para selecionar a potência desejada ou identificar o seu perfil de usuário/aplicativo, caso seja solicitado pelo sistema. 4. **Início da Carga:** Após a autenticação e verificação da conexão, o sistema iniciará o fluxo de energia automaticamente. O painel do carregador exibirá o status ""Carregando"" e, em alguns modelos, as informações de tempo estimado e porcentagem da bateria.**Orientações importantes:** _ **Segurança:** Caso note qualquer dano visível no cabo ou no conector, não tente realizar a conexão e escolha outro equipamento. _ **Acompanhamento:** Acompanhe o início da carga pelo painel do seu veículo ou pela tela do posto. \* **Monitoramento:** Eu realizo o monitoramento do status dos carregadores, mas a iniciação da sessão é um procedimento manual realizado diretamente na interface do posto. Se encontrar qualquer erro no visor durante esse processo, por favor, me informe o código ou a mensagem exibida para que eu possa diagnosticar o ocorrido.                                           |
| Meu pagamento foi feito mas o carregador não funciona?  | 0.8      | adequada              | Olá! Compreendo a sua situação. Se o pagamento foi processado, mas o carregador não iniciou o funcionamento, o problema pode estar relacionado a uma falha de comunicação entre o sistema de pagamento e o equipamento, ou a um travamento temporário no terminal. Para sua segurança e resolução do problema, recomendo seguir estes passos: 1. **Verifique a conexão do cabo:** Certifique-se de que o conector está firmemente encaixado na entrada do veículo. 2. **Aguarde a sincronização:** Em alguns casos, a liberação do equipamento pode levar alguns instantes após a confirmação do pagamento. 3. **Utilize outro carregador:** Como o equipamento atual não está respondendo, recomendo utilizar um dos nossos postos disponíveis no momento, onde o sistema está operando normalmente: - Posto Shopping Tamboré (Carregador 31) - Posto do Aeroporto (Carregador 29) - Posto Ipiranga (Carregadores 13 ou 99) - Posto do Villa Lobos (Carregador 58) Caso o problema persista, entre em contanto com o suporte técnico.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| O carregador não reconheceu meu veículo, o que eu faço? | 0.75     | adequada              | Compreendo a situação. Quando o carregador não reconhece o veículo, o problema pode estar relacionado a uma falha de comunicação entre o conector e o sistema do automóvel ou a um erro na autenticação local do dispositivo. Para resolver este problema e garantir o carregamento do seu veículo, siga estes passos: 1. **Procedimento de Segurança:** Desconecte o cabo tanto do carregador quanto do veículo. Aguarde cerca de 30 segundos e verifique se não há obstruções, sujeira ou danos visíveis nos pinos do conector. 2. **Nova Tentativa:** Reconecte o cabo firmemente, certificando-se de que o encaixe esteja completo em ambas as pontas. Muitas vezes, um encaixe parcial impede o reconhecimento do protocolo de comunicação. 3. **Troca de Equipamento:** Se a falha persistir após uma nova tentativa, o problema pode ser específico do conector ou do carregador em uso. Recomendo que você verifique em um de nossos pontos de alta performance disponíveis: _ **Carregador 13 (Posto Villa Lobos):** 50kW de capacidade. _ **Carregador 47 (Posto do Aeroporto):** 49kW de capacidade. **Importante:** Evite o **Carregador 63**, pois ele está ocupado e apresenta instabilidade no momento. Se, ao trocar para um dos carregadores recomendados, o erro ainda persistir, por favor, me informe qual é o modelo do seu veículo e a mensagem exata exibida no painel. Isso me ajudará a registrar o evento em nosso sistema e realizar um diagnóstico mais preciso.                                                                                                                                                                                                             |
