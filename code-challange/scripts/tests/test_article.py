import pytest
from lib.models.article import Article
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.db.connection import get_connection

@pytest.fixture(autouse=True)
def setup_db():
    with open('code-challenge/lib/db/schema.sql') as f:
        schema_sql = f.read()
    conn = get_connection()
    conn.executescript(schema_sql)
    conn.commit()
    from lib.db.seed import seed
    seed()
    conn.close()

def test_article_save_and_find():
    alice = Author.find_by_name("Alice")
    mag = Magazine.find_by_name("Tech Today")
    article = Article("Test Article", alice.id, mag.id)
    article.save()
    found = Article.find_by_id(article.id)
    assert found is not None
    assert found.title == "Test Article"
    assert found.author_id == alice.id
    assert found.magazine_id == mag.id

def test_article_find_by_title():
    articles = Article.find_by_title("AI Revolution")
    assert any(a.title == "AI Revolution" for a in articles)

def test_article_author_and_magazine():
    article = Article.find_by_title("AI Revolution")[0]
    assert article.author.name == "Alice"
    assert article.magazine.name == "Tech Today"

def test_article_not_found():
    assert Article.find_by_id(9999) is None
    assert Article.find_by_title("Nonexistent") == []
    assert Article.find_by_author(9999) == []
    assert Article.find_by_magazine(9999) == []

def test_article_save_update():
    alice = Author.find_by_name("Alice")
    mag = Magazine.find_by_name("Tech Today")
    article = Article("Update Test", alice.id, mag.id)
    article.save()
    article.title = "Updated Title"
    article.save()
    found = Article.find_by_id(article.id)
    assert found.title == "Updated Title"

def test_article_author_magazine_none():
    article = Article("Orphan", None, None)
    article.save()
    assert article.author is None
    assert article.magazine is None