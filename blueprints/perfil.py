from flask import Blueprint, request, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from dao.usuario_dao import UsuarioDao
from dao.animal_dao import AnimalDao
from dao.solicitacao_dao import SolicitacaoDao

bp_perfil = Blueprint('perfil', __name__, url_prefix='/perfil')

usuario_dao    = UsuarioDao()
animal_dao     = AnimalDao()
solicitacao_dao = SolicitacaoDao()




@bp_perfil.route('/')
@login_required
def ver():
    meus_animais      = animal_dao.listar_por_dono(current_user.id)
    minhas_solicitacoes = solicitacao_dao.listar_minhas_solicitacoes(current_user.id)
    pendentes_para_mim  = solicitacao_dao.listar_pendentes_do_dono(current_user.id)
    return render_template(
        'perfil.html',
        meus_animais=meus_animais,
        minhas_solicitacoes=minhas_solicitacoes,
        pendentes_para_mim=pendentes_para_mim
    )


@bp_perfil.route('/editar', methods=['GET', 'POST'])
@login_required
def editar():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        nova_senha = request.form.get('nova_senha')
        confirmar_senha = request.form.get('confirmar_senha')

        
        ok = usuario_dao.atualizar(current_user.id, nome, email, telefone)
        if not ok:
            flash('Não foi possível atualizar os dados. O e-mail pode estar em uso.', 'error')
            return render_template('perfil.html',
                                   meus_animais=animal_dao.listar_por_dono(current_user.id),
                                   minhas_solicitacoes=solicitacao_dao.listar_minhas_solicitacoes(current_user.id),
                                   pendentes_para_mim=solicitacao_dao.listar_pendentes_do_dono(current_user.id))

        
        if nova_senha:
            if nova_senha != confirmar_senha:
                flash('As senhas não coincidem.', 'error')
                return redirect(url_for('perfil.ver'))
            usuario_dao.atualizar_senha(current_user.id, nova_senha)

        flash('Dados atualizados com sucesso!', 'sucesso')
        return redirect(url_for('perfil.ver'))

    return redirect(url_for('perfil.ver'))




@bp_perfil.route('/animal/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_animal(id):
    animal = animal_dao.buscar_por_id(id)
    if not animal or animal.usuario_id != current_user.id:
        abort(403)

    if request.method == 'POST':
        ok = animal_dao.atualizar(
            id=id,
            nome=request.form.get('nome'),
            especie=request.form.get('especie'),
            raca=request.form.get('raca'),
            idade=request.form.get('idade'),
            descricao=request.form.get('descricao')
        )
        if ok:
            flash('Animal atualizado com sucesso!', 'sucesso')
        else:
            flash('Erro ao atualizar animal.', 'error')
        return redirect(url_for('perfil.ver'))

    return render_template('editar_animal.html', animal=animal)


@bp_perfil.route('/animal/excluir/<int:id>', methods=['POST'])
@login_required
def excluir_animal(id):
    animal = animal_dao.buscar_por_id(id)
    if not animal or animal.usuario_id != current_user.id:
        abort(403)
    animal_dao.deletar(id)
    flash('Animal removido.', 'sucesso')
    return redirect(url_for('perfil.ver'))



@bp_perfil.route('/solicitacao/aprovar/<int:id>', methods=['POST'])
@login_required
def aprovar_solicitacao(id):
    ok, msg = solicitacao_dao.aprovar(id, current_user.id)
    flash(msg, 'sucesso' if ok else 'error')
    return redirect(url_for('perfil.ver'))


@bp_perfil.route('/solicitacao/recusar/<int:id>', methods=['POST'])
@login_required
def recusar_solicitacao(id):
    ok, msg = solicitacao_dao.recusar(id, current_user.id)
    flash(msg, 'sucesso' if ok else 'error')
    return redirect(url_for('perfil.ver'))