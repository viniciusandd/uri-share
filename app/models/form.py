from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    usuario = StringField("usuario", validators=[DataRequired()])
    senha = PasswordField("senha", validators=[DataRequired()])
    lembrar_senha = BooleanField("lembrar_senha")