from app import db
import datetime
from app.models.funcoes import Funcoes

# Faltam as classes: Contato, Celular, Telefone e E-mail

class Perfil(db.Model):
    __tablename__ = "perfis"
    id            = db.Column(db.Integer, primary_key=True)
    razao_social  = db.Column(db.String, unique=True, nullable=False)
    nome_fantasia = db.Column(db.String, nullable=False)
    cnpj          = db.Column(db.String(14), unique=True, nullable=False)
    senha         = db.Column(db.String, nullable=False)
    logradouro    = db.Column(db.String, nullable=False)
    complemento   = db.Column(db.String)
    numero        = db.Column(db.String, nullable=False)
    bairro        = db.Column(db.String, nullable=False)
    cep           = db.Column(db.String(8), nullable=False)    
    sobre         = db.Column(db.String, nullable=False)
    interesses    = db.Column(db.String)
    cidade_id     = db.Column(db.Integer, db.ForeignKey('cidades.id'), nullable=False)
    cidade        = db.relationship('Cidade', foreign_keys=cidade_id)
    logo          = db.Column(db.String, nullable=False)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __init__(
            self,
            razao_social,
            nome_fantasia,
            cnpj, senha,
            logradouro,
            complemento,
            numero,
            bairro,
            cep,            
            sobre,
            interesses,
            cidade_id,
            logo
    ):
        self.razao_social  = razao_social
        self.nome_fantasia = nome_fantasia
        self.cnpj          = cnpj
        self.senha         = senha
        self.logradouro    = logradouro
        self.complemento   = complemento
        self.numero        = numero
        self.bairro        = bairro
        self.cep           = cep        
        self.sobre         = sobre
        self.interesses    = interesses
        self.cidade_id     = cidade_id
        self.logo          = logo

    def __repr__(self):
        return "<Perfil %r>" % self.razao_social

class Cidade(db.Model):
    __tablename__ = "cidades"
    id        = db.Column(db.Integer, primary_key=True)
    nome      = db.Column(db.String)
    estado_id = db.Column(db.Integer, db.ForeignKey('estados.id'))
    estado    = db.relationship('Estado', foreign_keys=estado_id)

class Estado(db.Model):
    __tablename__ = "estados"
    id      = db.Column(db.Integer, primary_key=True)
    nome    = db.Column(db.String)
    sigla   = db.Column(db.String(2), unique=True)
    pais_id = db.Column(db.Integer, db.ForeignKey('paises.id'))
    pais    = db.relationship('Pais', foreign_keys=pais_id)

class Pais(db.Model):
    __tablename__ = "paises"
    id    = db.Column(db.Integer, primary_key=True)
    nome  = db.Column(db.String)

class Categoria(db.Model):
    __tablename__ = "categorias"
    id        = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return "<Categoria %r>" % self.descricao    

class Postagem(db.Model):
    __tablename__   = "postagens"
    id              = db.Column(db.Integer, primary_key=True)
    titulo          = db.Column(db.String, nullable=False)
    conteudo        = db.Column(db.String, nullable=False)
    data            = db.Column(db.String, nullable=False)
    hora            = db.Column(db.String, nullable=False)
    media_avaliacao = db.Column(db.Float)
    perfil_id       = db.Column(db.Integer, db.ForeignKey('perfis.id'), nullable=False)
    categoria_id    = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)    
    perfil          = db.relationship('Perfil', foreign_keys=perfil_id)
    categoria       = db.relationship('Categoria', foreign_keys=categoria_id)

    def __init__(self, perfil_id, categoria_id, titulo, conteudo):
        self.perfil_id    = perfil_id
        self.categoria_id = categoria_id
        self.titulo       = titulo
        self.conteudo     = conteudo
        self.data         = Funcoes.retornar_data_atual()
        self.hora         = Funcoes.retornar_hora_atual()

    def calcular_media(self):
        avaliacoes = Avaliacao.query.filter_by(postagem_id=self.id).all()
        qtd_avaliacoes = len(avaliacoes)
        valor_total_avaliacoes = 0
        for avaliacao in avaliacoes:
            valor_total_avaliacoes = valor_total_avaliacoes + avaliacao.nota
        media_avaliacoes = valor_total_avaliacoes / qtd_avaliacoes
        return media_avaliacoes

    def formatar_data(self, tipo):
        # Tipos de formatação
        # 1 - timeline (Jun 01)
        # 2 - brasileiro (01/06/2019)
                        
        data = str(self.data)
        array_data = data.split("-")
        data = datetime.datetime(int(array_data[0]), int(array_data[1]), int(array_data[2]))
        if tipo == 'timeline':            
            return data.strftime("%b %d")
        if tipo == 'brasileiro':
            return data.strftime('%d/%m/%Y')

    def __repr__(self):
        return "<Postagem %r>" % self.titulo

class Avaliacao(db.Model):
    __tablename__ = "avaliacoes"
    id          = db.Column(db.Integer, primary_key=True)
    nota        = db.Column(db.Integer, nullable=False)
    perfil_id   = db.Column(db.Integer, db.ForeignKey('perfis.id'), nullable=False)
    postagem_id = db.Column(db.Integer, db.ForeignKey('postagens.id'), nullable=False)    
    perfil      = db.relationship('Perfil', foreign_keys=perfil_id)
    postagem    = db.relationship('Postagem', foreign_keys=postagem_id)

    def __init__(self, perfil_id, postagem_id, nota):
        self.perfil_id = perfil_id
        self.postagem_id = postagem_id
        self.nota = nota

class Comentario(db.Model):
    __tablename__ = "comentarios"
    id          = db.Column(db.Integer, primary_key=True)
    conteudo    = db.Column(db.String, nullable=False)
    data        = db.Column(db.String, nullable=False)
    hora        = db.Column(db.String, nullable=False)
    perfil_id   = db.Column(db.Integer, db.ForeignKey('perfis.id'), nullable=False)
    postagem_id = db.Column(db.Integer, db.ForeignKey('postagens.id'), nullable=False)    
    perfil      = db.relationship('Perfil', foreign_keys=perfil_id)
    postagem    = db.relationship('Postagem', foreign_keys=postagem_id)

    def __init__(self, perfil_id, postagem_id, conteudo):
        self.perfil_id = perfil_id
        self.postagem_id = postagem_id
        self.conteudo = conteudo
        self.data = Funcoes.retornar_data_atual()
        self.hora = Funcoes.retornar_hora_atual()

    def __repr__(self):
        return "<Comentario %r>" % self.id