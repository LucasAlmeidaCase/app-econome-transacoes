from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from flask_cors import CORS

from utils.logger import logger

info = Info(title="API EconoMe", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Define tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc, RapiDoc, "
                                                "RapiPDF, Scalar ou Elements")

@app.get("/", tags=[home_tag], responses={"200": {"description": "Redireciona para /openapi"}})
def home():
    """Página inicial da API EconoMe. Redireciona para /openapi, tela que permite a escolha do tipo da documentação."""
    try:
        return redirect('/openapi')
    except Exception as e:
        logger.error(f"Erro ao redirecionar para /openapi: {str(e)}")
        return {"message": "Erro inesperado"}, 400

if __name__ == "__main__":
    app.run(debug=True)