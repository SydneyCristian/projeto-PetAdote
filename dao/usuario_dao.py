from extensao import bd
from models.usuario import Usuario

class UsuarioDao:
    def __init__(self):
        self.bd = bd


    def verificar_login(self, email, senha):
        return Usuario.query.filter_by(email=email, senha=senha).first()
    

    
    def cadastrar(self, nome, email, senha, telefone):
        usuario = Usuario(nome=nome, email=email, senha=senha, telefone=telefone)
        try:
            self.bd.session.add(usuario)
            self.bd.session.commit()
            return True
        except Exception as e:
            print(e)
            self.bd.session.rollback()
            return False
        

    def listar_usuarios(self):
        return Usuario.query.all()
    

    def buscar_por_id(self, id):
        return bd.session.get(Usuario, id)
    

    def atualizar(self, id, nome, email, telefone):
        usuario = self.buscar_por_id(id)
        if usuario:
            usuario.nome = nome
            usuario.email = email
            usuario.telefone = telefone
            try:
                self.bd.session.commit()
                return True
            except Exception as e:
                print(e)
                self.bd.session.rollback()
        return False

    def atualizar_senha(self, id, nova_senha):
        usuario = self.buscar_por_id(id)
        if usuario:
            try:
                usuario.senha = nova_senha
                self.bd.session.commit()
                return True
            except Exception as e:
                print(e)
                self.bd.session.rollback()
        return False
    
    def deletar(self, id):
        usuario = self.buscar_por_id(id)
        if usuario:
            try:
                self.bd.session.delete(usuario)
                self.bd.session.commit()
                return True
            except Exception as e:
                print(e)
                self.bd.session.rollback()
        return False