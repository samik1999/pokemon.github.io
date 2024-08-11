import psycopg2
import json

class Database:
    def __init__(self):
        self.DB_HOST = 'localhost'
        self.DB_NAME = 'your_database_name'
        self.DB_USER = 'your_username'
        self.DB_PASS = 'your_password'

    def connect(self):
        return psycopg2.connect(host=self.DB_HOST, database=self.DB_NAME, user=self.DB_USER, password=self.DB_PASS)

    def init_db(self):
        with self.connect() as conn:
            with conn.cursor() as c:
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

    def save_battle_to_db(self, battle_id, pokemon_a, pokemon_b, status, result=None):
        with self.connect() as conn:
            with conn.cursor() as c:
                c.execute('''
                    INSERT INTO battles (id, pokemon_a, pokemon_b, status, result)
                    VALUES (%s, %s, %s, %s, %s)
                ''', (battle_id, pokemon_a, pokemon_b, status, json.dumps(result)))
                conn.commit()

    def update_battle_in_db(self, battle_id, status, result=None):
        with self.connect() as conn:
            with conn.cursor() as c:
                c.execute('''
                    UPDATE battles SET status = %s, result = %s WHERE id = %s
                ''', (status, json.dumps(result), battle_id))
                conn.commit()

    def get_battle_from_db(self, battle_id):
        with self.connect() as conn:
            with conn.cursor() as c:
                c.execute('''
                    SELECT status, result FROM battles WHERE id = %s
                ''', (battle_id,))
                result = c.fetchone()
        
        if result:
            status, result = result
            return {"status": status, "result": result}
        else:
            return {"status": "BATTLE_NOT_FOUND", "result": None}
