from datetime import date

from pydantic import BaseModel
from typing import List, Optional

from model.transacao.transacao_model import TransacaoModel
from model.transacao.enums.tipo_transacao_model import TipoTransacao
from schemas.transacao.observacao_schema import ObservacaoSchema


class TransacaoSchema(BaseModel):
    # Campo id opcional: utilizado em operações de listagem/visualização; ignorado no POST
    id: Optional[int] = None
    data_vencimento: Optional[date] = None
    descricao: str = "Salario"
    tipo_transacao: TipoTransacao = TipoTransacao.RECEITA
    valor: float = 3587.82
    pago: bool = False
    data_pagamento: Optional[date] = None
    pedido_id: Optional[int] = None

class TransacaoAtualizacaoSchema(BaseModel):
    """Schema para atualização parcial de transação vinculada a um pedido.

    Todos os campos são opcionais; apenas os fornecidos serão atualizados.
    """
    data_vencimento: Optional[date] = None
    descricao: Optional[str] = None
    tipo_transacao: Optional[TipoTransacao] = None
    valor: Optional[float] = None
    pago: Optional[bool] = None
    data_pagamento: Optional[date] = None

class TransacaoBuscaSchema(BaseModel):
    descricao: str = "Salario"

class ListagemTransacoesSchema(BaseModel):
    transacoes: List[TransacaoSchema]

def apresenta_transacoes(transacoes: List[TransacaoModel]):
    result = []
    for transacao in transacoes:
        result.append({
            "id": transacao.id,
            "data_vencimento": transacao.data_vencimento,
            "descricao": transacao.descricao,
            "tipo_transacao": transacao.tipo_transacao.value,
            "valor": transacao.valor,
            "pago": transacao.pago,
            "data_pagamento": transacao.data_pagamento,
            "observacoes": [{"texto": o.texto, "data_inclusao": o.data_inclusao} for o in transacao.observacoes],
            "pedido_id": transacao.pedido_id
        })
    return {"transacoes": result}

class TransacaoViewSchema(BaseModel):
    """ Define como a transação será retornada na API
    """
    id: int = 1
    data_vencimento: Optional[date] = None
    descricao: str = "Salario"
    tipo_transacao: TipoTransacao = TipoTransacao.RECEITA
    valor: float = 3587.82
    pago: bool = False
    data_pagamento: Optional[date] = None
    observacoes: List[ObservacaoSchema]
    pedido_id: Optional[int] = None

class TransacaoDelSchema(BaseModel):
    message: str
    descricao: str

def apresenta_transacao(transacao: TransacaoModel):
    return {
        "id": transacao.id,
        "data_vencimento": transacao.data_vencimento,
        "descricao": transacao.descricao,
        "tipo_transacao": transacao.tipo_transacao.value,
        "valor": transacao.valor,
        "pago": transacao.pago,
        "data_pagamento": transacao.data_pagamento,
        "observacoes": [{"texto": o.texto, "data_inclusao": o.data_inclusao} for o in transacao.observacoes],
        "pedido_id": transacao.pedido_id
    }