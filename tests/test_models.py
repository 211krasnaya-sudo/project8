import pytest

from models import Product, Category



def test_product_initialization():
    p = Product(name="Apple", description="Red apple", price=1.2, quantity=10)
    assert p.name == "Apple"
    assert p.description == "Red apple"
    assert p.price == 1.2
    assert p.quantity == 10


def test_category_initialization_with_empty_list():
    c = Category(name="Fruits", description="All fruits", products=[])
    assert c.name == "Fruits"
    assert c.description == "All fruits"
    assert len(c.products) == 0


def test_category_initialization_with_products():
    p1 = Product("Apple", "Red apple", 1.2, 10)
    p2 = Product("Banana", "Yellow banana", 0.8, 20)
    c = Category("Fruits", "All fruits", [p1, p2])
    assert len(c.products) == 2
    assert c.products[0] is p1
    assert c.products[1] is p2


def test_category_class_attributes_count_categories():
    Category.category_count = 0  # сброс для чистоты теста
    Category.product_count = 0

    c1 = Category("Fruits", "Fruits", [])
    c2 = Category("Vegetables", "Vegetables", [])

    assert Category.category_count == 2


def test_category_class_attributes_count_products():
    Category.category_count = 0
    Category.product_count = 0

    p1 = Product("Apple", "Red", 1.2, 10)
    p2 = Product("Banana", "Yellow", 0.8, 5)
    p3 = Product("Carrot", "Orange", 0.5, 8)

    c1 = Category("Fruits", "Fruits", [p1, p2])
    c2 = Category("Vegetables", "Veg", [p3])

    assert Category.product_count == 3
