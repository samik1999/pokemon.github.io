import psycopg2
import json

# Database connection parameters
DB_HOST = 'localhost'
DB_NAME = 'your_database_name'
DB_USER = 'your_username'
DB_PASS = 'your_password'

def init_db():
    """ Initialize the database and create the battles table. """
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS battles (
            id UUID PRIMARY KEY,
            pokemon_a TEXT NOT NULL,
            pokemon_b TEXT NOT NULL,
            status TEXT NOT NULL,
            result JSONB
        )
    ''')
    conn.commit()
    c.close()
    conn.close()

def save_battle_to_db(battle_id, pokemon_a, pokemon_b, status, result=None):
    """ Save the battle details to the database. """
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
    c = conn.cursor()
    c.execute('''
        INSERT INTO battles (id, pokemon_a, pokemon_b, status, result)
        VALUES (%s, %s, %s, %s, %s)
    ''', (battle_id, pokemon_a, pokemon_b, status, json.dumps(result)))
    conn.commit()
    c.close()
    conn.close()

def update_battle_in_db(battle_id, status, result=None):
    """ Update the battle status and result in the database. """
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
    c = conn.cursor()
    c.execute('''
        UPDATE battles SET status = %s, result = %s WHERE id = %s
    ''', (status, json.dumps(result), battle_id))
    conn.commit()
    c.close()
    conn.close()

def get_battle_from_db(battle_id):
    """ Retrieve battle status and result from the database. """
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
    c = conn.cursor()
    c.execute('''
        SELECT status, result FROM battles WHERE id = %s
    ''', (battle_id,))
    result = c.fetchone()
    c.close()
    conn.close()
    if result:
        status, result = result
        return {"status": status, "result": result}
    else:
        return {"status": "BATTLE_NOT_FOUND", "result": None}

