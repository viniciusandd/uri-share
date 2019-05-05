from flask import render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, login_manager

from app.models.tables import Perfil, Cidade
from app.models.form import LoginForm, PerfilForm

@login_manager.user_loader
def load_user(id):
    return Perfil.query.filter_by(id=id).first()

@app.route("/")
def raiz():
    return "Bem vindo ao Share!"

@app.route("/registrar", methods=['GET', 'POST'])
def registrar():
    formulario = PerfilForm()
    formulario.cidade_id.choices = [(g.id, g.nome) for g in Cidade.query.order_by('nome')]
    if formulario.validate_on_submit():
        # print(dict(formulario.cidade_id.choices).get(formulario.cidade_id.data))
        # print(formulario.cidade_id.data)
        print(formulario.sobre.data)
        if formulario.senha.data == formulario.senha_confirmar.data:
            perfil = Perfil(
                formulario.razao_social.data,
                formulario.nome_fantasia.data,
                formulario.cnpj.data,
                formulario.senha.data,
                formulario.logradouro.data,
                formulario.complemento.data,
                formulario.numero.data,
                formulario.bairro.data,
                formulario.cep.data,
                None,
                formulario.sobre.data,
                formulario.cidade_id.data
            )
            db.session.add(perfil)
            bErro = False
            try:
                db.session.commit()
            except Exception as e:
                bErro = True
                print('Falha ao inserir: % s' % e)
            
            if bErro:
                flash("Não foi possível confirmar o registro, preencha os campos corretamente.")
            else:
                flash("Você foi registrado com sucesso.")
                return redirect(url_for("login"))
                
        else:
            flash("As senhas digitadas são diferentes.")
    else:
        print(formulario.errors)

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
            # flash("Login efetuado com sucesso.")
            return redirect(url_for('home'))
        else:
            flash("Credenciais inválidas.")
    else:
        print(formulario.errors)
        
    return render_template('login.html', formulario=formulario)

@app.route("/logout")
def logout():
    logout_user()
    flash("Logout efetuado com sucesso.")
    return redirect(url_for('login'))

@app.route("/home")
def home():
    print(current_user.razao_social)
    return render_template('home.html')

@app.route("/perfil")
def perfil():    
    return render_template('perfil.html', perfil=current_user)