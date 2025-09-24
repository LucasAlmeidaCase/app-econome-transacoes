import os.path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

# Importando os elementos definidos no modelo
from model.base.base_model import Base
from model.transacao.observacao_model import ObservacaoModel
from model.transacao.transacao_model import TransacaoModel

db_path = "database/"
# Verifica se o diretório não existe e cria um novo
if not os.path.exists(db_path):
    os.makedirs(db_path)
    print("Diretório de banco de dados criado.")

# URL de conexão para o banco de dados SQLite local
db_url = 'sqlite:///%s/econome_db_transacoes.sqlite3' % db_path

# Cria o banco de dados e a tabela
engine = create_engine(db_url, echo=False)

# Instancia um criador de sessão com o banco
Session = sessionmaker(bind=engine)

# Verifica se o banco de dados já existe e cria se não existir
if not database_exists(engine.url):
    create_database(engine.url)

# Cria as tabelas no banco de dados
Base.metadata.create_all(engine)