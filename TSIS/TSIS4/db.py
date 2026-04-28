import psycopg2
from config import load_config

def init_db():
    commands = (
        """CREATE TABLE IF NOT EXISTS players (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL
        )""",
        """CREATE TABLE IF NOT EXISTS game_sessions (
            id SERIAL PRIMARY KEY,
            player_id INTEGER REFERENCES players(id),
            score INTEGER NOT NULL,
            level_reached INTEGER NOT NULL,
            played_at TIMESTAMP DEFAULT NOW()
        )"""
    )
    config = load_config()
    with psycopg2.connect(**config) as conn:
        with conn.cursor() as cur:
            for command in commands:
                cur.execute(command)
        conn.commit()

def save_score(username, score, level):
    config = load_config()
    with psycopg2.connect(**config) as conn:
        with conn.cursor() as cur:
            # Insert player if not exists, then get ID
            cur.execute("INSERT INTO players (username) VALUES (%s) ON CONFLICT (username) DO NOTHING", (username,))
            cur.execute("SELECT id FROM players WHERE username = %s", (username,))
            player_id = cur.fetchone()[0]
            # Save session
            cur.execute("INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s)",
                        (player_id, score, level))
        conn.commit()

def get_top_scores():
    config = load_config()
    with psycopg2.connect(**config) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT p.username, gs.score, gs.level_reached, gs.played_at::DATE 
                FROM game_sessions gs JOIN players p ON gs.player_id = p.id 
                ORDER BY gs.score DESC LIMIT 10
            """)
            return cur.fetchall()

def get_user_best(username):
    config = load_config()
    with psycopg2.connect(**config) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT MAX(score) FROM game_sessions gs JOIN players p ON gs.player_id = p.id WHERE p.username = %s", (username,))
            res = cur.fetchone()[0]
            return res if res else 0