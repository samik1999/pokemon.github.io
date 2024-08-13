from flask import Flask, request, jsonify
import pandas as pd
from threading import Thread
from uuid import uuid4
from pydantic import BaseModel, ValidationError
from typing import List, Dict, Any, Optional
from data import Database
from pokémonBattleSimulator import PokemonBattleSimulator

app = Flask(__name__)

file_path = '/Users/samiksha.bidua/Downloads/pokemon.csv'
pokemon_data = pd.read_csv(file_path)

db = Database()
db.init_db()
battle_simulator = PokemonBattleSimulator(pokemon_data)

# Define Pydantic Models for API Endpoints
class PaginatedPokemonResponse(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int
    data: List[Dict[str, Any]]  

class StartBattleRequest(BaseModel):
    pokemon_a: str
    pokemon_b: str

class StartBattleResponse(BaseModel):
    battle_id: str

class BattleResult(BaseModel):
    result: Optional[Dict[str, Any]] 
    status: str
    
class ErrorResponse(BaseModel):
    error: str

# Paginated data 
@app.route('/pokemon', methods=['GET'])
def list_pokemon():
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))

        if page < 1 or per_page < 1:
            error_response = ErrorResponse(error="Page number and items per page must be greater than 0")
            return jsonify(error_response.dict()), 400

        start = (page - 1) * per_page
        end = start + per_page

        paginated_pokemon = pokemon_data.iloc[start:end].to_dict(orient='records')

        if not paginated_pokemon:
            error_response = ErrorResponse(error="No more data available")
            return jsonify(error_response.dict()), 404

        response = PaginatedPokemonResponse(
            page=page,
            per_page=per_page,
            total=len(pokemon_data),
            total_pages=(len(pokemon_data) + per_page - 1) // per_page,
            data=paginated_pokemon
        )
        return jsonify(response.dict())

    except Exception as e:
        error_response = ErrorResponse(error=str(e))
        return jsonify(error_response.dict()), 500

# starting the battle between two pokemons
@app.route('/battle', methods=['POST'])
def start_battle():
    try:
        request_data = StartBattleRequest(**request.json)
        battle_id = str(uuid4())

        db.save_battle_to_db(battle_id, request_data.pokemon_a, request_data.pokemon_b, "BATTLE_INPROGRESS")
        
        def run_battle():
            try:
                result = battle_simulator.battle(request_data.pokemon_a, request_data.pokemon_b)
                db.update_battle_in_db(battle_id, "BATTLE_COMPLETED", result)
            except Exception as e:
                print(str(e))
                db.update_battle_in_db(battle_id, "BATTLE_FAILED")

        Thread(target=run_battle).start()
        
        response = StartBattleResponse(battle_id=battle_id)
        return jsonify(response.model_dump())

    except ValidationError as ve:
        error_response = ErrorResponse(error=str(ve))
        return jsonify(error_response.model_dump()), 400
    except Exception as e:
        error_response = ErrorResponse(error=str(e))
        return jsonify(error_response.model_dump()), 500

# To get the result of battle
@app.route('/battle/<battle_id>', methods=['GET'])
def get_battle_result(battle_id):
    try:
        result = db.get_battle_from_db(battle_id)
        if result is None:
            error_response = ErrorResponse(error="Battle not found")
            return jsonify(error_response.dict()), 404

        response = BattleResult(
            battle_id=battle_id,
            pokemon_a=result.get('pokemon_a'),
            pokemon_b=result.get('pokemon_b'),
            status=result.get('status'),
            result=result.get('result')
        )
        return jsonify(response.model_dump())
    except Exception as e:
        error_response = ErrorResponse(error=str(e))
        return jsonify(error_response.model_dump()), 500

if __name__ == '__main__':
    app.run(debug=True)
