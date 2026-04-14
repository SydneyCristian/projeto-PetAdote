from flask import Blueprint, request, render_template, redirect
from flask_login import login_required, current_user
from dao.animal_dao import AnimalDao

bp_animal = Blueprint('animal', __name__, url_prefix='/animais')

animal_dao = AnimalDao()


@bp_animal.route('/')
def listar():
    animais = animal_dao.listar()
    return render_template('listar_animais.html', animais=animais)


@bp_animal.route('/cadastrar', methods=['GET', 'POST'])
@login_required
def cadastrar():

    if request.method == 'POST':

        cadastro = animal_dao.cadastrar(
            nome=request.form.get('nome'),
            especie=request.form.get('especie'),
            raca=request.form.get('raca'),
            idade=request.form.get('idade'),
            descricao=request.form.get('descricao'),
            usuario_id=current_user.id
        )

        if cadastro:
            return redirect('/animais')
        else:
            msg=('Erro ao cadastrar animal', 'erro')

    return render_template('cadastrar_animal.html')


@bp_animal.route('/adotar/<int:id>')
@login_required
def adotar(id):

    animal_dao.adotar(id)

    return redirect('/animais')



@bp_animal.route('deletar/<int:id>')
@login_required
def deletar(id):

    animal_dao.deletar(id)

    return redirect('/animais')