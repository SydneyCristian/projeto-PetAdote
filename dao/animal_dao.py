from extensao import bd
from models.animal import Animal

class AnimalDao:
    def __init__(self):
        self.bd = bd




    def cadastrar(self, nome, especie, raca, idade, descricao, usuario_id):
        animal = Animal(
            nome=nome,
            especie=especie,
            raca=raca,
            idade=idade,
            descricao=descricao,
            usuario_id=usuario_id
        )

        try:
            self.bd.session.add(animal)
            self.bd.session.commit()
            return True
        except Exception as e:
            print(e)
            self.bd.session.rollback()
            return False    
    
    def listar(self):
        return Animal.query.filter_by(status='disponivel').all()


    def adotar(self, id):
        animal = Animal.query.get(id)

        if animal:
            animal.status = 'adotado'
            bd.session.commit()
            return True
        
        return False
    
    def listar_animais(self):
        return Animal.query.all()
    

    def buscar_por_id(self):
        return Animal.query.get(id)
    

    def deletar(self, id):
        animal = self.buscar_por_id(id)
        if animal:
            try:
                self.bd.session.delete(animal)
                self.bd.session.commit()
                return True
            except Exception as e:
                print(e)
                self.bd.session.rollback()
        return False
