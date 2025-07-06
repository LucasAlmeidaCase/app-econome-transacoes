from datetime import date

from pydantic import BaseModel
from typing import List, Optional

from model.transacao.transacao_model import TransacaoModel
from model.transacao.enums.tipo_transacao_model import TipoTransacao
from schemas.transacao.observacao_schema import ObservacaoSchema


class TransacaoSchema(BaseModel):
    data_vencimento: Optional[date] = None
    descricao: str = "Salario"
    tipo_transacao: TipoTransacao = TipoTransacao.RECEITA
    valor: float = 3587.82
    pago: bool = False
    data_pagamento: Optional[date] = None

class TransacaoBuscaSchema(BaseModel):
    descricao: str = "Salario"

class ListagemTransacoesSchema(BaseModel):
    transacoes: List[TransacaoSchema]

def apresenta_transacoes(transacoes: List[TransacaoModel]):
    result = []
    for transacao in transacoes:
        result.append({
            "data_vencimento": transacao.data_vencimento,
            "descricao": transacao.descricao,
            "tipo_transacao": transacao.tipo_transacao.value,
            "valor": transacao.valor,
            "pago": transacao.pago,
            "data_pagamento": transacao.data_pagamento,
            "observacoes": [{"texto": o.texto, "data_inclusao": o.data_inclusao} for o in transacao.observacoes]
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
        "observacoes": [{"texto": o.texto, "data_inclusao": o.data_inclusao} for o in transacao.observacoes]
    }