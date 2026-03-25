from flask import Blueprint, request, render_template
from dao.login_loja_dao import LojaDao

loja_dao = LojaDao()

bp_loja = Blueprint('login_loja', __name__, url_prefix='/login_loja')


@bp_loja.route('login', methods=['POST'])
def fazer_login_loja():
    login = request.form.get('usuario')
    senha = request.form.get('senha')

    loja_dao.verificar_login(login, senha)

    return 'Deu certo garotinho.'



@bp_loja.route('cadastrar', methods=['POST', 'GET']) # essa rota ainda nao esta pronta
def cadastrar_loja():
    if request.method == 'GET':
        return render_template('cadastrar_loja.html')  #ainda não esta pronto

    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')
    telefone = request.form.get('telefone')
    
    saida = loja_dao.cadastrar_loja(nome, email, senha, telefone)
    if saida:
        return render_template('login_loja.html')
    else:
        return render_template('login_loja.html') # falta colocar a mensagem de erro
    
    