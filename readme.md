# Track Automação Python

## 📋 Descrição

Sistema de automação para envio de pesquisas de satisfação para pacientes de hospitais através da API Track.co. O sistema coleta dados de pacientes de diferentes áreas hospitalares (ambulatório, exames, internação, maternidade, pronto socorro e oncologia) e agenda o envio automático de pesquisas por email e WhatsApp.

## 🏥 Hospitais Suportados

### HUB ES (Meridional)
- **HMS** - Meridional Serra
- **HPC** - Meridional Praia da Costa  
- **HMV** - Meridional Vitória
- **HMC** - Meridional Cariacica
- **HSF** - Hospital São Francisco
- **HSL** - Hospital São Luiz
- **HMSM** - Meridional São Mateus

### Outros
- **OTO_ING** - Otorrinolaringologia e Ingleses
- **HAT** - Hospital de Alta Tecnologia
- **HAC** - Hospital de Alta Complexidade
- **HPM_HST** - Hospital de Pronto Socorro e Hospital Santa Teresa
- **HSMC** - Hospital Santa Maria da Conceição

## 🏗️ Arquitetura

```
Track_Automacao_py/
├── app/
│   ├── __init__.py              # Configuração da aplicação Flask
│   ├── db/                      # Camada de banco de dados
│   │   ├── db.py               # Conexões Oracle (MV e TASY)
│   │   ├── querys_mv/          # Queries para banco MV
│   │   └── querys_tasy/        # Queries para banco TASY
│   ├── routes/
│   │   └── api_router.py       # Rotas da API
│   ├── scheduler/
│   │   ├── automations.py      # Lógica de automação principal
│   │   └── schedulers.py       # Agendamento de tarefas
│   └── service/
│       ├── track_api.py        # Integração com API Track.co
│       ├── survey_uuid.py      # UUIDs das pesquisas por hospital
│       └── calc_d1.py         # Cálculos de datas
├── run.py                      # Ponto de entrada da aplicação
└── requirements.txt            # Dependências Python
```

## 🚀 Funcionalidades

### Áreas de Pesquisa
- **Ambulatório**: Consultas ambulatoriais, consultas de retorno, especialidades médicas
- **Exames**: Exames laboratoriais, de imagem, hemodinâmica, ultrassonografia
- **Internação**: Pacientes internados em enfermarias gerais, UTIs, semi-intensivos
- **Maternidade**: Pacientes obstétricas, partos, cesáreas, acompanhamento pré-natal
- **Pronto Socorro**: Atendimentos de emergência, urgência, observação
- **Oncologia**: Tratamentos oncológicos, quimioterapia, radioterapia

### Canais de Distribuição
- **Email**: Envio de pesquisas por email com template personalizado
- **WhatsApp**: Envio de pesquisas via WhatsApp com templates aprovados
- **Links**: Geração de links únicos para pesquisas individuais
- **Lembretes**: Sistema de lembretes automáticos (7 e 14 dias após envio)

### Tipos de Atendimento Suportados
- **A (Ambulatório)**: Consultas agendadas, retornos, especialidades
- **E (Exames)**: Exames externos, laboratoriais, de imagem
- **I (Internação)**: Pacientes internados, alta hospitalar
- **U (Urgência)**: Pronto socorro, emergências, observação

## 🛠️ Tecnologias

- **Python 3.x**
- **Flask**: Framework web
- **APScheduler**: Agendamento de tarefas
- **cx_Oracle**: Conexão com banco Oracle
- **Pandas**: Manipulação de dados
- **Requests**: Chamadas HTTP para API externa

## 📦 Instalação

### Pré-requisitos
- **Python**: 3.7+ (recomendado 3.9+)
- **Oracle Client**: 19c ou superior instalado e configurado
- **Acesso aos bancos**: MV (Meridional) e TASY (Sistema hospitalar)


### Dependências do Sistema
- **cx_Oracle**: Driver Oracle para Python
- **Oracle Instant Client**: Biblioteca cliente Oracle
- **Pandas**: Para manipulação de dados
- **APScheduler**: Para agendamento de tarefas
- **Flask**: Framework web para API
- **Requests**: Para chamadas HTTP à API Track.co

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd Track_Automacao_py
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# ou
source venv/bin/activate  # Linux/Mac
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente
Crie um arquivo `.env` na raiz do projeto:

