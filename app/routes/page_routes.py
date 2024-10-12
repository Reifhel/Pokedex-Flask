from flask import Blueprint, render_template

page_bp = Blueprint('pages', __name__)


@page_bp.route('/')
def index():
    return render_template('index.html')


@page_bp.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')


@page_bp.route('/detalhes')
def detalhes():
    return render_template('detalhes.html')
