from app import db

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
    logo          = db.Column(db.BLOB)
    sobre         = db.Column(db.String, nullable=False)
    interesses    = db.Column(db.String)
    cidade_id     = db.Column(db.Integer, db.ForeignKey('cidades.id'), nullable=False)
    cidade        = db.relationship('Cidade', foreign_keys=cidade_id)

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
            logo,
            sobre,
            interesses,
            cidade_id
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
        self.logo          = logo
        self.sobre         = sobre
        self.interesses    = interesses
        self.cidade_id     = cidade_id

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
    descricao = db.Column(db.String)

class Interesse(db.Model):
    __tablename__ = "interesses"
    id            = db.Column(db.Integer, primary_key=True)
    perfil_id     = db.Column(db.Integer, db.ForeignKey('perfis.id'), nullable=False)
    categoria_id  = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    perfil        = db.relationship('Perfil', foreign_keys=perfil_id)
    categoria     = db.relationship('Categoria', foreign_keys=categoria_id)

    def __init__(self, perfil_id, categoria_id):
        self.perfil_id    = perfil_id
        self.categoria_id = categoria_id

class Postagem(db.Model):
    __tablename__   = "postagens"
    id              = db.Column(db.Integer, primary_key=True)
    perfil_id       = db.Column(db.Integer, db.ForeignKey('perfis.id'), nullable=False)
    categoria_id    = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    titulo          = db.Column(db.Text, nullable=False)
    conteudo        = db.Column(db.Text, nullable=False)
    data            = db.Column(db.Date, nullable=False)
    hora            = db.Column(db.Time, nullable=False)
    media_avaliacao = db.Column(db.Float)
    perfil          = db.relationship('Perfil', foreign_keys=perfil_id)
    categoria       = db.relationship('Categoria', foreign_keys=categoria_id)

    def __repr__(self):
        return "<Postagem %r>" % self.id

class Avaliacao(db.Model):
    __tablename__ = "avaliacoes"
    id          = db.Column(db.Integer, primary_key=True)
    postagem_id = db.Column(db.Integer, db.ForeignKey('postagens.id'), nullable=False)
    nota        = db.Column(db.Integer, nullable=False)
    postagem    = db.relationship('Postagem', foreign_keys=postagem_id)

# class Comentario(db.Model):
#     __tablename__ = "comentarios"
#     id          = db.Column(db.Integer, primary_key=True)
#     perfil_id   = db.Column(db.Integer)
#     postagem_id = db.Column(db.Integer)
#     conteudo    = db.Column(db.String)
#     data        = db.Column(db.Date)
#     hora        = db.Column(db.Time)
#     perfil      = db.relationship('Perfil', foreign_keys=perfil_id)
#     postagem    = db.relationship('Postagem', foreign_keys=postagem_id)

#     def __repr__(self):
#         return "<Comentario %r>" % self.id