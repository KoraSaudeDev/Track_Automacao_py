
# Track_Automacao_py

Automação de disparos de pesquisas Track.co com Flask, Oracle, agendamento e integração via API.

---

## Estrutura de Diretórios

### app/
Contém toda a lógica da aplicação.

#### __init__.py
- Inicializa a aplicação Flask.
- Registra as rotas.
- Inicia o agendador de tarefas para disparo automático de pesquisas.

---

### app/db/
Responsável pela conexão e queries no banco Oracle.

- **db.py**: Função para conectar ao banco Oracle usando variáveis de ambiente.
- **querys/ING_OTO.py**: Executa uma query SQL para buscar pacientes e dados necessários para o disparo das pesquisas.

---

### app/routes/
Define as rotas da API Flask.

- **api_router.py**: Blueprint principal. Rota `/` retorna status do bot.

---

### app/scheduler/
Gerencia o agendamento de tarefas automáticas.

- **schedulers.py**: Usa APScheduler para agendar o envio diário de pesquisas por e-mail (e WhatsApp, se ativado). Loga execuções e inicializa o agendador.

---

### app/service/
Serviços auxiliares e integrações externas.

- **track_api.py**: Funções para consumir a API Track.co (buscar pesquisas, enviar distribuições por e-mail/WhatsApp).
- **calc_d1.py**: Função utilitária para calcular datas de referência (ex: ontem).

---

## Instalação

1. **Clone o repositório**
2. **Instale as dependências:**
    ```
    pip install -r requirements.txt
    ```
3. **Configure as variáveis de ambiente** (exemplo no `.env`):
    ```
    ORGANIZATION_UUID=...
    API_TOKEN=...
    DB_USERNAME=...
    DB_PASSWORD=...
    DB_OTO_ING_HOST=...
    DB_OTO_ING_PORT=...
    DB_OTO_ING_NAME=...
    ORACLE_CLIENT_PATH=...
    ```
4. **Execute a aplicação:**
    ```
    python run.py
    ```

---

## Principais Funcionalidades

- **API REST** com Flask
- **Agendamento** de disparos automáticos (APScheduler)
- **Integração com banco Oracle** (cx_Oracle)
- **Envio de pesquisas** por e-mail e WhatsApp via Track.co
- **Consulta de dados** com Pandas
- **Log de sistema** em arquivo

---

## Endpoints

- `GET /` — Verifica se o bot está funcionando.

---

## Observações

- O agendamento de disparos é feito diariamente.
- Os logs são salvos em `system.log`.
- O código é modular, facilitando manutenção e expansão.

---