from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

def seed():
    # Clear previous data for idempotency
    from lib.db.connection import get_connection
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM magazines")
    conn.commit()
    conn.close()

    a1 = Author("Alice Smith")
    a1.save()
    a2 = Author("Bob Johnson")
    a2.save()

    m1 = Magazine("Tech Today", "Technology")
    m1.save()
    m2 = Magazine("Health Weekly", "Health")
    m2.save()

    a1.add_article(m1, "The Future of AI")
    a1.add_article(m2, "Healthy Living Tips")
    a2.add_article(m1, "Cybersecurity Essentials")
    a2.add_article(m1, "Cloud Computing Trends")
