from extensao import bd
from datetime import datetime

class SolicitacaoAdocao(bd.Model):
    __tablename__ = 'solicitacoes_adocao'

    id = bd.Column(bd.Integer, primary_key=True)
    animal_id = bd.Column(bd.Integer, bd.ForeignKey('animais.id'), nullable=False)
    solicitante_id = bd.Column(bd.Integer, bd.ForeignKey('usuarios.id'), nullable=False)
    
    status = bd.Column(bd.String(20), default='pendente', nullable=False)
    
    tem_espaco = bd.Column(bd.Boolean, nullable=False)
    tem_tempo = bd.Column(bd.Boolean, nullable=False)
    tem_condicoes = bd.Column(bd.Boolean, nullable=False)
    mensagem = bd.Column(bd.String(500))
    criado_em = bd.Column(bd.DateTime, default=datetime.utcnow)

    animal      = bd.relationship('Animal',   backref='solicitacoes', lazy=True)
    solicitante = bd.relationship('Usuario',  backref='solicitacoes', lazy=True)

    def __repr__(self):
        return f'<Solicitacao animal={self.animal_id} solicitante={self.solicitante_id} status={self.status}>'