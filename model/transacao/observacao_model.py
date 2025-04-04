from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from model.base.base_model import Base

class ObservacaoModel(Base):
    __tablename__ = 'observacao'

    id = Column(Integer, primary_key=True, autoincrement=True)
    texto = Column(String(5000))
    data_inclusao = Column(DateTime, default=datetime.now())

    fk_id_produto = Column(Integer, ForeignKey("transacao.pk_transacao"), nullable=False)

    def __init__(self, fk_id_produto: int, texto: str, data_inclusao: datetime = None):
        self.fk_id_produto = fk_id_produto
        self.texto = texto
        self.data_inclusao = data_inclusao if data_inclusao else datetime.now()