from lib.models.author import Author
from lib.models.magazine import Magazine

def main():
   
    alice = Author.find_by_name('Alice')
    if not alice:
        alice = Author('Alice')
        alice.save()

    bob = Author.find_by_name('Bob')
    if not bob:
        bob = Author('Bob')
        bob.save()

   
    tech_today = Magazine.find_by_name('Tech Today')
    if not tech_today:
        tech_today = Magazine('Tech Today', 'Technology')
        tech_today.save()

    health_weekly = Magazine.find_by_name('Health Weekly')
    if not health_weekly:
        health_weekly = Magazine('Health Weekly', 'Health')
        health_weekly.save()

    
    alice.add_article(tech_today, "AI in 2025")
    alice.add_article(health_weekly, "Staying Fit")

   
    bob.add_article(tech_today, "Cloud Security")

   
    print(f"Alice's articles:")
    for article in alice.articles():
        print(article['title'])

   
    print(f"\nMagazines Alice has contributed to:")
    for mag in alice.magazines():
        print(mag['name'])

    
    print(f"\nAuthors who contributed to {tech_today.name}:")
    contributors = tech_today.contributors()
    for contributor in contributors:
        print(contributor['name'])

if __name__ == '__main__':
    main()
