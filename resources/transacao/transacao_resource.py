from flask_openapi3 import Tag
from sqlalchemy.exc import IntegrityError

from database.connection import Session
from model.transacao.enums.tipo_transacao_model import TipoTransacao
from model.transacao.transacao_model import TransacaoModel
from schemas.error.error_schema import ErrorSchema
from schemas.transacao.transacao_schema import TransacaoSchema, apresenta_transacao, apresenta_transacoes, \
    TransacaoViewSchema, ListagemTransacoesSchema, TransacaoBuscaSchema
from utils.logger import logger

transacao_tag = Tag(name="Transações", description="Operações relacionadas as transações")


def config_transacao_routes(app):
    @app.post('/transacao', tags=[transacao_tag], responses={"200": TransacaoViewSchema,
                                                             "409": ErrorSchema.Config.json_schema_extra["examples"][
                                                                 "409"]["value"],
                                                             "400": ErrorSchema.Config.json_schema_extra["examples"][
                                                                 "400"]["value"]})
    def add_transacao(form: TransacaoSchema):
        """ Adiciona uma nova transação à base de dados

        Retorna uma representação da transação adicionada.
        """
        transacao = TransacaoModel(
            descricao=form.descricao,
            tipo_transacao=TipoTransacao(form.tipo_transacao),
            valor=form.valor,
            pago=form.pago
        )
        logger.debug(f"Adicionando transação: '{transacao.descricao}'")

        try:
            session = Session()
            session.add(transacao)
            session.commit()
            return apresenta_transacao(transacao), 200

        except IntegrityError:
            logger.error("Erro de integridade ao adicionar transação")
            return {"message": "Erro de integridade ao adicionar transação"}, 409

        except Exception as e:
            logger.error(f"Erro ao adicionar transação: '{transacao.descricao}', {str(e)}")
            return {"message": "Erro inesperado"}, 400

    @app.get('/transacoes', tags=[transacao_tag], responses={"200": ListagemTransacoesSchema,
                                                             "404": ErrorSchema.Config.json_schema_extra["examples"][
                                                                 "404"]["value"]})
    def get_transacoes():
        """Retorna todas as transações cadastradas"""
        try:
            session = Session()
            transacoes = session.query(TransacaoModel).all()
            if not transacoes:
                return {"message": "Nenhuma transação encontrada"}, 404
            return apresenta_transacoes(transacoes), 200

        except Exception as e:
            logger.error(f"Erro ao buscar transações: {str(e)}")
            return {"message": "Erro inesperado"}, 400

    @app.get('/transacao/', tags=[transacao_tag], responses={"200": TransacaoViewSchema,
                                                                     "404": ErrorSchema.Config.json_schema_extra[
                                                                         "examples"]["404"]["value"]})
    def get_transacao_id(query: TransacaoBuscaSchema):
        """Busca uma transação pelo ID"""

        transacao_descricao = query.descricao
        logger.debug(f"Buscando transação: '{transacao_descricao}'")
        try:
            session = Session()
            transacao = session.query(TransacaoModel).filter(TransacaoModel.descricao == transacao_descricao).first()
            if not transacao:
                return {"message": "Transação não encontrada"}, 404
            return apresenta_transacao(transacao), 200

        except Exception as e:
            logger.error(f"Erro ao buscar transação: {str(e)}")
            return {"message": "Erro inesperado"}, 400
