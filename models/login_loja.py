from extensao import bd

class Loja(bd.Model):
    __tablename__ = 'lojas'
    id = bd.Column(bd.Interger, primary_key=True)
    nome = bd.Column(bd.String)
    email = bd.Column(bd.String, unique=True)
    senha = bd.Column(bd.String)
    telefone = bd.Column(bd.Integer)

    # tipo_usuario
    # localizacao
    # data_cadastro
    
    def __repr__(self):
        return f'<Nome: {self.nome}>'       