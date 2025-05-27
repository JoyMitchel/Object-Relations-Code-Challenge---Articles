from lib.db.connection import get_connection
from lib.models.article import Article
from lib.models.author import Author

class Magazine:
    def __init__(self, name, category, id=None):
        self.id = id
        self.name = name.strip()
        self.category = category.strip()

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", (self.name, self.category))
            self.id = cursor.lastrowid
        else:
            cursor.execute("UPDATE magazines SET name = ?, category = ? WHERE id = ?", (self.name, self.category, self.id))
        conn.commit()
        conn.close()

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Magazine(row['name'], row['category'], row['id'])
        return None

    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE name = ?", (name,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Magazine(row['name'], row['category'], row['id'])
        return None

    @classmethod
    def find_by_category(cls, category):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE category = ?", (category,))
        rows = cursor.fetchall()
        conn.close()
        return [Magazine(row['name'], row['category'], row['id']) for row in rows]

    def articles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Article(row['title'], row['author_id'], row['magazine_id'], row['id']) for row in rows]

    def contributors(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT au.* FROM authors au
            JOIN articles a ON au.id = a.author_id
            WHERE a.magazine_id = ?
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Author(row['name'], row['id']) for row in rows]

    def article_titles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT title FROM articles WHERE magazine_id = ?", (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [row['title'] for row in rows]

    def contributing_authors(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT au.*, COUNT(a.id) as article_count
            FROM authors au
            JOIN articles a ON au.id = a.author_id
            WHERE a.magazine_id = ?
            GROUP BY au.id
            HAVING COUNT(a.id) > 2
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Author(row['name'], row['id']) for row in rows]

    @classmethod
    def top_publisher(cls):
        # Magazine with most articles
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.*, COUNT(a.id) AS article_count
            FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            GROUP BY m.id
            ORDER BY article_count DESC
            LIMIT 1
        """)
        row = cursor.fetchone()
        conn.close()
        if row:
            return Magazine(row['name'], row['category'], row['id'])
        return None
