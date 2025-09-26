# 💸 App Econome - Transações API

API REST em Python (Flask 3 + flask-openapi3) para gerenciamento de transações financeiras. Expõe operações de criação, listagem, consulta e remoção de transações, além do vínculo de observações. Oferece documentação automática multi-interface (Swagger UI, ReDoc, RapiDoc, RapiPDF, Scalar e Elements), logging estruturado e validação via Pydantic.

---

## 🧰 Tecnologias Utilizadas
- Python 3.13
- Flask 3 (flask-openapi3)
- Pydantic 2
- SQLAlchemy 2 (ORM)
- SQLite (arquivo local)
- Flask-CORS
- Docker & Docker Compose

---

## ✅ Pré-requisitos
- Docker e Docker Compose (recomendado)
- (Opcional) Python 3.13+ e `pip` caso queira executar sem Docker

---

## ▶️ Executando a Aplicação com Docker (recomendado)

1. Clone o repositório:
   ```bash
   git clone https://github.com/usuario/app-econome-transacoes.git
   cd app-econome-transacoes
   ```
2. Suba o container:
   ```bash
   docker compose up -d --build
   ```
3. Acesse no navegador:
   - Redirecionamento padrão: http://localhost:5001 (leva a /openapi)
   - Swagger UI: http://localhost:5001/swagger
   - ReDoc: http://localhost:5001/redoc
   - RapiDoc: http://localhost:5001/rapidoc
   - RapiPDF: http://localhost:5001/rapipdf
   - Scalar: http://localhost:5001/scalar
   - Elements: http://localhost:5001/elements
   - OpenAPI JSON: http://localhost:5001/openapi

> O serviço utiliza SQLite local (arquivo `database/econome_db_transacoes.sqlite3`). Não há necessidade de provisionar banco externo.

Para parar:
```bash
docker compose down
```

---

## ⚙️ Execução Local (sem Docker)

1. Crie e ative um ambiente virtual (opcional mas recomendado):
   ```bash
   python -m venv env
   # Linux/macOS
   source env/bin/activate
   # Windows (PowerShell)
   .\env\Scripts\Activate.ps1
   # Windows (CMD)
   env\Scripts\activate.bat
   ```
2. Instale dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Execute a aplicação:
   ```bash
   python app.py
   ```
4. Acesse a documentação em: http://localhost:5001/openapi

---

## 🌐 Documentação OpenAPI
A aplicação expõe múltiplas interfaces automaticamente via `flask-openapi3`:
- /openapi (router de escolha)
- /swagger
- /redoc
- /rapidoc
- /rapipdf
- /scalar
- /elements

---

## 🧱 Estrutura do Projeto
```
app-econome-transacoes/
├── app.py                      # Ponto de entrada / configuração do OpenAPI e rotas
├── docker-compose.yml          # Orquestra container da API
├── Dockerfile                  # Build da imagem Python
├── requirements.txt            # Dependências
├── database/
│   ├── connection.py           # Criação de sessão e engine SQLAlchemy
│   └── econome_db_transacoes.sqlite3  # Banco SQLite (criado em runtime)
├── model/
│   ├── base/                   # Base declarativa
│   └── transacao/              # Modelos de domínio (Transacao, Observacao, enums)
├── resources/
│   └── transacao/              # Endpoints (transação e observação)
├── schemas/                    # Schemas Pydantic (entrada/saída + erros)
├── utils/
│   └── logger.py               # Configuração de logging
└── README.md
```

---

## 🧠 Principais Funcionalidades
- Criar transação (POST /transacao)
- Listar transações (GET /transacoes)
- Consultar transação por descrição (GET /transacao?descricao=...)
- Remover transação por descrição (DELETE /transacao?descricao=...)
- Adicionar observação a uma transação (POST /transacao/observacao)
- Documentação multi-formato OpenAPI

---

## 📌 Modelagem (Resumo)
Transação:
- id (int)
- descricao (string)
- tipo_transacao (enum: definido em `TipoTransacao`)
- valor (float)
- pago (bool)
- data_inclusao (datetime)
- data_pagamento (date | null)
- data_vencimento (date | null)
- observacoes (lista de Observacao)

Observação:
- id (int)
- fk_id_produto (id da transação associada)
- texto (string)

---

## 🔁 Endpoints (Resumo Rápido)
| Método | Caminho                  | Descrição                                 |
|--------|--------------------------|-------------------------------------------|
| POST   | /transacao               | Cria nova transação                       |
| GET    | /transacoes              | Lista todas as transações                 |
| GET    | /transacao?descricao=... | Busca transação pela descrição            |
| DELETE | /transacao?descricao=... | Remove transação pela descrição           |
| POST   | /transacao/observacao    | Adiciona observação em uma transação      |

---

## 🧪 Exemplos de Requisições

Criar transação:
```bash
curl -X POST http://localhost:5001/transacao \
  -H "Content-Type: application/json" \
  -d '{
    "descricao": "Conta de Luz Janeiro",
    "tipo_transacao": "DESPESA",
    "valor": 250.75,
    "pago": false,
    "data_vencimento": "2025-02-05"
  }'
```

Adicionar observação:
```bash
curl -X POST http://localhost:5001/transacao/observacao \
  -H "Content-Type: application/json" \
  -d '{
    "transacao_id": 1,
    "texto": "Pago com atraso"
  }'
```

Deletar transação:
```bash
curl -X DELETE "http://localhost:5001/transacao?descricao=Conta%20de%20Luz%20Janeiro"
```

---

## 🧩 Erros e Respostas
O schema de erros centraliza mensagens padronizadas (veja `schemas/error/error_schema.py`). Exemplos típicos:
- 400: Erro inesperado / validação
- 404: Recurso não encontrado
- 409: Conflito (integridade)

---

## 🔐 Observações sobre Qualidade e Arquitetura
- Separação clara: `model` (ORM), `schemas` (validação/IO), `resources` (rotas), `database` (infra), `utils` (cross-cutting)
- Uso de SQLAlchemy 2 + Session scoped manual
- Pydantic 2 para tipagem e validação de entrada/saída
- Múltiplos formatos de documentação via `flask-openapi3`
- Logging centralizado (`utils/logger.py`)
- Enum de domínio para tipo de transação garante consistência

---

## 🚧 Próximas Melhorias (Sugestões)
- Adicionar migrações (Alembic)
- Paginação em /transacoes
- Filtros por período, status de pagamento
- Autenticação (JWT) e autorização
- Testes automatizados (pytest + coverage)
- Padronização de resposta de erro expandida (códigos internos)

---

## 👤 Autor
Desenvolvido por **Lucas Almeida**.
