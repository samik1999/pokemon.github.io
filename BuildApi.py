from flask import Flask, request, jsonify
import pandas as pd
from threading import Thread
from uuid import uuid4
import os
import json
from PokémonBattleSimulator import *  # Assuming this is your battle simulator logic
from data import *

app = Flask(__name__)

# Load the dataset from the CSV file
file_path = '/Users/samiksha.bidua/Downloads/pokemon.csv'
pokemon_data = pd.read_csv(file_path)

# Database connection parameters
DB_HOST = 'localhost'
DB_NAME = 'your_database_name'
DB_USER = 'your_username'
DB_PASS = 'your_password'

init_db()

@app.route('/pokemon', methods=['GET'])
def list_pokemon():
    try:
        # Get pagination parameters
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))

        # Validate parameters
        if page < 1 or per_page < 1:
            return jsonify({"error": "Page number and items per page must be greater than 0"}), 400

        # Calculate pagination
        start = (page - 1) * per_page
        end = start + per_page

        # Get paginated data
        paginated_pokemon = pokemon_data.iloc[start:end].to_dict(orient='records')

        # Check if data exists for the requested page
        if not paginated_pokemon:
            return jsonify({"error": "No more data available"}), 404

        # Return paginated data
        return jsonify({
            "page": page,
            "per_page": per_page,
            "total": len(pokemon_data),
            "total_pages": (len(pokemon_data) + per_page - 1) // per_page,
            "data": paginated_pokemon
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/battle', methods=['POST'])
def start_battle():
    pokemon_a_name = request.json['pokemon_a']
    pokemon_b_name = request.json['pokemon_b']
    battle_id = str(uuid4())
    
    # Save initial battle status in the database
    save_battle_to_db(battle_id, pokemon_a_name, pokemon_b_name, "BATTLE_INPROGRESS")
    
    def run_battle():
        try:
            result = battle(pokemon_a_name, pokemon_b_name, pokemon_data)
            update_battle_in_db(battle_id, "BATTLE_COMPLETED", result)
        except Exception as e:
            print(str(e))
            update_battle_in_db(battle_id, "BATTLE_FAILED")

    Thread(target=run_battle).start()
    
    return jsonify({"battle_id": battle_id})

@app.route('/battle/<battle_id>', methods=['GET'])
def get_battle_result(battle_id):
    result = get_battle_from_db(battle_id)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
