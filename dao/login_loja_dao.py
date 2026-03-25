from extensao import bd
from models.login_loja import Loja

class LojaDao:
    def __init__(self):
        self.bd = bd


    def verificar_login(self, email_loja, senha_loja):
        return Loja.query.filter_by(email=email_loja, senha=senha_loja).first()
    

    
    def cadastrar_loja(self, nome, email, senha, telefone):
        loja = Loja(nome=nome, email=email, senha=senha, telefone=telefone)
        try:
            self.bd.session.add(loja)
            self.bd.session.commit()
            return True
        except Exception as e:
            self.bd.session.rollback()
            return False