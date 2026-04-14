from extensao import bd
from flask_login import UserMixin

class Animal(bd.Model, UserMixin):
    __tablename__ = 'animais'
    id = bd.Column(bd.Integer(), primary_key = True)
    nome = bd.Column(bd.String(255))
    especie = bd.Column(bd.String(255))
    raca = bd.Column(bd.String(255))
    idade = bd.Column(bd.Integer())
    descricao =bd.Column(bd.String(255)) 
    status = bd.Column(bd.String(20), default='disponivel')

    usuario_id = bd.Column(bd.Integer(), bd.ForeignKey('usuarios.id'))