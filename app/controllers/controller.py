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

@app.route("/registrar")
def registrar():
    formulario = PerfilForm()
    return render_template('registrar.html', formulario=formulario)

# Para que o login funcione, é necessário que o campo formulario.csrf_token
# esteja no HTML, sem isso ele não será um formulário válido.
@app.route("/login", methods=['GET', 'POST'])
def login():
    formulario = LoginForm()
    if formulario.validate_on_submit():
        perfil = Perfil.query.filter_by(cnpj=formulario.cnpj.data).first()        
        if perfil and perfil.senha == formulario.senha.data:
            login_user(perfil)
            flash("Login efetuado com sucesso.")
            return redirect(url_for("home"))
        else:
            flash("Credenciais inválidas.")
    else:
        print(formulario.errors)
        
    return render_template('login.html', formulario=formulario)

@app.route("/logout")
def logout():
    logout_user()
    flash("Logout efetuado com sucesso.")
    return redirect(url_for("index"))

@app.route("/home")
def index():
    return render_template('home.html')