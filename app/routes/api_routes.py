from flask import Blueprint, jsonify, request
from app.models import Pokemon, db

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/pokemons', methods=['GET'])
def get_pokemons():
    pokemons = Pokemon.query.all()
    pokemon_list = [{"id": p.id, "name": p.name, "type": p.type}
                    for p in pokemons]
    return jsonify(pokemon_list), 200


@api_bp.route('/pokemons', methods=['POST'])
def create_pokemon():
    data = request.get_json()
    name = data.get("name")
    type = data.get("type")

    if not name or not type:
        return jsonify({"error": "Nome e tipo são obrigatórios!"}), 400

    new_pokemon = Pokemon(name=name, type=type)
    db.session.add(new_pokemon)
    db.session.commit()

    return jsonify({"message": f"Pokémon {name} adicionado com sucesso!"}), 201
