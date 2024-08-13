import unittest
import pandas as pd
from flask import jsonify
from pokémonBattleSimulator import PokemonBattleSimulator
from BuildApi import app
import json

# Sample Pokémon data for testing
sample_data = pd.DataFrame({
    'name': ['Pikachu', 'Bulbasaur', 'Charmander', 'Squirtle'],
    'type1': ['electric', 'grass', 'fire', 'water'],
    'type2': [None, 'poison', None, None],
    'attack': [55, 49, 52, 48],
    'against_electric': [1.0, 0.5, 1.0, 1.0],
    'against_grass': [1.0, 0.25, 2.0, 0.5],
    'against_fire': [1.0, 2.0, 0.5, 2.0],
    'against_water': [2.0, 2.0, 0.5, 1.0],
    'against_poison': [1.0, 1.0, 1.0, 1.0]
})

# ANSI escape sequences for bold text
BOLD = "\033[1m"
RESET = "\033[0m"

class TestPokemonBattleSimulator(unittest.TestCase):

    def setUp(self):
        self.simulator = PokemonBattleSimulator(sample_data)

    def test_normalize_name(self):
        print(f"{BOLD}Running test: test_normalize_name{RESET}")
        print(f"{BOLD}Description:{RESET} Test the normalization of Pokémon names by removing extra spaces and converting to lowercase.")
        print(f"{BOLD}Test Steps:{RESET} \n1. Call the normalize_name method with ' Pikachu '. \n2. Call the normalize_name method with 'Bulbasaur'.")
        print(f"{BOLD}Test Data:{RESET} Input: ' Pikachu ', 'Bulbasaur'")
        self.assertEqual(self.simulator.normalize_name(' Pikachu '), 'pikachu')
        self.assertEqual(self.simulator.normalize_name('Bulbasaur'), 'bulbasaur')
        
        print(f"{BOLD}Expected Result:{RESET} Result From Code should be 'pikachu' and 'bulbasaur'.")
        print("Result From Code: Normalization tests passed\n\n")

    def test_find_pokemon_by_name_exact(self):
        print(f"{BOLD}Running test: test_find_pokemon_by_name_exact{RESET}")
        print(f"{BOLD}Description:{RESET} Verify that the exact name of a Pokémon returns the correct Pokémon data.")
        print(f"{BOLD}Test Steps:{RESET} \n1. Call find_pokemon_by_name with 'Pikachu'.")
        print(f"{BOLD}Test Data:{RESET} Input: 'Pikachu'")
        
        pokemon = self.simulator.find_pokemon_by_name('Pikachu')
        self.assertEqual(pokemon['name'].values[0], 'Pikachu')
        
        print(f"{BOLD}Expected Result:{RESET} Result From Code should return Pokémon data for 'Pikachu'.")
        print("Result From Code: Found Pokémon - Pikachu\n\n")

    def test_find_pokemon_by_name_close_match(self):
        print(f"{BOLD}Running test: test_find_pokemon_by_name_close_match{RESET}")
        print(f"{BOLD}Description:{RESET} Verify that a close spelling match for a Pokémon returns the correct Pokémon data.")
        print(f"{BOLD}Test Steps:{RESET} \n1. Call find_pokemon_by_name with 'Pikachoo'.")
        print(f"{BOLD}Test Data:{RESET} Input: 'Pikachoo'")
        
        pokemon = self.simulator.find_pokemon_by_name('Pikachoo')
        self.assertEqual(pokemon['name'].values[0], 'Pikachu')
        print(f"{BOLD}Expected Result:{RESET} Result From Code should return Pokémon data for 'Pikachu'.")
        print("Result From Code: Found close match for 'Pikachoo' - Pikachu\n\n")

    def test_find_pokemon_by_name_not_found(self):
        print(f"{BOLD}Running test: test_find_pokemon_by_name_not_found{RESET}")
        print(f"{BOLD}Description:{RESET} Verify that an unknown Pokémon name raises a ValueError.")
        print(f"{BOLD}Test Steps:{RESET} \n1. Call find_pokemon_by_name with 'Unknown'.")
        
        print(f"{BOLD}Test Data:{RESET} Input: 'Unknown'")
        
        with self.assertRaises(ValueError):
            self.simulator.find_pokemon_by_name('Unknown')

        print(f"{BOLD}Expected Result:{RESET} A ValueError should be raised indicating the Pokémon is not found.")
        print("Result From Code: Pokémon not found as expected\n\n")

    def test_find_two_pokemons(self):
        print(f"{BOLD}Running test: test_find_two_pokemons{RESET}")
        print(f"{BOLD}Description:{RESET} Verify that finding two Pokémon by name returns the correct Pokémon data.")
        print(f"{BOLD}Test Steps:{RESET} \n1. Call find_two_pokemons with 'Pikachu' and 'Bulbasaur'.")
        print(f"{BOLD}Test Data:{RESET} Input: 'Pikachu', 'Bulbasaur'")
        
        pokemon_a, pokemon_b = self.simulator.find_two_pokemons('Pikachu', 'Bulbasaur')
        self.assertEqual(pokemon_a['name'].values[0], 'Pikachu')
        self.assertEqual(pokemon_b['name'].values[0], 'Bulbasaur')
        
        print(f"{BOLD}Expected Result:{RESET} Result From Code should return Pokémon data for 'Pikachu' and 'Bulbasaur'.")
        print("Result From Code: Found two Pokémon - Pikachu and Bulbasaur\n\n")

    def test_calculate_damage_single_type(self):
        print(f"{BOLD}Running test: test_calculate_damage_single_type{RESET}")
        print(f"{BOLD}Description:{RESET} Verify that damage calculation works for single-type Pokémon.")
        print(f"{BOLD}Test Steps:{RESET} \n1. Call calculate_damage with 'Pikachu' as attacker and 'Squirtle' as defender.")
        print(f"{BOLD}Test Data:{RESET} Attacker: 'Pikachu', Defender: 'Squirtle'")
        
        attacker = self.simulator.find_pokemon_by_name('Pikachu')
        defender = self.simulator.find_pokemon_by_name('Squirtle')
        damage = self.simulator.calculate_damage(attacker, defender)
        
        self.assertGreaterEqual(damage, 0) 
        print(f"{BOLD}Expected Result:{RESET} Damage should be a non-negative value.")
        print(f"Result From Code: Damage calculated - {damage}\n\n")

    def test_calculate_damage_dual_type(self):
        print(f"{BOLD}Running test: test_calculate_damage_dual_type{RESET}")
        print(f"{BOLD}Description:{RESET} Verify that damage calculation works for dual-type Pokémon.")
        print(f"{BOLD}Test Steps:{RESET} \n1. Call calculate_damage with 'Bulbasaur' as attacker and 'Squirtle' as defender.")
        print(f"{BOLD}Test Data:{RESET} Attacker: 'Bulbasaur', Defender: 'Squirtle'")
        
        attacker = self.simulator.find_pokemon_by_name('Bulbasaur')
        defender = self.simulator.find_pokemon_by_name('Squirtle')
        damage = self.simulator.calculate_damage(attacker, defender)
        
        self.assertGreaterEqual(damage, 0)  
        print(f"{BOLD}Expected Result:{RESET} Damage should be a non-negative value.")
        print(f"Result From Code: Damage calculated - {damage}\n\n")

    def test_calculate_damage_invalid_type(self):
        print(f"{BOLD}Running test: test_calculate_damage_invalid_type{RESET}")
        print(f"{BOLD}Description:{RESET} Verify that damage calculation raises an error for invalid Pokémon types.")
        print(f"{BOLD}Test Steps:{RESET} \n1. Create an invalid attacker Pokémon and call calculate_damage with it.")
        
    
        print(f"{BOLD}Test Data:{RESET} Attacker: Invalid Pokémon, Defender: 'Pikachu'")
        
        attacker = pd.DataFrame({
            'name': ['InvalidPokemon'],
            'type1': ['ghost'],
            'type2': [None],
            'attack': [50]
        })
        defender = self.simulator.find_pokemon_by_name('Pikachu')
        
        with self.assertRaises(ValueError):
            self.simulator.calculate_damage(attacker, defender)
        print(f"{BOLD}Expected Result:{RESET} A ValueError should be raised indicating an invalid type.")
        print("Result From Code: Invalid type error raised as expected\n\n")

    def test_battle_charmander_vs_bulbasaur(self):
        print(f"{BOLD}Running test: test_battle_charmander_vs_bulbasaur{RESET}")
        print(f"{BOLD}Description:{RESET} Verify that Bulbasaur wins against Charmander in battle.")
        print(f"{BOLD}Test Steps:{RESET} \n1. Call battle method with 'Bulbasaur' and 'Charmander'.")
        print(f"{BOLD}Test Data:{RESET} Attacker: 'Bulbasaur', Defender: 'Charmander'")
        
        result = self.simulator.battle('Bulbasaur', 'Charmander')
        self.assertEqual(result['winner'], 'Bulbasaur') 
        print(f"{BOLD}Expected Result:{RESET} Result From Code should indicate that 'Bulbasaur' is the winner.")
        print("Result From Code: Battle result - Winner: Bulbasaur\n\n")

    def test_battle_squirtle_vs_bulbasaur(self):
        print(f"{BOLD}Running test: test_battle_squirtle_vs_bulbasaur{RESET}")
        print(f"{BOLD}Description:{RESET} Verify that Squirtle wins against Bulbasaur in battle.")
        print(f"{BOLD}Test Steps:{RESET} \n1. Call battle method with 'Bulbasaur' and 'Squirtle'.")
        print(f"{BOLD}Test Data:{RESET} Attacker: 'Bulbasaur', Defender: 'Squirtle'")
        
        result = self.simulator.battle('Bulbasaur', 'Squirtle')
        self.assertEqual(result['winner'], 'Squirtle')  
        print(f"{BOLD}Expected Result:{RESET} Result From Code should indicate that 'Squirtle' is the winner.")
        print("Result From Code: Battle result - Winner: Squirtle\n\n")

    def test_battle_pikachu_vs_charmander(self):
        print(f"{BOLD}Running test: test_battle_pikachu_vs_charmander{RESET}")
        print(f"{BOLD}Description:{RESET} Verify that Charmander wins against Pikachu in battle.")
        print(f"{BOLD}Test Steps:{RESET} \n1. Call battle method with 'Pikachu' and 'Charmander'.")
        print(f"{BOLD}Test Data:{RESET} Attacker: 'Pikachu', Defender: 'Charmander'")
        
        result = self.simulator.battle('Pikachu', 'Charmander')
        self.assertEqual(result['winner'], 'Charmander')  
        print(f"{BOLD}Expected Result:{RESET} Result From Code should indicate that 'Charmander' is the winner.")
        print("Result From Code: Battle result - Winner: Charmander\n\n")

    def test_battle_draw(self):
        print(f"{BOLD}Running test: test_battle_draw{RESET}")
        
    
        print(f"{BOLD}Description:{RESET} Verify that a battle between the same Pokémon results in a draw.")
        print(f"{BOLD}Test Steps:{RESET} \n1. Call battle method with 'Bulbasaur' and 'Bulbasaur'.")
        print(f"{BOLD}Test Data:{RESET} Attacker: 'Bulbasaur', Defender: 'Bulbasaur'")
        
        result = self.simulator.battle('Bulbasaur', 'Bulbasaur')
        self.assertEqual(result['winner'], 'Draw')
        print(f"{BOLD}Expected Result:{RESET} Result From Code should indicate a draw.")
        print("Result From Code: Battle result - Winner: Draw\n\n")


