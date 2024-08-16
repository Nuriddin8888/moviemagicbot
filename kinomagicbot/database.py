import sqlite3

def setup_database():
    conn = sqlite3.connect('filmbot.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY,
                 full_name TEXT,
                 username TEXT,
                 subscribed INTEGER DEFAULT 0)''')
    conn.commit()

    c.execute('''CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                movie_code TEXT UNIQUE,
                movie_link TEXT,
                caption TEXT)''')
    conn.commit()
    conn.close()


def add_user(full_name, username, user_id):
    conn = sqlite3.connect('filmbot.db')
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO users (id, full_name, username) VALUES (?, ?, ?)', 
              (user_id, full_name, username))
    conn.commit()
    conn.close()

def get_user(full_name, user_id):
    conn = sqlite3.connect('filmbot.db')
    c = conn.cursor()
    c.execute('SELECT full_name FROM users WHERE id = ?', (user_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def is_subscribed(user_id):
    conn = sqlite3.connect('filmbot.db')
    c = conn.cursor()
    c.execute('SELECT subscribed FROM users WHERE id = ?', (user_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else 0

def get_all_users():
    conn = sqlite3.connect('filmbot.db')
    c = conn.cursor()
    c.execute("SELECT id, full_name, username, subscribed FROM users")
    users = c.fetchall()
    conn.close()
    return users

def update_subscription_status(user_id, status):
    conn = sqlite3.connect('filmbot.db')
    c = conn.cursor()
    c.execute('UPDATE users SET subscribed = ? WHERE id = ?', (status, user_id))
    conn.commit()
    conn.close()

def add_movie_to_db(movie_code, movie_link, caption):
    conn = sqlite3.connect('filmbot.db')
    c = conn.cursor()
    c.execute('INSERT INTO movies (movie_code, movie_link, caption) VALUES (?, ?, ?)', (movie_code, movie_link, caption))
    conn.commit()
    conn.close()

def get_all_movies():
    conn = sqlite3.connect('filmbot.db')
    c = conn.cursor()
    c.execute("SELECT movie_code, movie_link FROM movies")
    movies = c.fetchall()
    conn.close()
    return movies



def get_movie_by_code(movie_code):
    conn = sqlite3.connect('filmbot.db')
    c = conn.cursor()
    movie_code = movie_code.strip()
    c.execute('SELECT movie_link, caption FROM movies WHERE movie_code = ?', (movie_code,))
    result = c.fetchone()
    conn.close()    
    return result



def get_all_users_id():
    conn = sqlite3.connect('filmbot.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users")
    user_ids = [row[0] for row in cursor.fetchall()]
    conn.close()
    return user_ids



def get_all_movie_codes():
    conn = sqlite3.connect('filmbot.db')
    c = conn.cursor()
    c.execute("SELECT movie_code FROM movies")
    codes = [row[0] for row in c.fetchall()]
    conn.close()
    return codes
