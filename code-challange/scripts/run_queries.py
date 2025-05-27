from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

if __name__ == "__main__":

     alice = Author.find_by_name("Alice")
    if alice:
        print(f"Articles by {alice.name}:")
        for article in alice.articles:
            print(f"- {article.title}")