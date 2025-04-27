from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv

# ler o .env
load_dotenv()

# iniciando o flask
app = Flask(__name__)
app.config.from_pyfile('../config.py')

db = SQLAlchemy(app)
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app) # criptografar a senha no banco de dados

from app import routes

