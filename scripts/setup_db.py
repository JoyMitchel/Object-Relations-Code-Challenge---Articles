import sqlite3

def setup_db():
    conn = sqlite3.connect('articles.db')
    with open('lib/db/schema.sql') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print("Database schema created successfully.")

if __name__ == "__main__":
    setup_db()
