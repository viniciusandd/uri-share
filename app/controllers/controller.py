from flask import render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, login_manager

from app.models.tables import Perfil, Cidade, Postagem, Categoria
from app.models.forms import LoginForm, PerfilForm, PostagemForm

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
                formulario.tags_digitadas.data,
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
    # if not current_user.is_authenticated:
        # flash("Login não efetuado.")
        # return redirect('login') 

    categorias_id = buscar_categorias_id()
    postagens     = buscar_postagens(categorias_id)
    
    for postagem in postagens:
        print("ID: %s | Cont: %s" % (postagem.id, postagem.conteudo))

    return render_template('home.html', postagens=postagens)

def buscar_categorias_id():
    interesses     = current_user.interesses
    interesses     = interesses.split(",")
    qtd_interesses = len(interesses)
    interesses.pop(qtd_interesses - 1)

    list_categorias_id = []
    for interesse in interesses:
        categoria = Categoria.query.filter_by(descricao=interesse).first()
        if categoria:
            list_categorias_id.append(categoria.id)
            
    tuple_categorias_id = tuple(list_categorias_id)

    return tuple_categorias_id

def buscar_postagens(categorias_id):
    postagens = db.session.query(Postagem).filter(Postagem.categoria_id.in_(categorias_id)).order_by(Postagem.data.desc()).all()
    return postagens

@app.route("/perfil")
@app.route("/perfil/<int:id>")
def perfil(id=None):
    if id:
        perfil = Perfil.query.filter_by(id=id).first()
    else:
        perfil = current_user
    return render_template('perfil.html', perfil=perfil)

@app.route("/nova_postagem", methods=['GET', 'POST'])
def nova_postagem():
    formulario = PostagemForm()
    formulario.categoria_id.choices = [(g.id, g.descricao) for g in Categoria.query.order_by('descricao')]
    if formulario.validate_on_submit():
        postagem = Postagem(
            current_user.id, 
            formulario.categoria_id.data,
            formulario.titulo.data,
            formulario.conteudo.data
        )
        db.session.add(postagem)
        bErro = False
        try:
            db.session.commit()
        except Exception as e:
            bErro = True
            print('Falha ao inserir: % s' % e)
        
        if bErro:
            flash("Falha ao compartilhar a postagem.")
        else:
            flash("Postagem compartilhada com sucesso.")
               
    return render_template('postagem.html', formulario=formulario)