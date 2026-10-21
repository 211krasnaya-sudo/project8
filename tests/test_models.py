import pytest

from models import Category, LawnGrass, Order, Product, Smartphone


# --- 1. Базовые тесты ---
def test_product_initialization():
    p = Product(name="Apple", description="Red apple",
                price=1.2, quantity=10)
    assert p.name == "Apple"
    assert p.description == "Red apple"
    assert p.price == 1.2
    assert p.quantity == 10


def test_product_str():
    p = Product("Яблоко", "Красное", 80, 15)
    assert str(p) == "Яблоко, 80 руб. Остаток: 15 шт."


# --- 2. ТЕСТ 1: Цена <= 0 (строки 53, 57, 64) ---

def test_price_setter_rejects_non_positive(monkeypatch):
    p = Product("Булка", "Мягкая", 100.0, 5)
    with pytest.raises(ValueError):
        p.price = 0


# --- 3. ТЕСТ 2: Снижение цены → input (строки 80, 87, 105) ---

def test_price_setter_requires_confirmation_on_decrease(monkeypatch):
    p = Product("Булка", "Мягкая", 100.0, 5)  # Жёстко фиксируем 100

    # Подменяем input на "y" (согласие)
    monkeypatch.setattr("builtins.input", lambda _: "y")

    # Снижаем цену до 90 (90 < 100)
    p.price = 90.0
    assert p.price == 90.0  # Цена изменилась


# --- 4. ТЕСТ 3: Снижение цены, но отказ (строки 80, 87, 105) ---
# Проверяем ветку, где пользователь отвечает "n"
def test_price_setter_rejects_decrease_on_n(monkeypatch):
    p = Product("Булка", "Мягкая", 100.0, 5)
    monkeypatch.setattr("builtins.input", lambda _: "n")

    with pytest.raises(ValueError):
        p.price = 80.0


# --- 5. ТЕСТ 4: Повышение цены (без input) ---
def test_price_setter_allows_increase(monkeypatch):
    p = Product("Булка", "Мягкая", 100.0, 5)

    # Повышение цены не должно вызывать input
    p.price = 150.0
    assert p.price == 150.0


# --- 6. Тесты для new_product ---
def test_new_product_creates_new():
    data = {"name": "Арбуз", "description": "Сладкий",
            "price": 200, "quantity": 5}
    p = Product.new_product(data)
    assert isinstance(p, Product)
    assert p.name == "Арбуз"


def test_new_product_updates_existing_and_raises_price():
    existing = Product("Торт", "Вкусный", 500, 2)
    data = {"name": "Торт", "price": 600, "quantity": 3}

    result = Product.new_product(data, products_list=[existing])

    assert result is existing
    assert existing.quantity == 3
    assert existing.price == 600


# --- 7. Тесты для Order (Закрывают 232-233, 236, 242-243, 246-248) ---

def test_order_rejects_zero_quantity():
    p = Product("Товар", "Desc", 10, 5)
    with pytest.raises(ValueError):
        Order(p, 0)  # Строка 236


def test_order_rejects_negative_quantity():
    p = Product("Товар", "Desc", 10, 5)
    with pytest.raises(ValueError):
        Order(p, -5)  # Строки 242-243


def test_order_valid_creation_and_assignments():
    """
    Создаёт валидный Order, чтобы покрыть строки присваивания
    (self.product, self.quantity).
    """
    p = Product("Чай", "Зеленый", 10.0, 10)
    order = Order(p, 1)  # quantity = 1 > 0, ValueError не будет

    assert order.product is p
    assert order.quantity == 1


# --- 8. Тесты для Category ---
def test_category_init_validates():
    p = Product("Яблоко", "Красное", 80, 10)
    bad_item = "Не продукт"
    with pytest.raises(TypeError):
        Category("Фрукты", "Лучшие", [p, bad_item])


def test_category_add_and_total():
    cat = Category("Овощи", "Свежие", [])
    carrot = Product("Морковь", "Оранжевая", 30, 5)
    cat.add_product(carrot)
    assert len(cat._Category__products) == 1
    assert cat.calculate_total() == 150


# --- 9. Тесты для наследников ---
def test_smartphone_creation():
    s = Smartphone(
        name="iPhone", description="Флагман", price=1000, quantity=5,
        efficiency=9.5, model="15 Pro", memory=256, color="серый"
    )
    assert s.model == "15 Pro"
    assert "Смартфон" in str(s)


def test_lawn_grass_creation():
    g = LawnGrass(
        name="Трава",
        description="Зеленая",
        price=50,
        quantity=10,
        country="Россия",
        germination_period=7,
        color="зелёный"
    )
    assert g.country == "Россия"
    assert "Трава" in str(g)


