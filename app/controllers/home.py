from flask import render_template, flash
from flask_login import login_user
from app import app, db

from app.models.tables import Perfil
from app.models.form import LoginForm

@app.route("/")
def raiz():
    return "Bem vindo ao Share!"

@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    formulario = LoginForm()
    if formulario.validate_on_submit():
        perfil = Perfil.query.filter_by(cnpj=formulario.usuario.data).first()
        if perfil and perfil.senha == formulario.senha.data:
            login_user(perfil)
            flash("Perfil autenticado com sucesso.")
        else:
            flash("Suas credenciais são inválidas.")


    return render_template('login.html', formulario=formulario)