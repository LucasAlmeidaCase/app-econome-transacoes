from pydantic import BaseModel


class ErrorSchema(BaseModel):
    """Schema para representar um erro genérico"""
    message: str
    code: int
    status: str

    class Config:
        json_schema_extra = {
            "examples": {
                "409": {
                    "summary": "Erro de integridade",
                    "value": {
                        "message": "Erro de integridade",
                        "code": 409,
                        "status": "Conflict"
                    }
                },
                "400": {
                    "summary": "Erro inesperado",
                    "value": {
                        "message": "Erro inesperado",
                        "code": 400,
                        "status": "Bad Request"
                    }
                },
                "404": {
                    "summary": "Recurso não encontrado",
                    "value": {
                        "message": "Recurso não encontrado",
                        "code": 404,
                        "status": "Not Found"
                    }
                }
            }
        }