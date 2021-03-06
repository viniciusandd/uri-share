import os

from flask import render_template, flash, redirect, url_for, request, jsonify
from sqlalchemy import or_
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, login_manager
from werkzeug.utils import secure_filename
import requests

from app.models.tables import *
from app.models.ranking import Ranking
from app.models.forms import *

@login_manager.user_loader
def load_user(id):
    return Perfil.query.filter_by(id=id).first()

@app.route("/")
def raiz():
    return "Bem vindo ao Share!"

@app.route("/registrar", methods=['GET', 'POST'])
def registrar():
    formulario = RegistrarForm()
    formulario.cidade_id.choices = [(g.id, g.nome) for g in Cidade.query.order_by('nome')]
    if formulario.validate_on_submit():
        retorno_validacao = validar_cnpj(formulario.cnpj.data)
        if retorno_validacao[0]:
            if formulario.senha.data == formulario.senha_confirmar.data:
                filename = secure_filename(formulario.logo.data.filename)
                dot = filename.find('.')
                len_filename = len(filename)
                new_filename = formulario.cnpj.data + filename[dot:]
                formulario.logo.data.save(
                    os.path.join(
                        'app', 'static', 'assets', 'logos', new_filename
                    )
                )

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
                    formulario.sobre.data,
                    formulario.tags_digitadas.data,
                    formulario.cidade_id.data,
                    new_filename
                )
                db.session.add(perfil)
                
                bErro = False
                sMsgErro = ""
                try:
                    db.session.commit()       
                except Exception as e:
                    bErro = True
                    sMsgErro = "Falha ao registrar o perfil, revise suas informações."
                    print("Falha ao commitar a sessão do db")
                
                if bErro:
                    flash(sMsgErro)
                    os.remove(
                        os.path.join(
                            'app', 'static', 'assets', 'logos', new_filename
                        )
                    )
                else:
                    perfil = Perfil.query.filter_by(cnpj=formulario.cnpj.data).first()
                    interesses = perfil.lista_de_interesses()
                    for interesse in interesses:
                        categoria = Categoria.query.filter_by(descricao=interesse).first()
                        if not categoria:
                            sugestao = SugestaoCategoria(perfil.id, interesse, 1)
                            db.session.add(sugestao)

                    db.session.commit()

                    flash("Você foi registrado com sucesso.", "message-success")
                    return redirect(url_for("login"))
            else:
                flash("As senhas digitadas são diferentes.", "message-error")            
        else:
            flash(retorno_validacao[1], "message-error")
    else:
        print(formulario.errors)

    return render_template('registrar.html', formulario=formulario)

def validar_cnpj(cnpj):
    url = "https://www.receitaws.com.br/v1/cnpj/%s" % cnpj
    r = requests.get(url)

    print(r.text)

    # Se o formato não vier em JSON ou seja, 
    # houve uma falha na resposta da receita
    # ele retornará falha de validação
    try:
        resposta = r.json()
    except:
        return (False, "Falha ao estabelecer uma comunicação com a receita federal")

    # Documentos que serão utilizados nos testes
    documentos_testes = [
        "00000000000000",
        "00000000000001",
        "00000000000002",
        "00000000000003",
        "00000000000004",
        "00000000000005",
        "00000000000006",
        "00000000000007"
    ]

    if cnpj in documentos_testes:
        return (True, "O CNPJ informado é utilizado apenas para testes, futuramente será REMOVIDO.")

    # Status retornados pela receita federal: 
    # 1 - OK (operação com sucesso) 
    # 2 - ERROR (cnpj não encontrado ou falha na requisição)
    if resposta["status"] == "ERROR":
        return (False, "O CNPJ informado é inválido.")

    if resposta["situacao"] != "ATIVA":
        return (False, "O CNPJ informado não está com sua situação ATIVA.")

    return (True, "CNPJ válido.")

# Para que o login funcione, é necessário que o campo formulario.csrf_token
# esteja no HTML, sem isso ele não será um formulário válido.
@app.route("/login", methods=['GET', 'POST'])
def login():
    formulario = LoginForm()
    if formulario.validate_on_submit():
        perfil = Perfil.query.filter_by(cnpj=formulario.cnpj.data).first()        
        if perfil:
            perfil_banido = PerfilBanido.query.filter_by(perfil_id=perfil.id).first()
            if not perfil_banido:
                if perfil.senha == formulario.senha.data:
                    login_user(perfil)
                    return redirect(url_for('home'))
                else:
                    flash("Credenciais inválidas.", "message-error")
            else:
                flash(perfil_banido.motivo, "message-error")
        else:
            flash("Seu CNPJ não foi localizado, tente novamente.", "message-error")
    else:
        print(formulario.errors)
        
    return render_template('login.html', formulario=formulario)

