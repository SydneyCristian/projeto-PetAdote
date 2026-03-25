from flask import *
from blueprints.login_loja import bp_loja
from extensao import bd

def criar_servidor():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/projetoinfoesociedade'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_ECHO'] = True
    bd.init_app(app)


    app.register_blueprint(bp_loja)
    

    @app.route('/')
    def pagina_inicial():
        return render_template('login_loja.html')
    

    return app


if __name__ == '__main__':
    app = criar_servidor()
    with app.app_context():
        bd.create_all()
    app.run(debug=True)
        