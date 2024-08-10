import pandas as pd
from difflib import get_close_matches

def normalize_name(name):
    return name.strip().lower()

def find_pokemon_by_name(name, pokemon_data):
    name = normalize_name(name)
    all_names = pokemon_data['name'].str.lower().tolist()
    closest_matches = get_close_matches(name, all_names, n=1, cutoff=0.8)
    if closest_matches:
        return pokemon_data[pokemon_data['name'].str.lower() == closest_matches[0]]
    else:
        raise ValueError(f"Pokémon name '{name}' not found or has too many spelling mistakes.")

# function accepting two pokemon name as input   
def find_two_pokemons(pokemon_a_name, pokemon_b_name, pokemon_data):
    pokemon_a = find_pokemon_by_name(pokemon_a_name, pokemon_data)
    pokemon_b = find_pokemon_by_name(pokemon_b_name, pokemon_data)
    return pokemon_a, pokemon_b

#Calculate damage here
def calculate_damage(attacker, defender):
    
    attack = attacker['attack'].values[0]
    type1 = attacker['type1'].values[0]
    type2 = attacker['type2'].values[0]
    
    if f'against_{type1}' not in defender or (type2 and f'against_{type2}' not in defender):
        raise ValueError("Invalid type found in the Pokémon data.")

    against_type1 = defender[f'against_{type1}'].values[0]
    against_type2 = defender[f'against_{type2}'].values[0] if type2 else 1.0
    
    damage = (attack / 200) * 100 - (((against_type1 / 4) * 100) + ((against_type2 / 4) * 100))
    
    return damage

# function to find the winner of battle
def battle(pokemon_a_name, pokemon_b_name, pokemon_data):
    pokemon_a = find_pokemon_by_name(pokemon_a_name, pokemon_data)
    pokemon_b = find_pokemon_by_name(pokemon_b_name, pokemon_data)
    
    damage_a_to_b = calculate_damage(pokemon_a, pokemon_b)
    damage_b_to_a = calculate_damage(pokemon_b, pokemon_a)
    
    if damage_a_to_b > damage_b_to_a:
        winner = pokemon_a_name
        won_by_margin = damage_a_to_b - damage_b_to_a
    elif damage_b_to_a > damage_a_to_b:
        winner = pokemon_b_name
        won_by_margin = damage_b_to_a - damage_a_to_b
    else:
        winner = "Draw"
        won_by_margin = 0
    
    return {"winner": winner, "won_by_margin": won_by_margin}


