import pandas as pd
from difflib import get_close_matches

class PokemonBattleSimulator:
    def __init__(self, pokemon_data):
        self.pokemon_data = pokemon_data

    def normalize_name(self, name):
        return name.strip().lower()

    def find_pokemon_by_name(self, name):
        name = self.normalize_name(name)
        all_names = self.pokemon_data['name'].str.lower().tolist()
        closest_matches = get_close_matches(name, all_names, n=1, cutoff=0.8)
        if closest_matches:
            return self.pokemon_data[self.pokemon_data['name'].str.lower() == closest_matches[0]]
        else:
            raise ValueError(f"Pokémon name '{name}' not found or has too many spelling mistakes.")

    def find_two_pokemons(self, pokemon_a_name, pokemon_b_name):
        pokemon_a = self.find_pokemon_by_name(pokemon_a_name)
        pokemon_b = self.find_pokemon_by_name(pokemon_b_name)
        return pokemon_a, pokemon_b

    def calculate_damage(self, attacker, defender):
        attack = attacker['attack'].values[0]
        type1 = attacker['type1'].values[0]
        type2 = attacker['type2'].values[0] if attacker['type2'].values[0] else None

        if f'against_{type1}' not in defender.columns or (type2 and f'against_{type2}' not in defender.columns):
            raise ValueError("Invalid type found in the Pokémon data.")

        against_type1 = defender[f'against_{type1}'].values[0]
        against_type2 = defender[f'against_{type2}'].values[0] if type2 else 1.0
        damage = (((against_type1 / 4) * 100) + ((against_type2 / 4) * 100))- (attack / 200) * 100 
        return damage


    def battle(self, pokemon_name_a, pokemon_name_b):
        attacker = self.find_pokemon_by_name(pokemon_name_a)
        defender = self.find_pokemon_by_name(pokemon_name_b)

        damage_a = self.calculate_damage(attacker, defender)
        damage_b = self.calculate_damage(defender, attacker)
        print(f"{pokemon_name_a} vs {pokemon_name_b}: Damage A = {damage_a}, Damage B = {damage_b}")
        epsilon = 0.01  # Define a small threshold for comparison

        if damage_a > damage_b + epsilon:
            return {'winner': attacker['name'].values[0]}
        elif damage_b > damage_a + epsilon:
            return {'winner': defender['name'].values[0]}
        else:
            return {'winner': 'Draw'}

        
