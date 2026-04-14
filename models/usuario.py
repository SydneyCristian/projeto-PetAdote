from extensao import bd 
from flask_login import UserMixin

class Usuario(bd.Model, UserMixin):
    __tablename__ = 'usuarios'
    id = bd.Column(bd.Integer(), primary_key=True)
    nome = bd.Column(bd.String(100))
    email = bd.Column(bd.String(100), unique=True)
    senha = bd.Column(bd.String(100))
    telefone = bd.Column(bd.String(100))
    
    def __repr__(self):
        return f'<Nome: {self.nome}, Email: {self.email}>'
    
    @property
    def is_usuario(self):
        return True
    
    def get_id(self):
        return f'{self.id}'