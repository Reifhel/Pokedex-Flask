from app import db
import sqlalchemy as sa


class User(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    USER = db.Column(db.String(80), unique=True, nullable=False)
    PASSWORD = db.Column(db.String(120), nullable=False)


class Pokemon(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    NOME = db.Column(db.String(120), nullable=False)
    TIPO_BASE = db.Column(db.String(50), nullable=False)
    TIPO_SEC = db.Column(db.String(50), nullable=True)
    URL_IMAGE = db.Column(db.String(500), nullable=False)


class Capturas(db.Model):
    ID_USER = db.Column(db.Integer, sa.ForeignKey(
        'user.ID'), primary_key=True)
    ID_POKEMON = db.Column(db.Integer, sa.ForeignKey(
        'pokemon.ID'), primary_key=True)
