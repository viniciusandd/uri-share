from app import db

class Perfil(db.Model):
    __tablename__ = "perfis"
    id            = db.Column(db.Integer, primary_key=True)
    razao_social  = db.Column(db.String, unique=True)
    nome_fantasia = db.Column(db.String)
    cnpj          = db.Column(db.String(14), unique=True)
    senha         = db.Column(db.String)
    logradouro    = db.Column(db.String)
    complemento   = db.Column(db.String)
    numero        = db.Column(db.String)
    bairro        = db.Column(db.String)
    cep           = db.Column(db.String(8))
    logo          = db.Column(db.BLOB)
    cidade_id     = db.Column(db.Integer, db.ForeignKey('cidades.id'))
    estado_id     = db.Column(db.Integer, db.ForeignKey('estados.id'))
    pais_id       = db.Column(db.Integer, db.ForeignKey('paises.id'))
    cidade        = db.relationship('Cidade', foreign_keys=cidade_id)
    estado        = db.relationship('Estado', foreign_keys=estado_id)
    pais          = db.relationship('Pais', foreign_keys=pais_id)

    def __repr__(self):
        return "<Perfil %r>" % self.razao_social

class Cidade(db.Model):
    __tablename__ = "cidades"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String)    

class Estado(db.Model):
    __tablename__ = "estados"
    id    = db.Column(db.Integer, primary_key=True)
    nome  = db.Column(db.String)
    sigla = db.Column(db.String(2), unique=True)

class Postagem(db.Model):
    __tablename__   = "postagens"
    id              = db.Column(db.Integer, primary_key=True)
    perfil_id       = db.Column(db.Integer, db.ForeignKey('perfis.id'))
    categoria_id    = db.Column(db.Integer, db.ForeignKey('categorias.id'))
    conteudo        = db.Column(db.Text)
    data            = db.Column(db.Date)
    hora            = db.Column(db.Time)
    media_avaliacao = db.Column(db.Float)
    perfil          = db.relationship('Perfil', foreign_keys=perfil_id)
    categoria       = db.relationship('Categoria', foreign_keys=categoria_id)

    def __repr__(self):
        return "<Postagem %r>" % self.id

class Categoria(db.Model):
    __tablename__ = "categorias"
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String)

class Comentario(db.Model):
    __tablename__ = "comentarios"
    id          = db.Column(db.Integer, primary_key=True)
    perfil_id   = db.Column(db.Integer)
    postagem_id = db.Column(db.Integer)
    conteudo    = db.Column(db.String)
    data        = db.Column(db.Date)
    hora        = db.Column(db.Time)
    perfil      = db.relationship('Perfil', foreign_keys=perfil_id)
    postagem    = db.relationship('Postagem', foreign_keys=postagem_id)

    def __repr__(self):
        return "<Comentario %r>" % self.id
