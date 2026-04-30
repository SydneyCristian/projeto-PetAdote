from extensao import bd
from models.solicitacao import SolicitacaoAdocao
from models.animal import Animal


class SolicitacaoDao:
    def __init__(self):
        self.bd = bd

    def criar(self, animal_id, solicitante_id, tem_espaco, tem_tempo, tem_condicoes, mensagem):
        existente = SolicitacaoAdocao.query.filter_by(
            animal_id=animal_id,
            solicitante_id=solicitante_id,
            status='pendente'
        ).first()
        if existente:
            return False, 'Você já tem uma solicitação pendente para este animal.'

        s = SolicitacaoAdocao(
            animal_id=animal_id,
            solicitante_id=solicitante_id,
            tem_espaco=tem_espaco,
            tem_tempo=tem_tempo,
            tem_condicoes=tem_condicoes,
            mensagem=mensagem
        )
        try:
            self.bd.session.add(s)
            self.bd.session.commit()
            return True, 'Solicitação enviada! O responsável pelo animal entrará em contato.'
        except Exception as e:
            print(e)
            self.bd.session.rollback()
            return False, 'Erro ao enviar solicitação.'

    def listar_por_animal(self, animal_id):
        return SolicitacaoAdocao.query.filter_by(animal_id=animal_id).order_by(
            SolicitacaoAdocao.criado_em.desc()
        ).all()

    def listar_pendentes_do_dono(self, usuario_id): 
        return (
            SolicitacaoAdocao.query
            .join(Animal)
            .filter(Animal.usuario_id == usuario_id, SolicitacaoAdocao.status == 'pendente')
            .order_by(SolicitacaoAdocao.criado_em.desc())
            .all()
        )

    def listar_minhas_solicitacoes(self, solicitante_id):
        return SolicitacaoAdocao.query.filter_by(solicitante_id=solicitante_id).order_by(
            SolicitacaoAdocao.criado_em.desc()
        ).all()

    def buscar_por_id(self, id):
        return bd.session.get(SolicitacaoAdocao, id)

    def aprovar(self, solicitacao_id, dono_id):
        s = self.buscar_por_id(solicitacao_id)
        if not s or s.animal.usuario_id != dono_id:
            return False, 'Ação não permitida.'
        try:
            s.status = 'aprovado'
            s.animal.status = 'adotado'
            
            outras = SolicitacaoAdocao.query.filter(
                SolicitacaoAdocao.animal_id == s.animal_id,
                SolicitacaoAdocao.id != s.id,
                SolicitacaoAdocao.status == 'pendente'
            ).all()
            for o in outras:
                o.status = 'recusado'
            self.bd.session.commit()
            return True, f'Adoção de {s.animal.nome} aprovada!'
        except Exception as e:
            print(e)
            self.bd.session.rollback()
            return False, 'Erro ao aprovar.'

    def recusar(self, solicitacao_id, dono_id):
        s = self.buscar_por_id(solicitacao_id)
        if not s or s.animal.usuario_id != dono_id:
            return False, 'Ação não permitida.'
        try:
            s.status = 'recusado'
            self.bd.session.commit()
            return True, 'Solicitação recusada.'
        except Exception as e:
            print(e)
            self.bd.session.rollback()
            return False, 'Erro ao recusar.'