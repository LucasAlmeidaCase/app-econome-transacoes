from _pydatetime import date
from datetime import datetime
from typing import Union, Optional

from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, Boolean, Date
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
    data_pagamento = Column(Date, nullable=True)
    data_vencimento = Column(Date, nullable=True)
    # Relacionamento lógico com Pedido em outro microserviço (não enforced por FK aqui)
    pedido_id = Column(Integer, unique=True, index=True, nullable=True)
    # Relacionamento lógico com Participante (opcional) - não enforced (microserviço separado)
    participant_id = Column(Integer, index=True, nullable=True)

    observacoes = relationship("ObservacaoModel")

    def __init__(self, descricao: str, tipo_transacao: TipoTransacao, valor: float,
                 data_inclusao: Union[DateTime, None] = None, pago: bool = False, data_pagamento: Optional[date] = None,
                 data_vencimento: Optional[date] = None, pedido_id: Optional[int] = None,
                 participant_id: Optional[int] = None):
        self.descricao = descricao
        self.tipo_transacao = tipo_transacao
        self.valor = valor
        self.data_inclusao = data_inclusao if data_inclusao else datetime.now()
        self.pago = pago
        self.data_pagamento = data_pagamento
        self.data_vencimento = data_vencimento
        self.pedido_id = pedido_id
        self.participant_id = participant_id

    def adiciona_observacao(self, observacao: ObservacaoModel):
        self.observacoes.append(observacao)
