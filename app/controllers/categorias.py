from app import app, db

from app.models.tables import Categoria

@app.route("/inserir_categoria")
def inserir_categoria():
    categoria = Categoria("Finanças")
    db.session.add(categoria)
    db.session.commit()
    return "Ok"

@app.route("/categorias")
def buscar_categorias():
    categorias = Categoria.query.all()

    print(categorias)

