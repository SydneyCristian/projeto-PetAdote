from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from dao.animal_dao import AnimalDao
from dao.solicitacao_dao import SolicitacaoDao

bp_animal = Blueprint('animal', __name__, url_prefix='/animais')

animal_dao      = AnimalDao()
solicitacao_dao = SolicitacaoDao()


@bp_animal.route('/')
def listar():
    busca         = request.args.get('q', '').strip()
    filtro_status = request.args.get('status', 'disponivel')

    todos = animal_dao.listar_animais()

    if filtro_status == 'adotado':
        animais = [a for a in todos if a.status == 'adotado']
    else:
        animais = [a for a in todos if a.status == 'disponivel']

    if busca:
        animais = [
            a for a in animais
            if busca.lower() in (a.nome or '').lower()
            or busca.lower() in (a.especie or '').lower()
        ]

    qtd_disponiveis = sum(1 for a in todos if a.status == 'disponivel')
    qtd_adotados    = sum(1 for a in todos if a.status == 'adotado')

    return render_template(
        'listar_animais.html',
        animais=animais,
        busca=busca,
        filtro_status=filtro_status,
        qtd_disponiveis=qtd_disponiveis,
        qtd_adotados=qtd_adotados
    )


@bp_animal.route('/cadastrar', methods=['GET', 'POST'])
@login_required
def cadastrar():
    if request.method == 'POST':
        ok = animal_dao.cadastrar(
            nome=request.form.get('nome'),
            especie=request.form.get('especie'),
            raca=request.form.get('raca'),
            idade=request.form.get('idade'),
            descricao=request.form.get('descricao'),
            usuario_id=current_user.id
        )
        if ok:
            flash('Animal cadastrado com sucesso!', 'sucesso')
            return redirect(url_for('animal.listar'))
        flash('Erro ao cadastrar animal.', 'error')

    return render_template('cadastrar_animal.html')


@bp_animal.route('/solicitar/<int:id>', methods=['GET', 'POST'])
@login_required
def solicitar_adocao(id):
    animal = animal_dao.buscar_por_id(id)
    if not animal or animal.status != 'disponivel':
        flash('Animal não disponível para adoção.', 'error')
        return redirect(url_for('animal.listar'))

    if animal.usuario_id == current_user.id:
        flash('Você não pode solicitar a adoção do seu próprio animal.', 'error')
        return redirect(url_for('animal.listar'))

    if request.method == 'POST':
        tem_espaco    = request.form.get('tem_espaco') == 'sim'
        tem_tempo     = request.form.get('tem_tempo') == 'sim'
        tem_condicoes = request.form.get('tem_condicoes') == 'sim'
        mensagem      = request.form.get('mensagem', '')

        ok, msg = solicitacao_dao.criar(
            animal_id=id,
            solicitante_id=current_user.id,
            tem_espaco=tem_espaco,
            tem_tempo=tem_tempo,
            tem_condicoes=tem_condicoes,
            mensagem=mensagem
        )
        flash(msg, 'sucesso' if ok else 'error')
        return redirect(url_for('animal.listar'))

    return render_template('solicitar_adocao.html', animal=animal)


@bp_animal.route('/deletar/<int:id>', methods=['POST'])
@login_required
def deletar(id):
    animal_dao.deletar(id)
    flash('Animal removido.', 'sucesso')
    return redirect(url_for('animal.listar'))