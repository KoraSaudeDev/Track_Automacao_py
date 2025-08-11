# Track_Automacao_py

Automação completa de disparos de pesquisas Track.co utilizando Flask, integração com banco Oracle, agendamento de tarefas e envio de pesquisas por e-mail e WhatsApp.

---

## Visão Geral

Este projeto foi desenvolvido para automatizar o envio de pesquisas de satisfação para pacientes, integrando-se à API Track.co e ao banco de dados Oracle hospitalar. O disparo é agendado e pode ser feito por e-mail ou WhatsApp, com logs detalhados das execuções. O código é modular, didático e pronto para expansão.

---

## Estrutura de Diretórios e Explicação dos Arquivos

- **app/**: Diretório principal da aplicação.
     - **__init__.py**: Inicializa o Flask, registra as rotas e inicia o agendador de automações. Ao importar, já executa o agendamento automático.
     - **db/**: Responsável pela conexão e queries no banco Oracle.
          - **db.py**: Função `get_connection(db_alias)` conecta ao Oracle usando variáveis de ambiente, retornando um objeto de conexão pronto para uso em queries.
          - **querys/**: Diretorio com as queryes.
     - **routes/**: Diretorio onde contem as rotas.
          - **api_router.py**: Blueprint principal, define a rota `/` que retorna o status da aplicação.
     - **scheduler/**: Gerencia o agendamento de tarefas automáticas.
          - **schedulers.py**: Usa APScheduler para agendar o envio de pesquisas. Funções:
                - `send_email(data, survey_uuid)`: Envia pesquisas por e-mail usando a API Track.co.
                - `send_wpp(data, survey_uuid)`: Envia pesquisas por WhatsApp.
                - `schedule_task(task_func)`: Agenda uma função para execução periódica.
                - `start_schedulers(data, survey_uuid)`: Inicia o agendador e agenda as tarefas.
          - **automations.py**: Exemplo de uso do agendador. Função `teste()` retorna dados simulados de pacientes. Função `start()` agenda o envio de pesquisas usando esses dados.
     - **service/**: Serviços auxiliares e integrações externas.
          - **track_api.py**: Funções para consumir a API Track.co:
                - `getSurveys()`: Busca pesquisas disponíveis na organização.
                - `postDistribution(survey_uuid, distribution_channel, import_lines)`: Envia pesquisas por e-mail.
                - `postDistributionWhatsapp(survey_uuid, distribution_channel, import_lines)`: Envia pesquisas por WhatsApp, com template e integração configurados.
          - **calc_d1.py**: Função `get_filtered_dates(reference_date=None)` retorna a data de ontem (ou de referência) no formato esperado para as queries SQL.

- **requirements.txt**: Lista de dependências do projeto (Flask, cx_Oracle, APScheduler, requests, pandas, etc).
- **run.py**: Ponto de entrada da aplicação (pode ser usado para rodar o Flask manualmente).
- **system.log**: Arquivo de log das execuções, útil para auditoria e troubleshooting.

---

## Instalação e Execução Passo a Passo

1. **Clone o repositório:**
    ```bash
    git clone <url-do-repositorio>
    cd Track_Automacao_py
    ```
2. **Crie e ative um ambiente virtual (recomendado):**
    ```bash
    python -m venv venv
    venv\Scripts\activate  # No Windows
    # ou
    source venv/bin/activate  # No Linux/Mac
    ```
3. **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
4. **Configure as variáveis de ambiente** (exemplo no `.env`):
    ```ini
    ORGANIZATION_UUID=...
    API_TOKEN=...
    DB_USERNAME=...
    DB_PASSWORD=...
    DB_OTO_ING_HOST=...
    DB_OTO_ING_PORT=...
    DB_OTO_ING_NAME=...
    ORACLE_CLIENT_PATH=...
    ```
5. **Execute a aplicação:**
    ```bash
    flask run
    ```

---

## Fluxo Completo do Sistema

1. **Inicialização:**
    - Ao iniciar, o sistema executa `automations.start()`, que agenda o envio de pesquisas com dados de teste (ou reais, se adaptado).
2. **Agendamento:**
    - O módulo `schedulers.py` usa APScheduler para agendar tarefas.
3. **Coleta de Dados:**
    - O diretorio db/queryes contém os sql necessarios para cada hospital.
4. **Logs:**
    - Todas as operações relevantes (envio, erros, execuções) são logadas em `system.log` para auditoria e troubleshooting.

---

## Explicação Detalhada dos Principais Arquivos e Funções

### app/__init__.py

- Inicializa o Flask e registra o blueprint de rotas.
- Executa o agendador de automações ao importar o módulo.
- Função `create_app()` retorna a aplicação Flask pronta para uso.

### app/routes/api_router.py

- Define a rota `/` para checagem de status da aplicação.
- Retorna uma mensagem simples indicando que a aplicação está rodando.

### app/scheduler/automations.py

- Função `teste()`: Retorna uma lista de dicionários simulando pacientes (nome, e-mail, telefone, CPF).
- Função `start()`: Chama o agendador para iniciar o envio de pesquisas usando os dados de teste e um UUID de pesquisa.

### app/scheduler/schedulers.py

- Usa APScheduler para agendamento.
- Função `send_email(data, survey_uuid)`: Chama a API Track.co para enviar pesquisas por e-mail.
- Função `send_wpp(data, survey_uuid)`: Chama a API Track.co para enviar pesquisas por WhatsApp.
- Função `schedule_task(task_func)`: Agenda uma função para execução periódica (pode ser diária ou a cada X segundos).
- Função `start_schedulers(data, survey_uuid)`: Agenda as tarefas e inicia o scheduler.

### app/service/track_api.py

- Função `getSurveys()`: Busca todas as pesquisas disponíveis na organização Track.co.
- Função `postDistribution(survey_uuid, distribution_channel, import_lines)`: Envia pesquisas por e-mail para os pacientes informados.
- Função `postDistributionWhatsapp(survey_uuid, distribution_channel, import_lines)`: Envia pesquisas por WhatsApp, utilizando template e integração previamente configurados na Track.co.
- Todas as funções fazem log das operações e tratam erros, registrando no arquivo `system.log`.

### app/db/db.py

- Função `get_connection(db_alias)`: Conecta ao banco Oracle usando as variáveis de ambiente e retorna um objeto de conexão pronto para uso.
- Utiliza o driver cx_Oracle e suporta múltiplos bancos via alias.

### app/service/calc_d1.py

- Função `get_filtered_dates(reference_date=None)`: Retorna a data de ontem (ou de referência) no formato esperado para as queries SQL.
- Útil para buscar dados do dia anterior automaticamente.

---

## Endpoints Disponíveis

- `GET /` — Verifica se o bot está funcionando. Retorna mensagem simples.

---

## Observações Importantes

- O agendamento de disparos pode ser configurado para rodar diariamente ou em outro intervalo.
- Os logs são salvos em `system.log` e são essenciais para auditoria e troubleshooting.
- O código é modular, facilitando manutenção e expansão.
- O envio por WhatsApp ainda está em desenvolvimento.

