from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Importa e registra as blueprints para separar as rotas
    from app.routes.api_routes import api_bp
    from app.routes.page_routes import page_bp
    app.register_blueprint(api_bp)
    app.register_blueprint(page_bp)

    with app.app_context():
        db.create_all()

    return app
