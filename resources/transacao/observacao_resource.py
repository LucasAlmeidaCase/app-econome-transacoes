from flask_openapi3 import Tag

from database.connection import Session
from model.transacao.observacao_model import ObservacaoModel
from model.transacao.transacao_model import TransacaoModel
from schemas.error.error_schema import ErrorSchema
from schemas.transacao.observacao_schema import ObservacaoSchema
from schemas.transacao.transacao_schema import TransacaoViewSchema, apresenta_transacao
from utils.logger import logger

observacao_tag = Tag(name="Observações", description="Operações relacionadas às observações das transações")


def config_observacao_routes(app):
    @app.post('/transacao/observacao', tags=[observacao_tag], responses={"200": TransacaoViewSchema,
                                                                         "404": ErrorSchema.Config.json_schema_extra[
                                                                             "examples"]["404"]["value"],
                                                                         "400": ErrorSchema.Config.json_schema_extra[
                                                                             "examples"]["400"]["value"]})
    def add_observacao(form: ObservacaoSchema):
        """Adiciona uma observação a uma transação existente

        Retorna a transação atualizada com a nova observação.
        """
        logger.debug(f"Adicionando observação à transação ID {form.transacao_id}")
        try:
            session = Session()
            transacao = session.query(TransacaoModel).filter(TransacaoModel.id == form.transacao_id).first()

            if not transacao:
                logger.warning(f"Transação com ID {form.transacao_id} não encontrada")
                return {"message": "Transação não encontrada"}, 404

            observacao = ObservacaoModel(fk_id_produto=form.transacao_id, texto=form.texto)
            transacao.adiciona_observacao(observacao)

            session.commit()
            logger.debug(f"Observação adicionada com sucesso à transação ID {form.transacao_id}")
            return apresenta_transacao(transacao), 200

        except Exception as e:
            logger.error(f"Erro ao adicionar observação: {str(e)}")
            return {"message": "Erro inesperado ao adicionar observação"}, 400
