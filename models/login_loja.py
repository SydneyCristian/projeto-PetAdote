from extensao import bd

class Loja(bd.Model):
    __tablename__ = 'lojas'
    id = bd.Column(bd.Integer, primary_key=True)
    nome = bd.Column(bd.String(100))
    email = bd.Column(bd.String(100), unique=True)
    senha = bd.Column(bd.String(100))
    telefone = bd.Column(bd.String(100))

    # tipo_usuario
    # localizacao
    # data_cadastro
    
    def __repr__(self):
        return f'<Nome: {self.nome}>'          