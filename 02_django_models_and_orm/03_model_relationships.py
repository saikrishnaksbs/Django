"""
MODEL RELATIONSHIPS: ONE-TO-MANY, MANY-TO-MANY, ONE-TO-ONE
==========================================================
This script demonstrates how to configure and query relational model schemas:
1. One-to-Many relationship (ForeignKey)
2. Many-to-Many relationship (ManyToManyField)
3. One-to-One relationship (OneToOneField)
"""

import django
from django.conf import settings
from django.db import models
from django.core.management import call_command

if not settings.configured:
    settings.configure(
        DEBUG=True,
        SECRET_KEY="temporary-secret-key-for-standalone-dev",
        INSTALLED_APPS=["__main__"],
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
            }
        },
    )
    django.setup()

# ----------------- RELATIONSHIP DEFINITIONS -----------------

# 1. Author (Independent model)
class Author(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        app_label = "__main__"
        
    def __str__(self):
        return self.name

# 2. Book (One-to-Many: One Author has many Books, a Book has one Author)
class Book(models.Model):
    title = models.CharField(max_length=200)
    # on_delete=models.CASCADE means if Author is deleted, delete all their books
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")

    class Meta:
        app_label = "__main__"
        
    def __str__(self):
        return self.title

# 3. Publication (Many-to-Many: A Publication releases many Books, a Book can belong to many Publications)
class Publication(models.Model):
    title = models.CharField(max_length=150)
    books = models.ManyToManyField(Book, related_name="publications")

    class Meta:
        app_label = "__main__"
        
    def __str__(self):
        return self.title

# 4. AuthorProfile (One-to-One: One Author has exactly one Profile, one Profile belongs to one Author)
class AuthorProfile(models.Model):
    author = models.OneToOneField(Author, on_delete=models.CASCADE, related_name="profile")
    biography = models.TextField()

    class Meta:
        app_label = "__main__"
        
    def __str__(self):
        return f"Profile of {self.author.name}"


# ----------------- RELATIONSHIP QUERIES -----------------

if __name__ == "__main__":
    call_command("migrate", run_syncdb=True, verbosity=0)
    
    # 1. Create instances
    author = Author.objects.create(name="George Orwell")
    
    # One-to-One creation
    profile = AuthorProfile.objects.create(author=author, biography="English novelist and essayist.")
    
    # One-to-Many creation
    book1 = Book.objects.create(title="1984", author=author)
    book2 = Book.objects.create(title="Animal Farm", author=author)
    
    # Many-to-Many creation
    pub1 = Publication.objects.create(title="Penguin Books")
    pub2 = Publication.objects.create(title="Secker & Warburg")
    
    pub1.books.add(book1, book2)
    pub2.books.add(book1)

    print("[ORM] Relational database populated.")

    # 2. Querying One-to-Many (Forward and Reverse)
    print("\n--- One-to-Many Queries ---")
    # Forward: Book -> Author
    b = Book.objects.get(title="1984")
    print(f"Book '{b.title}' was written by: {b.author.name}")
    
    # Reverse: Author -> Book (using related_name="books")
    a = Author.objects.get(name="George Orwell")
    print(f"George Orwell's books: {list(a.books.all())}")

    # 3. Querying Many-to-Many
    print("\n--- Many-to-Many Queries ---")
    # Forward: Publication -> Book
    print(f"Penguin Books publications: {list(pub1.books.all())}")
    
    # Reverse: Book -> Publication (using related_name="publications")
    print(f"Publications containing '1984': {list(book1.publications.all())}")

    # 4. Querying One-to-One
    print("\n--- One-to-One Queries ---")
    # Forward: AuthorProfile -> Author
    p = AuthorProfile.objects.get(id=profile.id)
    print(f"Profile belongs to author: {p.author.name}")
    
    # Reverse: Author -> AuthorProfile
    print(f"George Orwell biography: {author.profile.biography}")
