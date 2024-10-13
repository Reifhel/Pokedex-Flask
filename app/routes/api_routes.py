from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from app.models import Pokemon, User, db

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route("/cadastrar_user", methods=['POST'])
def cadastra_user():
    data = request.get_json()
    name = data.get("USER")
    password = data.get("PASSWORD")

    if not name or not password:
        return jsonify({"error": "NOME e PASSWORD são obrigatórios!"}), 400

    new_user = User(USER=name, PASSWORD=password)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": f"Usuário {name} adicionado com sucesso!"}), 201
    except IntegrityError:
        db.session.rollback()  # Reverte a transação se houver erro
        return jsonify({"error": "Usuário já existe!"}), 500
    except Exception as e:
        db.session.rollback()  # Reverte a transação para qualquer outro erro
        return jsonify({"error": f"Ocorreu um erro: {str(e)}"}), 500


@api_bp.route("/login", methods=['POST'])
def login():
    data = request.get_json()
    name = data.get("USER")
    password = data.get("PASSWORD")

    if not name or not password:
        return jsonify({"error": "NOME e PASSWORD são obrigatórios!"}), 400

    user = User.query.filter_by(USER=name).first()

    if user and user.PASSWORD == password:
        return jsonify({"message": "Login bem-sucedido!"}), 200
    else:
        return jsonify({"error": "Nome de usuário ou senha incorretos!"}), 401


@api_bp.route('/users', methods=['GET'])
def users():
    users = User.query.all()
    user_list = [{"ID": p.ID, "USUARIO": p.USER}
                 for p in users]
    return jsonify(user_list), 200


@api_bp.route('/pokemons', methods=['GET'])
def get_pokemons():
    pokemons = Pokemon.query.all()
    pokemon_list = [{"ID": p.ID, "NOME": p.NOME, "TIPO_BASE": p.TIPO_BASE, "TIPO_SECUNDARIO": p.TIPO_SEC, "URL_IMAGEM": p.URL_IMAGE}
                    for p in pokemons]
    return jsonify(pokemon_list), 200


@api_bp.route('/add_pokemons', methods=['POST'])
def create_pokemon():
    data = request.get_json()
    name = data.get("NOME")
    base_type = data.get("TIPO_BASE")
    sec_type = data.get("TIPO_SEC")
    url_image = data.get("URL_IMAGE")

    if not name or not base_type or not url_image:
        return jsonify({"error": "NOME, TIPO_BASE e URL_IMAGE são obrigatórios!"}), 400

    new_pokemon = Pokemon(NOME=name, TIPO_BASE=base_type,
                          TIPO_SEC=sec_type, URL_IMAGE=url_image)
    db.session.add(new_pokemon)
    db.session.commit()

    return jsonify({"message": f"Pokémon {name} adicionado com sucesso!"}), 201
