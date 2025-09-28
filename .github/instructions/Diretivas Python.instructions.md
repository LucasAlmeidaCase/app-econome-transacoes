---
applyTo: '**'
---

# Prompt de Implementação Python (EconoMe API)

"Sempre que eu solicitar uma implementação ou refatoração de código em Python para este projeto, siga rigorosamente as diretrizes abaixo. O código deve ser limpo, coeso e aderente às boas práticas de APIs REST modernas com Flask 3, flask-openapi3, SQLAlchemy 2 e Pydantic 2.

---

### 1. Padrões de Código e Nomenclatura

* Use **PEP8** como base (nomes claros, snake_case para funções/variáveis, PascalCase para classes).
* Evite abreviações obscuras; priorize legibilidade e clareza semântica.
* Nomeie rotas de forma consistente, usando substantivos no plural para coleções (`/transacoes`, `/observacoes`).

---

### 2. Organização do Projeto

* Respeite a arquitetura definida no repositório:

  * `model/` → entidades ORM do SQLAlchemy (separar base/declarações/domain).
  * `schemas/` → Pydantic models para entrada/saída e erros.
  * `resources/` → rotas/endpoints (controllers).
  * `database/` → conexão, sessão e engine.
  * `utils/` → logging e funções cross-cutting.
* Não misture responsabilidades: validação no `schemas`, persistência no `model`/`DAO`, lógica de negócio em services (quando aplicável), API em `resources`.

---

### 3. Arquitetura e Princípios

* Siga **SOLID** adaptado ao Python/Flask:

  * **SRP**: cada módulo deve ter uma única responsabilidade clara.
  * **DIP**: abstraia dependências quando fizer sentido (ex: repositórios).
* Prefira **injeção de dependência explícita** (passando sessão/serviço como argumento).
* Nunca coloque lógica de negócio dentro de controllers; concentre em funções/métodos separados.

---

### 4. Integração com Flask + OpenAPI

* Sempre defina schemas de request e response com **Pydantic**.
* Documente endpoints via decorators do `flask-openapi3` (para expor corretamente em Swagger/ReDoc).
* Use **Flask-CORS** quando necessário, sem configurações excessivas globais.
* Prefira **tipagem estática (type hints)** em todos os métodos.

---

### 5. Persistência (SQLAlchemy 2 + SQLite)

* Utilize **ORM declarativo** para mapear entidades.
* Use **Session local** (`scoped_session`) ou `async_session` se expandir no futuro.
* Evite SQL hardcoded espalhado; prefira abstrações via ORM.
* Lembre-se de sempre fechar sessões ou usar `with Session()` (context manager).
* Nunca inclua lógica de negócio dentro dos modelos ORM.

---

### 6. Validação e Schemas (Pydantic 2)

* Centralize validações de entrada e saída nos schemas.
* Prefira **BaseModel do Pydantic** com `ConfigDict` para conversões (`orm_mode=True`).
* Evite `Any`; defina tipos corretos (`str`, `float`, `datetime.date`, enums).
* Use **enums de domínio** (como `TipoTransacao`) para consistência de valores.

---

### 7. Tratamento de Erros

* Padronize erros com schemas em `schemas/error/`.
* Use exceções específicas (ex: `TransacaoNaoEncontradaError`) em vez de genéricas.
* Retorne mensagens claras no JSON, mas evite vazar detalhes internos (SQL, stacktrace).
* Sempre diferencie status codes:

  * `400` → erro de validação
  * `404` → não encontrado
  * `409` → conflito
  * `500` → erro interno

---

### 8. Qualidade e Manutenção

* Métodos curtos e focados em uma responsabilidade.
* Evite duplicação de lógica (extraia para helpers/services).
* Testes unitários com **pytest**, cobrindo rotas, serviços e DAO.
* Logging estruturado via `utils/logger.py`, sem `print`.

---

### 9. Decisões de Design

* Caso haja dúvida entre expor lógica diretamente em rotas ou extrair para service/repository, **prefira service/repository**.
* Pergunte antes de alterar convenções arquiteturais (ex: troca de SQLite por Postgres, ou introdução de Alembic).
* Prefira soluções simples e consistentes em vez de abstrações complexas desnecessárias.

---

### **Instrução de Entrega**

Sempre que for solicitado:

* Implemente ou refatore código seguindo os critérios acima.
* Inclua tipagem explícita, validações adequadas e logging.
* Garanta que o código seja **coeso, legível, testável e alinhado à arquitetura existente**."