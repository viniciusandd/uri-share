import os.path
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

# Passando o caminho absoluto do banco de dados
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database/storage.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True

SECRET_KEY = 'chave-secreta-da-aplicacao'