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
            ├── analise_pergunta.md # system prompt para analise e classificação da pergunta do usuário
            ├── relatorio.md # system prompt para analise e relatorio dos postos disponiveis
            ├── system_prompt.md # system prompt final, que se comunica com o usuário e se utiliza dos dados das outras duas ais
        ├── relatorio.csv # arquivo com os resultados dos testes
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

| pergunta                                                | acuracia | estado                | resposta           |
| ------------------------------------------------------- | -------- | --------------------- |----------------------------------------------------------------- |
| Quais carregadores estão disponíveis neste momento?     | 0.75     | adequada              | Olá. Sou a EnergyAI e estou aqui para auxiliar você. Com base no monitoramento atual da rede, aqui estão os pontos com disponibilidade imediata para o carregamento do seu veículo: **Posto Shopping Tamboré:** Este é o local com a maior disponibilidade, apresentando todos os carregadores operacionais e livres para uso. **Posto do Aeroporto:** Encontra-se com 50% de sua capacidade disponível. **Posto Ipiranga:** Possui 2 de seus 3 carregadores livres no momento. **Atenção:** O **Posto do Villa Lobos** encontra-se atualmente com todos os carregadores ocupados, portanto, não é recomendado que se dirija a este local caso necessite de recarga imediata. Recomendo priorizar o Posto Shopping Tamboré para garantir que você não encontre filas ou esperas. Posso ajudar com mais alguma informação sobre a localização ou o tipo de carregador disponível nesses postos?                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| Minha recarga foi interrompida, o que aconteceu?        | 0.8      | adequada              | Olá. Eu sou a EnergyAI e sinto muito pelo transtorno causado pela interrupção da sua recarga. Como não tenho acesso direto aos logs individuais da sua sessão específica no momento, não é possível apontar a causa exata sem uma análise técnica detalhada. No entanto, interrupções inesperadas geralmente ocorrem por um dos seguintes motivos: **Variação na rede elétrica:** Oscilações de tensão podem levar o carregador a interromper a sessão por questões de segurança. **Falha na comunicação:** Se o cabo sofrer uma desconexão física parcial ou se houver perda de sinal do protocolo OCPP, o sistema interrompe o fornecimento para evitar danos. **Configuração do veículo:** Alguns sistemas de gerenciamento de bateria do próprio veículo podem solicitar o encerramento da carga por atingir o limite programado ou superaquecimento. **Sobrecarga ou limite de tempo:** Em locais com alta demanda, o sistema de gerenciamento de energia pode priorizar o balanceamento da carga, o que pode resultar em desligamentos preventivos. **Recomendações de segurança e próximos passos:****Verificação física:** Certifique-se de que o cabo está firmemente conectado ao seu veículo e ao carregador. Verifique se não há sinais de danos físicos no plugue ou no cabo.**Reinicialização:** Tente iniciar uma nova sessão. Se o erro persistir, o equipamento pode estar passando por uma falha técnica.**Alternativa:** Caso o posto em que você se encontra apresente instabilidade recorrente, recomendo que utilize o **Posto Shopping Tamboré**, que no momento apresenta 100% de disponibilidade e alta confiabilidade operacional. Evite, por ora, o Posto Villa Lobos, que se encontra operando em carga máxima, o que pode gerar gargalos.Se você puder me informar o local exato (posto) e o horário da interrupção, posso registrar este evento em nosso sistema para que nossa equipe de manutenção técnica verifique o histórico do carregador específico. Como está o status das luzes indicadoras no painel do carregador agora? Isso ajudará no diagnóstico. |
| Como iniciar uma sessão de carregamento?                | 0.6      | parcialmente adequada | Olá. Sou a EnergyAI, assistente de gerenciamento da rede de carregadores GoodWe. Para iniciar uma sessão de carregamento em nossos postos, siga estas etapas padrão: **Estacionamento:** Posicione seu veículo de forma que o cabo de carregamento alcance a porta de carga do carro sem tensionar o fio. **Conexão:** Insira o conector do carregador na entrada do seu veículo. Certifique-se de que o encaixe esteja firme e travado. **Autenticação:** No painel do carregador ou no aplicativo indicado no posto, selecione o carregador correspondente e inicie a sessão (via cartão RFID, QR Code ou interface do próprio equipamento). **Verificação:** Aguarde a luz indicadora do carregador mudar para a cor que sinaliza o início do fluxo de energia (geralmente azul ou verde, dependendo do modelo). Verifique no painel do seu veículo se o processo de carregamento foi iniciado. **Observações importantes:** Por questões de segurança, nunca force a conexão do cabo. Caso o carregador apresente uma luz vermelha ou mensagem de erro no painel, não tente forçar o início. Entre em contato com o suporte local para diagnóstico. Considerando a disponibilidade atual, recomendo utilizar o **Posto Shopping Tamboré** ou o **Posto Ipiranga**, que apresentam as melhores condições operacionais no momento. Evite postos com alta demanda, como o do Villa Lobos, para garantir que você tenha um suporte estável durante a carga. Caso encontre dificuldades técnicas durante esses passos, informe-me o código de erro exibido na tela para que eu possa realizar o diagnóstico.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| Meu pagamento foi feito mas o carregador não funciona?  | 0.8      | adequada              | Olá. Compreendo a sua frustração com essa situação. Eu sou a EnergyAI e serei responsável por orientá-lo nesta ocorrência. Como sistema de monitoramento, informo que não possuo acesso direto aos fluxos financeiros ou ao processamento de pagamentos. No entanto, para resolver o problema de o carregador não iniciar a carga após o processamento, sugiro que siga estes passos de segurança e verificação: 1. **Verificação física:** Certifique-se de que o cabo de carregamento esteja conectado firmemente tanto ao carregador quanto ao seu veículo. Um encaixe incompleto pode impedir o início da carga por segurança. 2. **Reinicialização da tentativa:** Se possível, retire o cabo, aguarde 30 segundos e reinicie o processo de conexão seguindo as instruções na tela do posto. 3. **Contato de suporte:** Como o pagamento foi processado, é necessário que você entre em contato com o suporte técnico local do posto específico onde se encontra. Eles possuem as ferramentas necessárias para liberar a carga remotamente ou realizar o estorno do valor, caso o equipamento apresente falha técnica. **Informação adicional:** Caso não consiga resolver o problema nesta unidade, informo que o **Posto Shopping Tamboré** e o **Posto do Aeroporto** estão com disponibilidade operacional no momento e operando normalmente. Por favor, mantenha o comprovante de pagamento à disposição para facilitar o atendimento junto à equipe de suporte do posto. Registrarei este incidente em nosso sistema para análise técnica preventiva.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| O carregador não reconheceu meu veículo, o que eu faço? | 0.5      | parcialmente adequada | Olá. Compreendo que está enfrentando dificuldades para iniciar o carregamento. Eu sou a EnergyAI e estou aqui para auxiliar no diagnóstico do sistema. Para solucionar essa falha de reconhecimento entre o carregador e o seu veículo, por favor, siga os passos abaixo: 1. **Verificação física do cabo:** Certifique-se de que o conector está totalmente inserido na porta de carga do veículo e que a trava de segurança foi acionada corretamente. Um encaixe parcial é a causa mais comum desse problema. 2. **Ciclo de conexão:** Desconecte o cabo, aguarde cerca de 10 segundos e tente realizar o procedimento de conexão novamente, garantindo que o comando de início seja feito conforme as instruções na tela do carregador ou no aplicativo. 3. **Status do veículo:** Verifique se o seu veículo possui alguma configuração de ""agendamento de carga"" ou ""limite de carga"" ativa, que pode estar impedindo o início imediato do processo. 4. **Inspeção visual:** Verifique se não há obstruções, sujeira ou danos visíveis nos pinos do cabo ou na entrada do veículo que possam comprometer a comunicação (protocolo de handshake). **Observação importante:** Como sou uma inteligência artificial voltada ao monitoramento da infraestrutura, não consigo intervir fisicamente no hardware ou nos protocolos específicos do seu veículo. Caso o problema persista após essas tentativas, recomendo que se desloque para um dos nossos postos com alta disponibilidade, como o **Posto Shopping Tamboré** ou o **Posto Ipiranga**, onde a infraestrutura está operando de forma estável. Se o problema for recorrente em outros pontos, sugiro que entre em contato com o suporte técnico da montadora do seu veículo para verificar o sistema de carregamento embarcado. Mantenho este evento registrado em nosso sistema para análise técnica. Deseja que eu forneça a localização de algum dos postos recomendados?                                                                                                                                                  |
