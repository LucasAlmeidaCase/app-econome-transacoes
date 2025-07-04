# API EconoMe

Este projeto faz parte do material didático da Disciplina **Desenvolvimento Full Stack Básico**.

O objetivo deste projeto é ilustrar o conteúdo apresentado ao longo das três aulas da disciplina.
<hr></hr>

## ✅ Pré-requisitos

- [Docker](https://www.docker.com/) e [Docker Compose](https://docs.docker.com/compose/)
- (Opcional) [Python 3.x](https://www.python.org/downloads/) e `pip`, caso deseje rodar localmente sem Docker

---

## 🚀 Como executar o projeto

### ▶️ Executando com Docker (recomendado)

1. Clone o repositório:

    ```bash
    git clone https://github.com/usuario/app-econome-backend.git
    cd app-econome-backend
    ```

2. Inicie os containers:

    ```bash
    docker compose up -d --build
    ```

3. Acesse a API no navegador:

    👉 <http://localhost:5001>

Se estiver tudo certo, você será redirecionado para a interface de documentação (/openapi).

⚙️ Executando localmente (sem Docker)

Será necessário ter todas as libs Python listadas no `requirements.txt` instaladas. Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

### Criar e ativar um ambiente virtual

```bash
python -m venv env
source env/bin/activate  # No Windows use `env\Scripts\activate`
```

### Instalação das dependências

```bash
pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas descritas no arquivo `requirements.txt`.

Para executar a API basta utilizar o comando:

```bash
python app.py
```

Abra o <http://localhost:5001/#/> no navegador para verificar o status da API em execução.
