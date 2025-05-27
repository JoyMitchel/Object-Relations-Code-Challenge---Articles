from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

if __name__ == "__main__":

     alice = Author.find_by_name("Alice")
    if alice:
        print(f"Articles by {alice.name}:")
        for article in alice.articles:
            print(f"- {article.title}")

       if alice:
        print(f"Magazines {alice.name} contributed to:")
        for mag in alice.magazines:
            print(f"- {mag.name} ({mag.category})")
       
        tech_today = Magazine.find_by_name("Tech Today")
    if tech_today:
        print(f"Contributors to {tech_today.name}:")
        for author in tech_today.contributors:
            print(f"- {author.name}")


    if tech_today:
        print(f"Articles in {tech_today.name}:")
        for article in tech_today.articles:
            print(f"- {article.title} by {article.author.name}")