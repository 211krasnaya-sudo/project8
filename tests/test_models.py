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
    assert c.products == ""


def test_category_initialization_with_products():
    p1 = Product("Apple", "Red apple", 1.2, 10)
    p2 = Product("Banana", "Yellow banana", 0.8, 20)
    c = Category("Fruits", "All fruits", [p1, p2])
    assert "Apple, 1.2 руб. Остаток: 10 шт." in c.products
    assert "Banana, 0.8 руб. Остаток: 20 шт." in c.products


def test_category_class_attributes_count_categories():
    Category.category_count = 0
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


# ─── Задание 1: приватный атрибут products и метод add_product ───

def test_products_is_private():
    cat = Category("Фрукты", "Свежие фрукты", [])
    assert hasattr(cat, "_Category__products")
    assert isinstance(cat.products, str)


def test_add_product_appends_to_list():
    cat = Category("Фрукты", "Свежие", [])
    apple = Product("Яблоко", "Красное", 80, 15)
    cat.add_product(apple)
    assert len(cat._Category__products) == 1


def test_add_product_increments_counter():
    Category.product_count = 0
    cat = Category("Фрукты", "Свежие", [])
    cat.add_product(Product("Яблоко", "Красное", 80, 15))
    cat.add_product(Product("Груша", "Жёлтая", 100, 10))
    assert Category.product_count == 2


def test_add_product_returns_none():
    cat = Category("Фрукты", "Свежие", [])
    result = cat.add_product(Product("Яблоко", "Красное", 80, 15))
    assert result is None


# ─── Задание 2: геттер products ───

def test_products_getter_returns_string():
    cat = Category("Фрукты", "Свежие", [])
    cat.add_product(Product("Яблоко", "Красное", 80, 15))
    cat.add_product(Product("Груша", "Жёлтая", 100, 10))
    result = cat.products
    assert isinstance(result, str)
    assert "Яблоко, 80 руб. Остаток: 15 шт." in result
    assert "Груша, 100 руб. Остаток: 10 шт." in result


def test_products_getter_empty_category():
    cat = Category("Пусто", "Ничего нет", [])
    assert cat.products == ""


def test_products_getter_format():
    cat = Category("Фрукты", "Свежие", [])
    cat.add_product(Product("Банан", "Жёлтый", 50, 30))
    expected = "Банан, 50 руб. Остаток: 30 шт.\n"
    assert cat.products == expected


# ─── Задание 3: класс-метод new_product ───

def test_new_product_creates_instance():
    data = {"name": "Арбуз", "description": "Сладкий", "price": 200, "quantity": 5}
    product = Product.new_product(data)
    assert isinstance(product, Product)
    assert product.name == "Арбуз"
    assert product.price == 200
    assert product.quantity == 5


def test_new_product_existing_duplicate():
    existing = Product("Арбуз", "Сладкий", 200, 5)
    data = {"name": "Арбуз", "description": "Другой", "price": 250, "quantity": 10}
    result = Product.new_product(data, products_list=[existing])
    assert result is existing
    assert existing.quantity == 15
    assert existing.price == 250


def test_new_product_duplicate_lower_price():
    existing = Product("Арбуз", "Сладкий", 300, 5)
    data = {"name": "Арбуз", "description": "Другой", "price": 200, "quantity": 10}
    result = Product.new_product(data, products_list=[existing])
    assert result.quantity == 15
    assert result.price == 300


# ─── Задание 4: геттер и сеттер цены ───

def test_price_getter():
    product = Product("Хлеб", "Свежий", 50, 10)
    assert product.price == 50


def test_price_setter_positive():
    product = Product("Хлеб", "Свежий", 50, 10)
    product.price = 60
    assert product.price == 60


def test_price_setter_zero(capsys):
    product = Product("Хлеб", "Свежий", 50, 10)
    product.price = 0
    assert product.price == 50
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out


def test_price_setter_negative(capsys):
    product = Product("Хлеб", "Свежий", 50, 10)
    product.price = -10
    assert product.price == 50
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out


# ─── Доп. задание 4: подтверждение при понижении цены ───

def test_price_decrease_confirmed(monkeypatch):
    product = Product("Хлеб", "Свежий", 100, 10)
    monkeypatch.setattr("builtins.input", lambda _: "y")
    product.price = 80
    assert product.price == 80


def test_price_decrease_cancelled(monkeypatch):
    product = Product("Хлеб", "Свежий", 100, 10)
    monkeypatch.setattr("builtins.input", lambda _: "n")
    product.price = 80
    assert product.price == 100
