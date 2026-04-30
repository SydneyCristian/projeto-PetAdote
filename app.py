from flask import Flask, redirect, url_for
from blueprints.login_usuario import bp_usuario
from blueprints.animal import bp_animal
from blueprints.perfil import bp_perfil
from extensao import bd, login_manager
from models.usuario import Usuario
import models.solicitacao  


def criar_servidor():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/projetoinfoesociedade'
    app.config['SECRET_KEY'] = 'KJHJH3w42#n!'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_ECHO'] = True

    bd.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'login_usuario.login'
    login_manager.login_message = 'Faça login para acessar essa página.'

    @login_manager.user_loader
    def carregar_usuario(usuario_id):
        return bd.session.get(Usuario, int(usuario_id))

    app.register_blueprint(bp_usuario)
    app.register_blueprint(bp_animal)
    app.register_blueprint(bp_perfil)

    @app.route('/')
    def pagina_inicial():
        return redirect(url_for('animal.listar'))

    return app


if __name__ == '__main__':
    app = criar_servidor()
    with app.app_context():
        bd.create_all()
    app.run(debug=True)