```env
# API Track.co
ORGANIZATION_UUID=seu_uuid_organizacao
API_TOKEN=seu_token_api

# Banco de Dados MV (Meridional)
DB_USERNAME=usuario_mv
DB_PASSWORD=senha_mv
ORACLE_CLIENT_PATH=

# Banco de Dados TASY
DB_USERNAME_TASY=usuario_tasy
DB_PASSWORD_TASY=senha_tasy

# Configurações dos bancos por hospital
DB_HMS_HOST=
DB_HMS_PORT=
DB_HMS_NAME=

DB_HMC_HOST=
DB_HMC_PORT=
DB_HMC_NAME=

DB_HPC_HOST=
DB_HPC_PORT=
DB_HPC_NAME=

DB_HMV_HOST=
DB_HMV_PORT=
DB_HMV_NAME=

DB_HSF_HOST=
DB_HSF_PORT=
DB_HSF_NAME=

DB_HSL_HOST=
DB_HSL_PORT=
DB_HSL_NAME=

DB_HMSM_HOST=
DB_HMSM_PORT=
DB_HMSM_NAME=

DB_OTO_ING_HOST=
DB_OTO_ING_PORT=
DB_OTO_ING_NAME=

DB_HAT_HOST=
DB_HAT_PORT=
DB_HAT_NAME=

DB_HAC_HOST=
DB_HAC_PORT=
DB_HAC_NAME=

DB_HPM_HST_HOST=
DB_HPM_HST_PORT=
DB_HPM_HST_NAME=

DB_HSMC_HOST=
DB_HSMC_PORT=
DB_HSMC_NAME=

# Flask
FLASK_RUN_PORT=5000
```

## 🚀 Execução

### Execução Manual
```bash
flask run
```

## 📊 Monitoramento

### Logs
O sistema gera logs em `system.log` com informações sobre:
- Conexões com bancos de dados
- Execução de agendamentos
- Envios de pesquisas
- Erros e avisos

### Endpoint de Status
- **URL**: `http://localhost:5000/`
- **Funcionalidade**: Exibe o conteúdo do log do sistema


## 🔧 Desenvolvimento

### Estrutura de Queries
Cada hospital possui seu próprio metedo de query em `app/db/querys_mv/` ou `app/db/querys_tasy/`. Para adicionar um novo hospital:

1. Crie um novo metedo seguindo o padrão existente
2. Implemente o método `DB()` que retorna os dados dos pacientes
3. Adicione o hospital em `app/service/survey_uuid.py`
4. Configure os UUIDs das pesquisas

## 📊 Monitoramento e Logs

### Estrutura dos Logs
O sistema gera logs detalhados em `system.log` com o seguinte formato:

```
[2025-01-15 10:30:00] - Hospital HMS iniciado
[2025-01-15 10:30:01] - Banco conectado! MV 
[2025-01-15 10:30:02] - HMS - AMBULATORIO -  schedulers iniciado
[2025-01-15 10:30:03] - HMS - EXAMES -  schedulers iniciado
[2025-01-15 10:30:04] - HMS - INTERNACAO -  schedulers iniciado
[2025-01-15 10:30:05] - HMS - MATERNIDADE -  schedulers iniciado
[2025-01-15 10:30:06] - HMS - PRONTO SOCORRO -  schedulers iniciado
[2025-01-15 10:30:07] - HMS - ONCOLOGIA -  schedulers iniciado
```

### Níveis de Log
- **INFO**: Operações normais (conexões, agendamentos)
- **WARNING**: Avisos (hospital não encontrado, sem dados)
- **ERROR**: Erros críticos (falha na API, erro de banco)


## 🔒 Segurança

### Variáveis de Ambiente
- **Nunca** commite credenciais no repositório
- Use arquivo `.env` local ou variáveis do sistema
- Rotacione senhas regularmente
- Use usuários com privilégios mínimos no banco

### Acesso ao Banco
- **MV**: Usuário com acesso apenas às tabelas necessárias
- **TASY**: Usuário com permissões de leitura específicas



### Docker
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["flask", "run"]
```


**Versão**: 1.0.0  