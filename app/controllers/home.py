from flask import render_template
from app import app

@app.route("/")
def raiz():
    return "Bem vindo ao Share!"

@app.route("/index", defaults={"usuario":None})
@app.route("/index/<usuario>")
def index(usuario):
    return render_template('index.html', usuario=usuario)