# --- 10. Тесты для __add__ ---
def test_product_add_same_class():
    p1 = Product("A", "T", 10, 5)
    p2 = Product("B", "T2", 20, 3)
    result = p1 + p2
    assert result == (10 * 5) + (20 * 3)


def test_add_different_classes_raises():
    s = Smartphone("iPhone", "A", 1000, 1, 9.0, "14", 128, "чёрный")
    g = LawnGrass("Трава", "B", 50, 10, "Россия", 7, "зелёный")
    with pytest.raises(TypeError) as exc_info:
        _ = s + g
    assert "Нельзя складывать объекты разных классов" in str(exc_info.value)


def test_price_setter_decline_on_decrease(monkeypatch):
    p = Product("Булка", "Мягкая", 100.0, 5)
    monkeypatch.setattr("builtins.input", lambda _: "n")

    with pytest.raises(ValueError):
        p.price = 90.0


# --- Тесты для Задания 1 (валидация в __init__) ---

def test_product_rejects_zero_quantity():
    with pytest.raises(ValueError) as exc_info:
        Product("Пустой товар", "Нет на складе", 100.0, 0)
    assert str(exc_info.value) == ("Товар с нулевым количеством не "
                                   "может быть добавлен")


def test_product_rejects_negative_quantity():
    with pytest.raises(ValueError) as exc_info:
        Product("Отрицательный товар", "Странный случай", 50.0, -5)
    assert str(exc_info.value) == ("Товар с нулевым"
                                   " количеством не может быть добавлен")


# --- Тесты для Задания 2 (average_price) ---

def test_category_average_price_with_items():
    cat = Category("Фрукты", "Свежие фрукты", [])
    p1 = Product("Яблоко", "Красное", 80.0, 10)
    p2 = Product("Банан", "Жёлтый", 50.0, 20)
    cat.add_product(p1)
    cat.add_product(p2)

    avg = cat.average_price()
    assert avg == 65.0  # (80 + 50) / 2


def test_category_average_price_empty():
    cat = Category("Пустая категория", "Ничего нет", [])
    avg = cat.average_price()
    assert avg == 0.0


# --- Тесты для Доп. задания (ZeroQuantityError + try/except/else/finally) ---

def test_category_add_product_success_path():
    """
    Проверяет ветку else: товар успешно добавлен.
    Также косвенно проверяет finally (он всегда выполняется).
    """
    cat = Category("Овощи", "Свежие", [])
    p = Product("Морковь", "Оранжевая", 30.0, 5)

    # Можно перехватить print, но для простоты проверим, что товар добавился
    cat.add_product(p)
    assert len(cat._Category__products) == 1
    assert cat._Category__products[0] is p


def test_category_add_non_product_raises_type_error():
    """
    Проверяет, что Category rejects не-Product объекты
    ДО обращения к их атрибутам.
    """
    cat = Category("Странная категория", "Тестовая", [])

    with pytest.raises(TypeError) as exc_info:
        cat.add_product("Не продукт")

    assert ("В категорию можно добавлять только объекты Product"
            in str(exc_info.value))


def test_creation_logger_mixin_prints_on_init(capsys):
    # Передаём все обязательные аргументы, как в реальном классе
    Product(name="Test", description="Тестовый товар", price=10.0, quantity=5)

    captured = capsys.readouterr()
    output = captured.out

    assert output.strip() != "", (
        "Ожидался вывод от миксина, но его нет. "
        "Проверь, что в __init__ миксина есть print"
        " и он вызывается через super()."
    )


def test_category_products_property():
    cat = Category("Фрукты", "Лучшие", [])
    p1 = Product("Яблоко", "Красное", 80, 10)
    p2 = Product("Банан", "Жёлтый", 50, 20)
    cat.add_product(p1)
    cat.add_product(p2)

    result = cat.products  # Вызывает property
    assert "Яблоко" in result
    assert "Банан" in result


def test_category_total_quantity():
    cat = Category("Овощи", "Свежие", [])
    cat.add_product(Product("Морковь", "Оранж", 30, 5))
    cat.add_product(Product("Свёкла", "Тёмная", 40, 2))

    assert cat.total_quantity() == 7  # 5 + 2


def test_category_str_representation():
    cat = Category("Ягоды", "Сладкие", [])
    cat.add_product(Product("Клубника", "Свежая", 200, 3))

    s = str(cat)
    assert "Ягоды" in s
    assert "количество продуктов: 3 шт." in s


def test_category_add_operator():
    c1 = Category("A", "Cat A", [])
    c2 = Category("B", "Cat B", [])

    c1.add_product(Product("X", "X", 10, 1))  # total cost = 10
    c2.add_product(Product("Y", "Y", 20, 1))  # total cost = 20

    total_sum = c1 + c2
    assert total_sum == 30  # 10 + 20
