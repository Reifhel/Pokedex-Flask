from flask import Blueprint, jsonify, request
from app.models import Pokemon, db

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/pokemons', methods=['GET'])
def get_pokemons():
    pokemons = Pokemon.query.all()
    pokemon_list = [{"ID": p.ID, "NOME": p.NOME, "TIPO_BASE": p.TIPO_BASE, "TIPO_SECUNDARIO": p.TIPO_SEC, "URL_IMAGEM": p.URL_IMAGE}
                    for p in pokemons]
    return jsonify(pokemon_list), 200


@api_bp.route('/pokemons', methods=['POST'])
def create_pokemon():
    data = request.get_json()
    print(data)
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
