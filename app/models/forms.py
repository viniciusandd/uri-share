from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, FileField, SelectField, TextAreaField, HiddenField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    cnpj          = StringField("cnpj", validators=[DataRequired()])
    senha         = PasswordField("senha", validators=[DataRequired()])
    lembrar_senha = BooleanField("lembrar_senha")

class PerfilForm(FlaskForm):
    razao_social    = StringField("razao_social", validators=[DataRequired()])
    nome_fantasia   = StringField("nome_fantasia", validators=[DataRequired()])
    cnpj            = StringField("cnpj", validators=[DataRequired()])
    senha           = PasswordField("senha", validators=[DataRequired()])
    senha_confirmar = PasswordField("senha_confirmar", validators=[DataRequired()])
    logradouro      = StringField("logradouro", validators=[DataRequired()])
    complemento     = StringField("complemento")
    numero          = StringField("numero", validators=[DataRequired()])
    bairro          = StringField("bairro", validators=[DataRequired()])
    cep             = StringField("cep", validators=[DataRequired()])
    logo            = FileField("logo")
    sobre           = TextAreaField("sobre", validators=[DataRequired()])
    interesses      = StringField("interesses")
    tags_digitadas  = HiddenField("tags_digitadas")
    cidade_id       = SelectField("cidade", coerce=int)

class PostagemForm(FlaskForm):
    titulo       = StringField("titulo", validators=[DataRequired()])
    conteudo     = TextAreaField("conteudo", validators=[DataRequired()])
    categoria_id = SelectField("categoria", coerce=int)