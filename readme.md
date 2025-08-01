
# Automação de Envio de Pesquisas Track.co

Este projeto consiste em uma aplicação Flask para automatizar o envio de pesquisas da plataforma Track.co. A aplicação é capaz de se conectar a um banco de dados Oracle, interagir com a API da Track.co para buscar e enviar pesquisas por e-mail e WhatsApp, além de agendar tarefas de forma recorrente.

## Funcionalidades

* **API RESTful:** Expõe endpoints para interagir com o sistema.
* **Integração com a Track.co:** Conecta-se à API da Track.co para buscar pesquisas e criar distribuições de envio.
* **Conexão com Banco de Dados Oracle:** Inclui um módulo para conexão com um banco de dados Oracle.
* **Agendamento de Tarefas:** Utiliza a biblioteca `apscheduler` para executar tarefas em segundo plano (ex: envio diário de pesquisas).
* **Cálculo de Datas:** Possui uma função utilitária para calcular datas específicas com base no dia da semana.
* **Configuração via Variáveis de Ambiente:** Carrega configurações sensíveis a partir de um arquivo `.env`, mantendo a segurança.

## Estrutura do Projeto

```
.
├── app/
│   ├── controllers/
│   │   └── api_controller.py   # Controladores que lidam com a lógica das rotas
│   ├── db/
│   │   └── db.py               # Módulo de conexão com o banco de dados
│   ├── routes/
│   │   └── api_router.py       # Definição das rotas da API
│   ├── service/
│   │   ├── calc_d2.py          # Utilitário para cálculo de datas
│   │   ├── jobs.py             # Agendador de tarefas
│   │   └── track_api.py        # Serviço para comunicação com a API da Track.co
│   ├── __init__.py             # Inicializador da aplicação Flask
│   └── config.py               # Configurações da aplicação
├── .env.example                # Exemplo de arquivo de variáveis de ambiente
├── .gitignore                  # Arquivos e pastas ignorados pelo Git
├── requirements.txt            # Lista de dependências do projeto
└── run.py                      # Ponto de entrada para executar a aplicação
```

## Pré-requisitos

* Python 3.x
* pip

## Como Configurar e Executar

1.  **Clone o repositório:**
    ```bash
    git clone <URL_DO_REPOSITORIO>
    cd <NOME_DO_DIRETORIO>
    ```

2.  **Crie e ative um ambiente virtual (recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure as variáveis de ambiente:**
    * Renomeie o arquivo `.env.example` para `.env`.
    * Abra o arquivo `.env` e preencha as variáveis com suas credenciais e configurações:
        ```ini
        DB_USERNAME=seu_usuario_do_banco
        DB_PASSWORD=sua_senha_do_banco
        DB_HOST=host_do_banco
        DB_PORT=porta_do_banco
        DB_NAME=nome_do_servico_do_banco
        API_TOKEN=seu_token_da_api_track.co
        ORGANIZATION_UUID=seu_uuid_da_organizacao_track.co
        FLASK_RUN_PORT=5555
        ```

5.  **Execute a aplicação:**
    ```bash
    flask run
    ```
    Ou diretamente com o `run.py`:
    ```bash
    python run.py
    ```
    A aplicação estará rodando em `http://0.0.0.0:5555` (ou a porta que você definiu em `FLASK_RUN_PORT`).

## Endpoints da API

* **`GET /`**
    * **Descrição:** Rota de "health check" para verificar se a aplicação está no ar.
    * **Resposta:** `"O bot está funcionando....."`

As rotas a seguir estão comentadas em `app/routes/api_router.py` e podem ser ativadas conforme a necessidade:

* **`GET /`** (apontando para `getSurveys`)
    * **Descrição:** Busca as pesquisas disponíveis na sua organização na Track.co.
    * **Controlador:** `api_controller.getSurveys`

* **`GET /add`** (apontando para `postDistribution`)
    * **Descrição:** Envia uma pesquisa específica por e-mail para uma lista de contatos pré-definida no código.
    * **Controlador:** `api_controller.postDistribution`

## Agendamento de Tarefas

O arquivo `app/service/jobs.py` contém a lógica para agendar tarefas. Em `app/__init__.py`, a função `jobs.schedule_task` é chamada para agendar a tarefa `api_controller.postDistributionEmail` para ser executada a cada 24 horas.

## Dependências

As principais dependências do projeto são:

* **Flask**: Framework web.
* **Flask-Cors**: Para lidar com Cross-Origin Resource Sharing (CORS).
* **cx_Oracle**: Driver para conexão com o banco de dados Oracle.
* **python-dotenv**: Para carregar variáveis de ambiente de um arquivo `.env`.
* **apscheduler**: Para agendamento de tarefas em background.
* **pandas**: Utilizado para manipulação de dados.
* **requests**: Para realizar requisições HTTP para a API da Track.co.

## PROXIMOS PASSOS 

* Puxar dados reais da database
* Criar diretorios com sql dos hospitais
* Integração com WhatsApp