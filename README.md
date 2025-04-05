# API EconoMe
Este projeto faz parte do material didático da Disciplina **Desenvolvimento Full Stack Básico**.

O objetivo deste projeto é ilustrar o conteúdo apresentado ao longo das três aulas da disciplina.
<hr></hr>

## Pré-requisitos

- Python 3.x
- pip

## Como executar
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

Abra o http://localhost:5000/#/ no navegador para verificar o status da API em execução.