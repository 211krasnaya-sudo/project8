import pytest
from models import Product, Category, Order, Smartphone, LawnGrass


# --- 1. Базовые тесты ---
def test_product_initialization():
    p = Product(name="Apple", description="Red apple", price=1.2, quantity=10)
    assert p.name == "Apple"
    assert p.description == "Red apple"
    assert p.price == 1.2
    assert p.quantity == 10


def test_product_str():
    p = Product("Яблоко", "Красное", 80, 15)
    assert str(p) == "Яблоко, 80 руб. Остаток: 15 шт."


# --- 2. ТЕСТ 1: Цена <= 0 (строки 53, 57, 64) ---
# Этот тест ТОЛЬКО для проверки отказа от нулевой/отрицательной цены.
# Здесь НЕ нужен monkeypatch, потому что input не вызывается.
def test_price_setter_rejects_non_positive(monkeypatch):
    """
    Проверяет ветку new_price <= 0.
    Должен закрыть строки 53, 57, 64.
    """
    p = Product("Булка", "Мягкая", 100.0, 5)

    p.price = 0
    assert p.price == 100.0

    p.price = -10
    assert p.price == 100.0


# --- 3. ТЕСТ 2: Снижение цены → input (строки 80, 87, 105) ---
# Этот тест ТОЛЬКО для ветки со снижением цены.
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
    p = Product("Булка", "Мягкая", 100.0, 5)  # Снова жёстко 100

    # Подменяем input на "n" (отказ)
    monkeypatch.setattr("builtins.input", lambda _: "n")

    old_price = p.price
    p.price = 80.0  # Пытаемся снизить до 80

    # Цена НЕ должна измениться
    assert p.price == old_price


# --- 5. ТЕСТ 4: Повышение цены (без input) ---
def test_price_setter_allows_increase(monkeypatch):
    p = Product("Булка", "Мягкая", 100.0, 5)

    # Повышение цены не должно вызывать input
    p.price = 150.0
    assert p.price == 150.0


# --- 6. Тесты для new_product ---
def test_new_product_creates_new():
    data = {"name": "Арбуз", "description": "Сладкий", "price": 200, "quantity": 5}
    p = Product.new_product(data)
    assert isinstance(p, Product)
    assert p.name == "Арбуз"


def test_new_product_updates_existing_and_raises_price():
    existing = Product("Торт", "Вкусный", 500, 2)
    data = {"name": "Торт", "price": 600, "quantity": 3}

    result = Product.new_product(data, products_list=[existing])

    assert result is existing
    assert existing.quantity == 5
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
    Создаёт валидный Order, чтобы покрыть строки присваивания (self.product, self.quantity).
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
    """
    Проверяет ветку снижения цены, где пользователь отвечает 'n'.
    Должен закрыть строки 80, 87, 105.
    """
    p = Product("Булка", "Мягкая", 100.0, 5)
    old_price = p.price

    # Подменяем input ДО того, как меняем цену
    monkeypatch.setattr("builtins.input", lambda _: "n")

    # Пытаемся снизить цену
    p.price = 90.0

    # Цена не должна измениться
    assert p.price == old_price
