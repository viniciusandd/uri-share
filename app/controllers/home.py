from flask import render_template
from app import app

from app.models.form import LoginForm

@app.route("/")
def raiz():
    return "Bem vindo ao Share!"

@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/login")
def login():
    formulario = LoginForm()
    return render_template('login.html', formulario=formulario)
