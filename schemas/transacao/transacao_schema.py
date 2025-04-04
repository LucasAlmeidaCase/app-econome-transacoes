from pydantic import BaseModel
from typing import List

from model.transacao.transacao_model import TransacaoModel
from model.transacao.enums.tipo_transacao_model import TipoTransacao
from schemas.transacao.observacao_schema import ObservacaoSchema


class TransacaoSchema(BaseModel):
    descricao: str = "Salario"
    tipo_transacao: TipoTransacao = TipoTransacao.RECEITA
    valor: float = 3587.82
    pago: bool = True

class TransacaoBuscaSchema(BaseModel):
    descricao: str = "Salario"

class ListagemTransacoesSchema(BaseModel):
    transacoes: List[TransacaoSchema]

def apresenta_transacoes(transacoes: List[TransacaoModel]):
    result = []
    for transacao in transacoes:
        result.append({
            "descricao": transacao.descricao,
            "tipo_transacao": transacao.tipo_transacao.value,
            "valor": transacao.valor,
            "pago": transacao.pago,
            "observacoes": [{"texto": o.texto, "data_inclusao": o.data_inclusao} for o in transacao.observacoes]
        })
    return {"transacoes": result}

class TransacaoViewSchema(BaseModel):
    """ Define como a transação será retornada na API
    """
    id: int = 1
    descricao: str = "Salario"
    tipo_transacao: TipoTransacao = TipoTransacao.RECEITA
    valor: float = 3587.82
    pago: bool = True
    observacoes: List[ObservacaoSchema]

class TransacaoDelSchema(BaseModel):
    message: str
    descricao: str

def apresenta_transacao(transacao: TransacaoModel):
    return {
        "id": transacao.id,
        "descricao": transacao.descricao,
        "tipo_transacao": transacao.tipo_transacao.value,
        "valor": transacao.valor,
        "pago": transacao.pago,
        "observacoes": [{"texto": o.texto, "data_inclusao": o.data_inclusao} for o in transacao.observacoes]
    }