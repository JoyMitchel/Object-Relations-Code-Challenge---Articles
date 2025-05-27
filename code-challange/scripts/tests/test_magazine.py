import pytest
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.connection import get_connection

@pytest.fixture(autouse=True)
def setup_db():
    # Recreate schema and seed before each test
    with open('code-challenge/lib/db/schema.sql') as f:
        schema_sql = f.read()
    conn = get_connection()
    conn.executescript(schema_sql)
    conn.commit()
    from lib.db.seed import seed
    seed()
    conn.close()

def test_author_save_and_find():
    author = Author("Test Author")
    author.save()
    found = Author.find_by_id(author.id)
    assert found is not None
    assert found.name == "Test Author"

def test_author_not_found():
    assert Author.find_by_id(9999) is None
    assert Author.find_by_name("Nonexistent") is None

def test_author_articles():
    alice = Author.find_by_name("Alice")
    articles = alice.articles
    assert len(articles) >= 1
    assert all(a.author_id == alice.id for a in articles)

def test_author_no_articles():
    author = Author("No Articles")
    author.save()
    assert author.articles == []

def test_author_magazines():
    alice = Author.find_by_name("Alice")
    magazines = alice.magazines
    assert any(m.name == "Tech Today" for m in magazines)

def test_author_no_magazines():
    author = Author("No Mags")
    author.save()
    assert author.magazines == []

def test_add_article():
    alice = Author.find_by_name("Alice")
    mag = Magazine.find_by_name("Tech Today")
    article = alice.add_article(mag, "New Tech Article")
    assert article.title == "New Tech Article"
    assert article.author_id == alice.id
    assert article.magazine_id == mag.id

def test_author_add_article_and_relationships():
    author = Author("Edge Case")
    author.save()
    from lib.models.magazine import Magazine
    mag = Magazine("Edge Mag", "Edge Cat")
    mag.save()
    article = author.add_article(mag, "Edge Article")
    assert article in author.articles
    assert mag in author.magazines
    assert "Edge Cat" in author.topic_areas()

def test_topic_areas():
    alice = Author.find_by_name("Alice")
    topics = alice.topic_areas()
    assert "Technology" in topics

def test_author_topic_areas_empty():
    author = Author("No Topics")
    author.save()
    assert author.topic_areas() == []