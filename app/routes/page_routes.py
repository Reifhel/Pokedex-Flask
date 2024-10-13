from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Pokemon

page_bp = Blueprint('pages', __name__)


@page_bp.route('/')
def index():
    pokemons = Pokemon.query.all()
    return render_template('index.html', pokemons=pokemons)


@page_bp.route('/add_pokemon')
def add_pokemon():
    return render_template('addpokemon.html')


@page_bp.route('/login')
def login():
    return render_template('login.html')


@page_bp.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')