@app.route("/logout")
def logout():
    logout_user()
    flash("Logout efetuado com sucesso.", "message-success")
    return redirect(url_for('login'))

@app.route("/home")
def home():    
    categorias_id = buscar_categorias_id()
    postagens     = buscar_postagens(categorias_id)
    postagens_id  = buscar_postagens_id(postagens)
    print(postagens_id)
    comentarios   = buscar_comentarios(postagens_id)    
    print(comentarios)        

    return render_template('home.html', postagens=postagens, comentarios=comentarios)

def buscar_categorias_id():
    interesses = current_user.lista_de_interesses()
    categorias = Categoria.query.all()
    list_categorias_id = []
    for categoria in categorias:
        for interesse in interesses:
            if categoria.descricao.lower() == interesse.lower():
                list_categorias_id.append(categoria.id)
                break

    tuple_categorias_id = tuple(list_categorias_id)
    return tuple_categorias_id

def buscar_postagens(categorias_id):
    postagens = db.session.query(Postagem).filter(or_(Postagem.perfil_id == current_user.id, Postagem.categoria_id.in_(categorias_id))).order_by(Postagem.data.desc(), Postagem.hora.desc()).all()
    return postagens

def buscar_postagens_id(postagens):
    list_postagens_id = []
    for postagem in postagens:
        list_postagens_id.append(postagem.id)
    
    tuple_postagens_id = tuple(list_postagens_id)
    return tuple_postagens_id

def buscar_comentarios(postagens_id):
    # comentarios = db.session.query(Comentario).filter(Comentario.postagem_id.in_(postagens_id)).order_by(Comentario.data.desc(), Comentario.hora.desc(), Comentario.postagem_id).all()
    # return comentarios

    comentarios = {}
    for id in postagens_id:
        comentarios_por_id = Comentario.query.filter_by(postagem_id=id).order_by(Comentario.data.desc(), Comentario.hora.desc()).all()
        comentarios[id] = comentarios_por_id

    return comentarios        

@app.route("/perfil")
@app.route("/perfil/<int:id>")
def perfil(id=None):    
    if id:
        perfil = Perfil.query.filter_by(id=id).first()
    else:
        perfil = current_user

    postagens   = Postagem.query.filter_by(perfil_id=perfil.id).all()    
    comentarios = Comentario.query.filter_by(perfil_id=perfil.id).all()
    avaliacoes  = Avaliacao.query.filter_by(perfil_id=perfil.id).all()

    return render_template(
        'perfil.html', perfil=perfil, postagens=postagens, comentarios=comentarios, avaliacoes=avaliacoes
    )

@app.route("/perfil_editar", methods=['GET', 'POST'])
def perfil_editar():
    perfil = Perfil.query.filter_by(id=current_user.id).first()
    formulario = EditarPerfilForm()
    formulario.cidade_id.choices = [(g.id, g.nome) for g in Cidade.query.order_by('nome')]
    
    if formulario.validate_on_submit():        
        print(formulario.interesses.data)
        perfil.razao_social  = formulario.razao_social.data
        perfil.nome_fantasia = formulario.nome_fantasia.data        
        perfil.cnpj          = formulario.cnpj.data        
        perfil.logradouro    = formulario.logradouro.data        
        perfil.complemento   = formulario.complemento.data        
        perfil.numero        = formulario.numero.data        
        perfil.bairro        = formulario.bairro.data        
        perfil.cep           = formulario.cep.data        
        perfil.sobre         = formulario.sobre.data        
        perfil.interesses    = formulario.tags_digitadas.data        
        perfil.cidade_id     = formulario.cidade_id.data 

        bErro = False
        try:
            db.session.commit()
        except Exception as e:
            bErro = True
            print('Erro ao gravar as atualizações no perfil')

        if bErro:
            flash("Falha ao editar o perfil", "message-error")
        else:
            flash("Perfil atualizado com sucesso", "message-success")

    perfil = Perfil.query.filter_by(id=current_user.id).first()
    formulario.id.data             = perfil.id
    formulario.razao_social.data   = perfil.razao_social
    formulario.nome_fantasia.data  = perfil.nome_fantasia
    formulario.cnpj.data           = perfil.cnpj
    formulario.logradouro.data     = perfil.logradouro
    formulario.complemento.data    = perfil.complemento
    formulario.numero.data         = perfil.numero
    formulario.bairro.data         = perfil.bairro
    formulario.cep.data            = perfil.cep
    formulario.sobre.data          = perfil.sobre
    formulario.tags_digitadas.data = perfil.interesses
    formulario.cidade_id.data      = perfil.cidade_id

    return render_template('perfil_editar.html', formulario=formulario)

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
            # flash("Postagem compartilhada com sucesso.")
            return redirect(url_for('home'))
               
    return render_template('postagem.html', formulario=formulario)

