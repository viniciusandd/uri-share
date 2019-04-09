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

    def __init__(
        self, 
        razao_social,
        nome_fantasia, 
        cnpj,
        senha, 
        logradouro,
        complemento,
        numero,
        bairro,
        cep        
    ):
    self.razao_social = razao_social
    self.nome_fantasia = nome_fantasia
    self.cnpj = cnpj
    self.senha = senha
    self.logradouro = logradouro
    self.complemento = complemento
    self.numero = numero
    self.bairro = bairro
    self.cep = cep

    def __repr__(self):
        return "<Perfil %r>" % self.razao_social

class Postagem(db.Model):
    __tablename__   = "postagens"
    id              = db.Column(db.Integer, primary_key=True)
    perfil_id       = db.Column(db.Integer, db.ForeignKey('perfis.id'))
    conteudo        = db.Column(db.Text)
    data            = db.Column(db.Date)
    hora            = db.Column(db.Time)
    media_avaliacao = db.Column(db.Float)
    perfil          = db.relationship('Perfil', foreign_keys=perfil_id)

    def __init__(self, perfil_id, conteudo, data, hora, media_avaliacao):
        self.perfil_id = perfil_id
        self.conteudo = conteudo
        self.data = data
        self.hora = hora
        self.media_avaliacao = media_avaliacao

    def __repr__(self):
        retun "<Postagem %r>" % self.id        
