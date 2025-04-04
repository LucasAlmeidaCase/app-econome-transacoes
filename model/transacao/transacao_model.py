from datetime import datetime
from typing import Union

from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, Boolean
from sqlalchemy.orm import relationship

from model.base.base_model import Base
from model.transacao.observacao_model import ObservacaoModel
from model.transacao.enums.tipo_transacao_model import TipoTransacao


class TransacaoModel(Base):
    """
    Classe que representa uma transação financeira no sistema.
    """
    __tablename__ = 'transacao'

    id = Column("pk_transacao", Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(255), nullable=False)
    tipo_transacao = Column(Enum(TipoTransacao), nullable=False)
    valor = Column(Float(), nullable=False)
    data_inclusao = Column(DateTime, default=datetime.now())
    pago = Column(Boolean, nullable=False, default=False)

    observacoes = relationship("ObservacaoModel")

    def __init__(self, descricao: str, tipo_transacao: TipoTransacao, valor: float,
                 data_inclusao: Union[DateTime, None] = None, pago: bool = False):
        self.descricao = descricao
        self.tipo_transacao = tipo_transacao
        self.valor = valor
        self.data_inclusao = data_inclusao if data_inclusao else datetime.now()
        self.pago = pago

    def adiciona_observacao(self, observacao: ObservacaoModel):
        self.observacoes.append(observacao)
