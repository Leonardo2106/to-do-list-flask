from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.fields.choices import RadioField
from wtforms.fields.datetime import DateField
from wtforms.fields.simple import TextAreaField


class UsuarioForm(FlaskForm):
    nome = StringField('Nome', validators=[validators.DataRequired(), validators.Length(min=1, max=80)])
    nickname = StringField('Nickname', validators=[validators.DataRequired(), validators.Length(min=1, max=20)])
    email = StringField('Email', [validators.DataRequired(), validators.Length(min=1, max=100)])
    senha = PasswordField('Senha', [validators.Optional(), validators.Length(min=1, max=100)])
    confirmar_senha = PasswordField('Confirmar senha', [validators.Optional(), validators.Length(min=1, max=100)])
    criar = SubmitField('Criar')
    login = SubmitField('Login')
    salvar = SubmitField('Salvar')

class TarefaForm(FlaskForm):
    titulo = StringField('Titulo', validators=[validators.DataRequired(), validators.Length(min=1, max=80)])
    tarefa = TextAreaField('Tarefa', [validators.DataRequired(), validators.Length(min=1, max=3000)])
    importante = RadioField('Importante', choices=[('True', 'Sim'), ('False', 'Não')], validators=[validators.DataRequired()])
    prazo = DateField('Prazo', [validators.DataRequired()])
    criar = SubmitField('Criar')
    salvar = SubmitField('Salvar')