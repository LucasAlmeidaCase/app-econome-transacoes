from urllib.parse import unquote

from flask_openapi3 import Tag
from sqlalchemy.exc import IntegrityError

from database.connection import Session
from model.transacao.enums.tipo_transacao_model import TipoTransacao
from model.transacao.transacao_model import TransacaoModel
from schemas.error.error_schema import ErrorSchema
from schemas.transacao.transacao_schema import TransacaoSchema, apresenta_transacao, apresenta_transacoes, \
    TransacaoViewSchema, ListagemTransacoesSchema, TransacaoBuscaSchema, TransacaoDelSchema, TransacaoAtualizacaoSchema
from pydantic import BaseModel
from utils.logger import logger

transacao_tag = Tag(name="Transações", description="Operações relacionadas as transações")


def config_transacao_routes(app):
    class PedidoIdPathSchema(BaseModel):
        pedido_id: int
    class TransacaoIdPathSchema(BaseModel):
        transacao_id: int

    @app.post('/transacao', tags=[transacao_tag], responses={"200": TransacaoViewSchema,
                                                             "409": ErrorSchema.Config.json_schema_extra["examples"][
                                                                 "409"]["value"],
                                                             "400": ErrorSchema.Config.json_schema_extra["examples"][
                                                                 "400"]["value"]})
    def add_transacao(body: TransacaoSchema):
        """ Adiciona uma nova transação à base de dados

        Retorna uma representação da transação adicionada.
        """
        transacao = TransacaoModel(
            data_vencimento=body.data_vencimento,
            descricao=body.descricao,
            tipo_transacao=TipoTransacao(body.tipo_transacao),
            valor=body.valor,
            pago=body.pago,
            data_pagamento=body.data_pagamento,
            pedido_id=body.pedido_id
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

    @app.get('/transacoes/pedido/<int:pedido_id>', tags=[transacao_tag], responses={"200": TransacaoViewSchema,
                                                                                    "404": ErrorSchema.Config.json_schema_extra[
                                                                                            "examples"]["404"]["value"]})
    def get_transacao_por_pedido(path: PedidoIdPathSchema):
        """Retorna a transação associada a um pedido específico (pedido_id)."""
        session = Session()
        try:
            transacao = session.query(TransacaoModel).filter(TransacaoModel.pedido_id == path.pedido_id).first()
            if not transacao:
                return {"message": "Transação não encontrada"}, 404
            return apresenta_transacao(transacao), 200
        except Exception as e:
            logger.error(f"Erro ao buscar transação por pedido_id={path.pedido_id}: {str(e)}")
            return {"message": "Erro inesperado"}, 400
        finally:
            session.close()

    @app.put('/transacoes/pedido/<int:pedido_id>', tags=[transacao_tag], responses={"200": TransacaoViewSchema,
                                                                                    "404": ErrorSchema.Config.json_schema_extra[
                                                                                        "examples"]["404"]["value"],
                                                                                    "400": ErrorSchema.Config.json_schema_extra[
                                                                                        "examples"]["400"]["value"]})
    def atualizar_transacao_por_pedido(path: PedidoIdPathSchema, body: TransacaoAtualizacaoSchema):
        """Atualiza campos da transação associada a um pedido. Apenas campos enviados serão alterados."""
        session = Session()
        try:
            transacao = session.query(TransacaoModel).filter(TransacaoModel.pedido_id == path.pedido_id).first()
            if not transacao:
                return {"message": "Transação não encontrada"}, 404

            # Atualiza apenas campos presentes (não None)
            if body.descricao is not None:
                transacao.descricao = body.descricao
            if body.tipo_transacao is not None:
                transacao.tipo_transacao = TipoTransacao(body.tipo_transacao)
            if body.valor is not None:
                transacao.valor = body.valor
            if body.data_vencimento is not None:
                transacao.data_vencimento = body.data_vencimento
            if body.pago is not None:
                transacao.pago = body.pago
                # Se marcar como não pago, limpa data_pagamento
                if body.pago is False:
                    transacao.data_pagamento = None
            if body.data_pagamento is not None:
                transacao.data_pagamento = body.data_pagamento

            session.add(transacao)
            session.commit()
            return apresenta_transacao(transacao), 200
        except Exception as e:
            logger.error(f"Erro ao atualizar transação de pedido_id={path.pedido_id}: {str(e)}")
            session.rollback()
            return {"message": "Erro inesperado"}, 400
        finally:
            session.close()

    @app.delete('/transacao', tags=[transacao_tag], responses={"200": TransacaoDelSchema,
                                                               "404": ErrorSchema.Config.json_schema_extra[
                                                                   "examples"]["404"]["value"],
                                                               "400": ErrorSchema.Config.json_schema_extra[
                                                                   "examples"]["400"]["value"]})
    def del_transacao(query: TransacaoBuscaSchema):
        """Deleta uma transação a partir da descrição informada

        Retorna uma mensagem de confirmação da remoção.
        """
        transacao_descricao = unquote(unquote(query.descricao))
        logger.debug(f"Tentando deletar transação: '{transacao_descricao}'")

        try:
            session = Session()
            count = session.query(TransacaoModel).filter(TransacaoModel.descricao == transacao_descricao).delete()
            session.commit()

            if count:
                logger.debug(f"Transação deletada com sucesso: '{transacao_descricao}'")
                return {"message": "Transação removida", "descricao": transacao_descricao}, 200
            else:
                logger.warning(f"Transação não encontrada para exclusão: '{transacao_descricao}'")
                return {"message": "Transação não encontrada"}, 404

        except Exception as e:
            logger.error(f"Erro ao deletar transação '{transacao_descricao}': {str(e)}")
            return {"message": "Erro inesperado ao deletar transação"}, 400

    @app.put('/transacao/<int:transacao_id>', tags=[transacao_tag], responses={"200": TransacaoViewSchema,
                                                                              "404": ErrorSchema.Config.json_schema_extra["examples"]["404"]["value"],
                                                                              "400": ErrorSchema.Config.json_schema_extra["examples"]["400"]["value"]})
    def update_transacao(path: TransacaoIdPathSchema, body: TransacaoSchema):
        """Atualiza uma transação existente pelo ID.

        Campos não enviados serão ignorados (atualização parcial simples).
        """
        transacao_id = path.transacao_id
        logger.debug(f"Atualizando transação id={transacao_id}")
        session = Session()
        try:
            transacao = session.query(TransacaoModel).filter(TransacaoModel.id == transacao_id).first()
            if not transacao:
                return {"message": "Transação não encontrada"}, 404

            if body.descricao is not None:
                transacao.descricao = body.descricao
            if body.tipo_transacao is not None:
                transacao.tipo_transacao = TipoTransacao(body.tipo_transacao)
            if body.valor is not None:
                transacao.valor = body.valor
            if body.pago is not None:
                transacao.pago = body.pago
            if body.data_pagamento is not None or (body.pago is False):
                transacao.data_pagamento = body.data_pagamento
            if body.data_vencimento is not None:
                transacao.data_vencimento = body.data_vencimento
            if body.pedido_id is not None:
                transacao.pedido_id = body.pedido_id

            session.commit()
            session.refresh(transacao)
            return apresenta_transacao(transacao), 200
        except Exception as e:
            logger.error(f"Erro ao atualizar transação id={transacao_id}: {str(e)}")
            session.rollback()
            return {"message": "Erro inesperado ao atualizar transação"}, 400
        finally:
            session.close()