@app.route("/excluir_postagem", methods=['GET'])
def excluir_postagem():
    postagem_id = request.args.get('postagem_id', 0, type=int)
    print(postagem_id)
    postagem = Postagem.query.filter_by(id=postagem_id).first()

    if not postagem:
        return jsonify({'retorno':'Falha ao localizar postagem.'})

    db.session.delete(postagem)
    try:
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "status": 0
            }
        )        
        
    return jsonify(
        {
            'status': 1
        }
    )    

@app.route("/novo_comentario", methods=['GET'])
def novo_comentario():
    postagem_id = request.args.get('postagem_id', 0, type=int)
    conteudo = request.args.get('conteudo', '', type=str)

    comentario  = Comentario(
        current_user.id, postagem_id, conteudo
    )
    db.session.add(comentario)

    print(comentario)

    try:
        db.session.commit()
    except Exception as e:
        return jsonify({"status":0})

    print(comentario)

    return jsonify(
        {
            "status": 1,
            "perfil": {
                "id": current_user.id, 
                "nome_fantasia": current_user.nome_fantasia
            },
            "comentario": comentario.id,
            "conteudo": conteudo
        }
    )

@app.route("/excluir_comentario", methods=['GET'])
def excluir_comentario():
    comentario_id = request.args.get('comentario_id', 0, type=int)
    comentario = Comentario.query.filter_by(id=comentario_id).first()
    if comentario:
        db.session.delete(comentario)
        try:
            db.session.commit()
        except:
            return jsonify({"retorno":0})
        
    return jsonify({"retorno":1})

@app.route("/nova_avaliacao", methods=['GET'])
def nova_avaliacao():
    postagem_id = request.args.get('postagem_id', 0, type=int)
    nota = request.args.get('nota', 0.0, type=float)

    avaliacao = Avaliacao.query.filter_by(perfil_id=current_user.id,postagem_id=postagem_id).first()
    if not avaliacao:
        avaliacao = Avaliacao(current_user.id, postagem_id, nota)
    else:
        avaliacao.nota = nota

    db.session.add(avaliacao)
    db.session.commit()
    atualizar_media_avaliacao_postagem(postagem_id)

    return jsonify({"status":1})

def atualizar_media_avaliacao_postagem(postagem_id):
    postagem = Postagem.query.filter_by(id=postagem_id).first()
    media_avaliacoes = postagem.calcular_media()        
    postagem.media_avaliacao = media_avaliacoes
    db.session.add(postagem)
    db.session.commit()

@app.route("/buscar", methods=['POST'])
def buscar():
    if request.method == 'POST':
        parametro = request.values.get("parametro")
        
        arroba = parametro.find('@')
        if arroba > -1:
            parametro = parametro[arroba+1:]
            print(parametro)
            perfis = Perfil.query.filter_by(nome_fantasia=parametro).all()    
            return render_template('buscas.html', perfis=perfis, postagens=None)

        perfis = Perfil.query.filter(Perfil.razao_social.like("%"+ parametro +"%")).all()
        postagens = Postagem.query.filter(Postagem.titulo.like("%"+ parametro +"%")).all()

        if not postagens:
            perfis_id = []       
            for perfil in perfis:
                perfis_id.append(perfil.id)

            postagens = db.session.query(Postagem).filter(Postagem.perfil_id.in_(tuple(perfis_id))).order_by(Postagem.data.desc(), Postagem.hora.desc()).limit(5).all()

        return render_template('buscas.html', perfis=perfis, postagens=postagens)

