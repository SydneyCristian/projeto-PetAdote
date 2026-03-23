from flask import *
from extensao import bd

def criar_servidor():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postegres:1234@localhost:5432/projetoinfoesociedade'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_ECHO'] = True
    bd.init_app(app)


    @app.route('/')
    def pagina_inicial():
        return render_template('login_loja.html')
    

    return app


if __name__ == '__main__':
    app.run(debug=True)
        