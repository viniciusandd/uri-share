from flask import render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, login_manager

from app.models.tables import Perfil
from app.models.form import LoginForm

@login_manager.user_loader
def load_user(id):
    return Perfil.query.filter_by(id=id).first()

@app.route("/")
def raiz():
    return "Bem vindo ao Share!"

@app.route("/home")
def index():
    return render_template('home.html')

@app.route("/cadastrar_perfil")
def cadastrar_perfil():
    return 'Cadastrar perfil'

@app.route("/login", methods=['GET', 'POST'])
def login():
    formulario = LoginForm()
    if formulario.validate_on_submit():
        perfil = Perfil.query.filter_by(cnpj=formulario.usuario.data).first()
        if perfil and perfil.senha == formulario.senha.data:
            login_user(perfil)
            flash("Login efetuado com sucesso.")
            return redirect(url_for("home"))
        else:
            flash("Credenciais inválidas.")

    return render_template('login.html', formulario=formulario)

@app.route("/logout")
def logout():
    logout_user()
    flash("Logout efetuado com sucesso.")
    return redirect(url_for("index"))