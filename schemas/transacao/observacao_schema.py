from datetime import datetime

from pydantic import BaseModel


class ObservacaoSchema(BaseModel):
    transacao_id: int = 1
    texto: str = "Observação sobre a transação"