@app.route("/nova_sugestao_categoria", methods=['GET','POST'])
def nova_sugestao_categoria():
    formulario = SugestaoCategoriaForm()

    if formulario.validate_on_submit():
        sugestao_categoria = SugestaoCategoria(
            current_user.id,
            formulario.descricao.data,
            1
        )
        db.session.add(sugestao_categoria)
        bErro = False
        try:
            db.session.commit()
        except Exception as e:
            bErro = True
            print('Falha ao inserir sugestão categoria')
        
        if bErro:
            flash("Falha ao inserir sugestão categoria", "message-error")
        else:
            flash("Sugestão de categoria gravada com sucesso", "message-success")
               
    return render_template('sugestao_categoria_nova.html', formulario=formulario)

@app.route("/listar_sugestao_categoria", methods=['GET'])
def listar_sugestao_categoria():
    sugestoes_categorias = SugestaoCategoria.query.filter_by(perfil_id=current_user.id).all()
    return render_template('sugestao_categoria_listar.html', sugestoes_categorias=sugestoes_categorias)

@app.route("/excluir_sugestao_categoria")
def excluir_sugestao_categoria():
    sugestao_categoria_id = request.args.get('sugestao_categoria_id', 0, type=int)    
    sugestao = SugestaoCategoria.query.filter_by(id=sugestao_categoria_id).first()
    if sugestao:    
        db.session.delete(sugestao)
        try:
            db.session.commit()
        except Exception as e:
            return jsonify({"retorno": 0})
            
        return jsonify({'retorno': 1})


@app.route("/ranking")
def ranking():
    postagens = Postagem.query.order_by(Postagem.media_avaliacao.desc()).limit(20).all()
    ranking   = Ranking(postagens)
    podium    = ranking.montar_podium()
    return render_template('ranking.html', postagens=postagens, podium=podium)

@app.route("/listar_categorias")
def listar_categorias():
    categorias = Categoria.query.all()
    return render_template('categorias_listar.html', categorias=categorias)

@app.route("/nova_categoria", methods=['GET', 'POST'])
def nova_categoria():
    formulario = CategoriaForm()

    if formulario.validate_on_submit():
        categoria = Categoria(
            formulario.descricao.data,
        )
        db.session.add(categoria)
        bErro = False
        try:
            db.session.commit()
        except Exception as e:
            bErro = True
            print('Falha ao inserir categoria')
        
        if bErro:
            flash("Falha ao inserir categoria", "message-error")
        else:
            flash("Categoria gravada com sucesso", "message-success")

    sugestoes = SugestaoCategoria.query.filter_by(status=1).all()        
               
    return render_template('categoria_nova.html', formulario=formulario, sugestoes_categorias=sugestoes)

@app.route("/sugestao_categoria_pendente")
def sugestao_categoria_pendente():
    sugestao_categoria_id = request.args.get('sugestao_categoria_id', 0, type=int)
    status = request.args.get('status', 0, type=int)

    sugestao = SugestaoCategoria.query.filter_by(id=sugestao_categoria_id).first()
    if sugestao:
        sugestao.status = status
    
    if sugestao.status == 2:
        categoria = Categoria(sugestao.descricao)
        db.session.add(categoria)
    
    bErro = False
    try:
        db.session.commit()
    except:
        bErro = True

    if bErro:
        return jsonify({"retorno":0})
    
    return jsonify({"retorno":1})

@app.route("/formulario_banir_perfil", methods=['GET'])
def formulario_banir_perfil():
    formulario = BanirPerfilForm()
    lista = [(g.id, g.razao_social) for g in Perfil.query.order_by('razao_social')]
    lista = retirando_perfis(lista)
    formulario.perfil_id.choices = lista
    return render_template('banir_perfil.html', formulario=formulario)

def retirando_perfis(lista):
    nova_lista = []
    for tupla in lista:
        if tupla[0] > 1: # Administrador
            perfil_banido = PerfilBanido.query.filter_by(perfil_id=tupla[0]).first()
            if not perfil_banido:
                nova_lista.append(tupla)
    
    return nova_lista

@app.route("/banir_perfil", methods=['GET'])
def banir_perfil():
    perfil_id = request.args.get('perfil_id', 0, type=int)
    motivo = request.args.get('motivo', '', type=str)

    perfil_banido = PerfilBanido(perfil_id, motivo)
    db.session.add(perfil_banido)

    try:
        db.session.commit()
    except:
        return jsonify({"retorno":0})

    return jsonify({"retorno":1})
