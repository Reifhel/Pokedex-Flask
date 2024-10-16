from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from app.models import Pokemon, User, Capturas, db

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
        return jsonify({"error": "Usuário {name} já existe!"}), 500
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
    pokemon_list = [{"id": p.ID, "nome": p.NOME, "tipo_base": p.TIPO_BASE, "tipo_sec": p.TIPO_SEC, "url_image": p.URL_IMAGE, "capturado": False}
                    for p in pokemons]
    return jsonify(pokemon_list), 200


@api_bp.route('/capturados', methods=['GET'])
def get_all_with_capturados():
    user_name = request.args.get('user')

    # Tenta encontrar o usuário pelo nome
    user = User.query.filter_by(USER=user_name).first()
    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404

    # Obtém IDs dos Pokémons capturados pelo usuário
    capturados_ids = {
        c.ID_POKEMON for c in Capturas.query.filter_by(ID_USER=user.ID)}

    # Busca todos os Pokémons
    all_pokemons = Pokemon.query.all()
    pokemons_data = []

    # Marca cada Pokémon como capturado ou não
    for pokemon in all_pokemons:
        pokemons_data.append({
            "id": pokemon.ID,
            "nome": pokemon.NOME,
            "tipo_base": pokemon.TIPO_BASE,
            "tipo_sec": pokemon.TIPO_SEC,
            "url_image": pokemon.URL_IMAGE,
            "capturado": pokemon.ID in capturados_ids
        })

    return jsonify(pokemons_data)


@api_bp.route('/pesquisar_pokemon', methods=['GET'])
def search_pokemon():
    search = request.args.get('search')

    # Obtém os Pokémons que contem o valor pesquisado pelo usuário no nome
    resultado_pesquisa = [{"id": p.ID, "nome": p.NOME, "tipo_base": p.TIPO_BASE, "tipo_sec": p.TIPO_SEC, "url_image": p.URL_IMAGE, "capturado": False}
                          for p in Pokemon.query.filter(Pokemon.NOME.contains(search))]

    return jsonify(resultado_pesquisa), 201


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


@api_bp.route('/add_captura', methods=['POST'])
def add_captura():
    user_name = request.args.get('user')
    id_pokemon = request.args.get('id_pokemon')

    # Tenta encontrar o usuário pelo nome
    user = User.query.filter_by(USER=user_name).first()
    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404

    # Adicionar nova captura
    nova_captura = Capturas(ID_USER=user.ID, ID_POKEMON=id_pokemon)
    db.session.add(nova_captura)
    db.session.commit()

    return jsonify({"message": "Captura adicionada com sucesso!"}), 201


@api_bp.route('/remove_captura', methods=['DELETE'])
def remove_captura():
    user = request.args.get('user')
    id_pokemon = request.args.get('id_pokemon')

    if not user or not id_pokemon:
        return jsonify({"error": "Usuário e ID do Pokémon são obrigatórios!"}), 400

    # Verificar se o usuário existe
    user_record = User.query.filter_by(USER=user).first()
    if not user_record:
        return jsonify({"error": "Usuário não encontrado!"}), 404

    # Verificar se a captura existe
    captura_existente = Capturas.query.filter_by(
        ID_USER=user_record.ID, ID_POKEMON=id_pokemon).first()
    if not captura_existente:
        return jsonify({"error": "Captura não encontrada!"}), 404

    # Remover a captura
    db.session.delete(captura_existente)
    db.session.commit()

    return jsonify({"message": "Captura removida com sucesso!"}), 200
