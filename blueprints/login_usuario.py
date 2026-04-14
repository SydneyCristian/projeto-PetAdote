from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user


from dao.usuario_dao import UsuarioDao

usuario_dao = UsuarioDao()  

bp_usuario = Blueprint('login_usuario', __name__, url_prefix='/login_usuario')


@bp_usuario.route('/login', methods=['POST', 'GET'])  
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        usuario = usuario_dao.verificar_login(email, senha)

        if not usuario:
            flash('Usuário não encontrado! Faça cadastro no PetAdote.', 'error')
            return redirect(url_for('login_usuario.login')) 

        login_user(usuario)
        return redirect(url_for('animal.listar')) 

    return render_template('login_usuario.html')


@bp_usuario.route('/cadastrar', methods=['POST', 'GET'])  
def cadastrar():
    if request.method == 'GET':
        return render_template('cadastrar_usuario.html')

    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')
    telefone = request.form.get('telefone')

    saida = usuario_dao.cadastrar_usuario(nome, email, senha, telefone)
    if saida:
        flash('Conta criada com sucesso! Faça login para continuar.', 'success')
        return redirect(url_for('login_usuario.login'))  
    else:
        flash('Não foi possível criar a conta. O e-mail pode já estar em uso.', 'error')
        return render_template('cadastrar_usuario.html')


@bp_usuario.route('/menu_principal')
@login_required  
def menu_principal():
     print('Usuario logado', current_user.nome)
     return render_template('menu_principal.html')
    


@bp_usuario.route('/logout')
def logout():
    logout_user()
    return redirect('/login_usuario/login')