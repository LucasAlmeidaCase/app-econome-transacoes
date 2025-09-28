import os.path

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
import re

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

"""
Rotina simples de "migração" incremental:

1) Se a coluna pedido_id ainda não existir na tabela transacao (bancos criados antes da funcionalidade
    de vínculo Pedido-Transação), ela é adicionada via ALTER TABLE e um índice único é criado. Em seguida,
    tentamos fazer backfill a partir do padrão de descrição: "Pedido <numero> (#<id>)".

2) Se a coluna participant_id não existir (feature de associação opcional de Participante à transação),
    ela é adicionada e criado um índice simples (não unique). Não há backfill possível.

Obs.: Para algo mais robusto, considerar Alembic no futuro.
"""


def aplicar_migracoes_simples():
    inspector = inspect(engine)
    try:
        tables = inspector.get_table_names()
    except Exception:
        return
    if 'transacao' not in tables:
        # Tabela ainda não existe; será criada normalmente abaixo
        return
    col_names = [c['name'] for c in inspector.get_columns('transacao')]
    changed = False
    if 'pedido_id' not in col_names:
        with engine.begin() as conn:
            conn.execute(text("ALTER TABLE transacao ADD COLUMN pedido_id INTEGER"))
            # Em SQLite não dá para adicionar constraint UNIQUE facilmente após criação; criamos índice único.
            conn.execute(text("CREATE UNIQUE INDEX IF NOT EXISTS ix_transacao_pedido_id ON transacao(pedido_id)"))
        changed = True
        # Backfill best-effort
        pattern = re.compile(r"\(#(\d+)\)")
        with engine.begin() as conn:
            result = conn.execute(text("SELECT pk_transacao, descricao FROM transacao WHERE pedido_id IS NULL"))
            for row in result.fetchall():
                pk, desc = row
                if not desc:
                    continue
                m = pattern.search(desc)
                if not m:
                    continue
                pedido_id = int(m.group(1))
                try:
                    conn.execute(text("UPDATE transacao SET pedido_id = :pid WHERE pk_transacao = :pk"), {"pid": pedido_id, "pk": pk})
                except Exception:
                    # Ignora conflitos (duplicados) para manter operação resiliente
                    pass
    if 'participant_id' not in col_names:
        with engine.begin() as conn:
            conn.execute(text("ALTER TABLE transacao ADD COLUMN participant_id INTEGER"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS ix_transacao_participant_id ON transacao(participant_id)"))
        changed = True
    if not changed:
        return


# Aplica migrações simples antes de criar novas tabelas/colunas padrão
aplicar_migracoes_simples()
Base.metadata.create_all(engine)