class TestPokemonAPIs(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_list_pokemon(self):
        print(f"{BOLD}Running test: test_list_pokemon{RESET}")
        print(f"{BOLD}Description:{RESET} Verify that the Pokémon list API returns the correct number of Pokémon.")
        print(f"{BOLD}Test Steps:{RESET} \n1. Send a GET request to '/pokemon?page=1&per_page=2'.")
        print(f"{BOLD}Test Data:{RESET} Request: '/pokemon?page=1&per_page=2'")
        
        response = self.app.get('/pokemon?page=1&per_page=2')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        print(data)
        self.assertIn('data', data)
        self.assertEqual(len(data['data']), 2) 
        print(f"{BOLD}Expected Result:{RESET} The response should contain a 'data' key with 2 Pokémon.")
        print("Result From Code: Pokémon list retrieved successfully\n\n")

    def test_list_pokemon_invalid_page(self):
        print(f"{BOLD}Running test: test_list_pokemon_invalid_page{RESET}")
        print(f"{BOLD}Description:{RESET} Verify that requesting an invalid page number returns a 400 error.")
        print(f"{BOLD}Test Steps:{RESET} \n1. Send a GET request to '/pokemon?page=0&per_page=10'.")
        print(f"{BOLD}Test Data:{RESET} Request: '/pokemon?page=0&per_page=10'")
        
        response = self.app.get('/pokemon?page=0&per_page=10')
        self.assertEqual(response.status_code, 400)
        
        data = json.loads(response.data)
        self.assertEqual(data['error'], "Page number and items per page must be greater than 0")
        print(f"{BOLD}Expected Result:{RESET} The response should return a 400 error with an appropriate message.")
        print("Result From Code: Invalid page number error returned as expected\n\n")

    def test_list_pokemon_no_data(self):
        print(f"{BOLD}Running test: test_list_pokemon_no_data{RESET}")
        print(f"{BOLD}Description:{RESET} Verify that requesting a page out of range returns a 404 error.")
        print(f"{BOLD}Test Steps:{RESET} \n1. Send a GET request to '/pokemon?page=100&per_page=10'.")
        print(f"{BOLD}Test Data:{RESET} Request: '/pokemon?page=100&per_page=10'")
        
        response = self.app.get('/pokemon?page=100&per_page=10')  
        self.assertEqual(response.status_code, 404)
        
        data = json.loads(response.data)
        self.assertEqual(data['error'], "No more data available")
        print(f"{BOLD}Expected Result:{RESET} The response should return a 404 error with an appropriate message.")
        print("Result From Code: No data available error returned as expected\n\n")

    def test_start_battle(self):
        print(f"{BOLD}Running test: test_start_battle{RESET}")
        print(f"{BOLD}Description:{RESET} Verify that starting a battle returns a valid battle ID.")
        print(f"{BOLD}Test Steps:{RESET} \n1. Send a POST request to '/battle' with two Pokémon names.")
        
        response = self.app.post('/battle', json={
            'pokemon_a': 'Pikachu',
            'pokemon_b': 'Charmander'
        })
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertIn('battle_id', data)
        print(f"{BOLD}Expected Result:{RESET} The response should contain a 'battle_id' key.")
        print("Result From Code: Battle started successfully\n\n")

    def test_start_battle_invalid_request(self):
        print(f"{BOLD}Running test: test_start_battle_invalid_request{RESET}")
        print(f"{BOLD}Description:{RESET} Verify that a battle request with missing data returns a 400 error.")
        print(f"{BOLD}Test Steps:{RESET} \n1. Send a POST request to '/battle' with missing 'pokemon_b'.")
        
        response = self.app.post('/battle', json={
            'pokemon_a': 'Pikachu' 
        })
        self.assertEqual(response.status_code, 400)

        data = json.loads(response.data)
        self.assertIn('error', data)
        print(f"{BOLD}Expected Result:{RESET} The response should return a 400 error with an appropriate message.")
        print("Result From Code: Invalid battle request error returned as expected\n\n")

    def test_get_battle_result(self):
        print(f"{BOLD}Running test: test_get_battle_result{RESET}")
        print(f"{BOLD}Description:{RESET} Verify that getting the result of a battle returns the correct status and result.")
        print(f"{BOLD}Test Data:{RESET} Start battle between 'Pikachu' and 'Charmander'")
        
        battle_response = self.app.post('/battle', json={
            'pokemon_a': 'Pikachu',
            'pokemon_b': 'Charmander'
        })
        self.assertEqual(battle_response.status_code, 200)
        battle_data = json.loads(battle_response.data)
        battle_id = battle_data['battle_id']

        result_response = self.app.get(f'/battle/{battle_id}')
        self.assertEqual(result_response.status_code, 200)

        result_data = json.loads(result_response.data)
        self.assertIn('status', result_data)
        self.assertIn('result', result_data)

        print(f"{BOLD}Expected Result:{RESET} The response should contain 'status' and 'result' keys.")
        print("Result From Code: Battle result retrieved successfully\n\n")

if __name__ == '__main__':
    unittest.main()
