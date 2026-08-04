"""
DATABASE CRUD AND QUERYSET LOOKUPS
==================================
This script demonstrates how to execute create, read, update, and delete actions
and filter records using field lookups.
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

class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_digits=2)
    stock = models.IntegerField()

    class Meta:
        app_label = "__main__"

    def __str__(self):
        return f"{self.name} - ${self.price} (Stock: {self.stock})"

if __name__ == "__main__":
    # Create tables
    call_command("migrate", run_syncdb=True, verbosity=0)
    
    # 1. CREATE
    Product.objects.create(name="Laptop", category="Electronics", price=999.99, stock=5)
    Product.objects.create(name="Smartphone", category="Electronics", price=499.50, stock=12)
    Product.objects.create(name="Coffee Mug", category="Kitchen", price=12.99, stock=100)
    Product.objects.create(name="Desk Chair", category="Office", price=120.00, stock=0)
    
    print("[ORM] Database initialized with products.")
    
    # 2. READ & FILTER
    print("\n--- Reading Products ---")
    # Fetch all records
    all_products = Product.objects.all()
    print(f"All products count: {len(all_products)}")
    
    # Simple filter
    electronics = Product.objects.filter(category="Electronics")
    print(f"Electronics: {list(electronics)}")
    
    # Field lookups: price__gt (greater than), stock__lte (less than or equal)
    expensive = Product.objects.filter(price__gt=150.00)
    print(f"Products > $150: {list(expensive)}")
    
    out_of_stock = Product.objects.filter(stock=0)
    print(f"Out of stock items: {list(out_of_stock)}")
    
    # Case-insensitive substring match: name__icontains
    coffee_items = Product.objects.filter(name__icontains="coffee")
    print(f"Coffee products: {list(coffee_items)}")
    
    # 3. UPDATE
    print("\n--- Updating Records ---")
    # Get a single record
    laptop = Product.objects.get(name="Laptop")
    print(f"Original Laptop Stock: {laptop.stock}")
    
    # Modify field and save
    laptop.stock = 15
    laptop.save()
    
    # Verify update
    updated_laptop = Product.objects.get(name="Laptop")
    print(f"Updated Laptop Stock: {updated_laptop.stock}")
    
    # Bulk update
    Product.objects.filter(category="Electronics").update(price=50.00)
    print(f"Bulk discounted electronics: {list(Product.objects.filter(category='Electronics'))}")
    
    # 4. DELETE
    print("\n--- Deleting Records ---")
    mug = Product.objects.get(name="Coffee Mug")
    mug.delete()
    
    # Verify deletion
    try:
        Product.objects.get(name="Coffee Mug")
    except Product.DoesNotExist:
        print("Coffee Mug has been deleted from the database.")
