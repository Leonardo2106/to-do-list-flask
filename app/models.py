from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship

from app import db

class Usuarios(db.Model):
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    nome = db.Column(String(80), nullable=False)
    nickname = db.Column(String(20), nullable=False)
    email = db.Column(String(100), nullable=False)
    senha = db.Column(String(100), nullable=False)
    tarefas = relationship('Tarefas', back_populates='usuario')

    def __repr__(self):
        return '<User %r>' % self.nome

class Tarefas(db.Model):
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(String(80), nullable=False)
    tarefa = db.Column(String(3000), nullable=False)
    importante = db.Column(Boolean, nullable=False, default=False)
    data_criacao = db.Column(DateTime, nullable=False, server_default=db.func.now())
    prazo = db.Column(Date)
    usuario_id = db.Column(Integer, ForeignKey('usuarios.id', ondelete='CASCADE'), nullable=False)
    usuario = relationship('Usuarios', back_populates='tarefas')

    def __repr__(self):
        return '<Tarefa %r>' % self.titulo