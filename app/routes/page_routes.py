from flask import Blueprint, render_template
from app.models import Pokemon

page_bp = Blueprint('pages', __name__)


@page_bp.route('/')
def index():
    pokemons = Pokemon.query.all()
    return render_template('index.html', pokemons=pokemons)


@page_bp.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')


@page_bp.route('/detalhes')
def detalhes():
    return render_template('detalhes.html')
