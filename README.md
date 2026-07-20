# API de Grupo Econômico - Desafio Sicredi

API desenvolvida para o desafio técnico da Sicredi, responsável por importar associados de um arquivo CSV para o MongoDB e disponibilizar uma consulta por grupo econômico.

A aplicação importa os dados de um arquivo CSV para o MongoDB, consulta os associados pelo número da conta e não retorna a própria conta usada na busca.

## Tecnologias

- Python
- FastAPI
- MongoDB
- Beanie
- Pydantic v2
- Docker e Docker Compose
- pytest

## Pré-requisitos

- Python 3.13+
- Docker
- Docker Compose

## Configuração

Crie o arquivo `.env` a partir do exemplo:

```bash
cp .env.example .env
```

Variáveis disponíveis:

```env
MONGO_URI=mongodb://localhost:27017
DATABASE_NAME=sicredi
CSV_IMPORT_PATH=data/cadastro_visao_geral_associado_conta.csv
CSV_IMPORT_TIME=02:00
```

`CSV_IMPORT_TIME` usa o formato `HH:MM`, considerando o timezone do servidor da aplicação.

## Executando a aplicação

Suba o MongoDB:

```bash
docker-compose up -d
```

Crie o ambiente virtual e instale as dependências:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Inicie a API:

```bash
.venv/bin/uvicorn app.api.main:app --reload
```

Durante o startup, a aplicação inicializa o MongoDB e importa uma vez o CSV definido em `CSV_IMPORT_PATH`. Assim, a API já fica pronta para consulta.

Depois que a importação inicial termina com sucesso, o scheduler diário é iniciado. Ele agenda uma nova importação do mesmo CSV uma vez por dia, no horário definido em `CSV_IMPORT_TIME`.

## Exemplo de uso

```bash
curl http://localhost:8000/associates/581516
```

Resposta esperada com o CSV de exemplo:

```json
[
  {
    "name": "Maria Fernanda Alves",
    "cpf_cnpj": "22872352687"
  },
  {
    "name": "Carlos Eduardo Santos",
    "cpf_cnpj": "68346379018"
  },
  {
    "name": "Ana Paula Costa",
    "cpf_cnpj": "50379613043"
  }
]
```

## Executando os testes

```bash
.venv/bin/python -m pytest tests
```

## Arquitetura

O fluxo de importação do CSV é tratado separadamente pelo scheduler, responsável pela sincronização inicial e pelas importações diárias.

O projeto segue uma arquitetura simples:

```text
Router -> Service -> Repository -> Beanie -> MongoDB
```

- Router: define os endpoints HTTP.
- Service: concentra a regra de negócio da consulta por grupo econômico.
- Repository: executa as consultas e atualizações no MongoDB usando Beanie.
- Scheduler: executa a importação inicial e agenda a sincronização diária do CSV.

## Estrutura do projeto

```text
app/
  api/          aplicação FastAPI e routers
  core/         configuração, banco, logging e normalização
  models/       documentos Beanie
  repositories/ consultas e upserts no MongoDB
  scheduler/    importação inicial e sincronização diária do CSV
  schemas/      schemas de resposta da API
  services/     regras de negócio
data/           CSV de exemplo
docs/           documentos do desafio
tests/          testes automatizados
```
