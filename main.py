"""Проверочный модуль для демонстрации работы классов Product и Category."""

from models import Product, Category


def main():
    # Создание продуктов через класс-метод
    product_data_1 = {
        "name": "Samsung Galaxy S24",
        "description": "Флагманский смартфон",
        "price": 89990,
        "quantity": 15,
    }
    product_data_2 = {
        "name": "iPhone 15 Pro",
        "description": "Смартфон Apple",
        "price": 109990,
        "quantity": 10,
    }

    product1 = Product.new_product(product_data_1)
    product2 = Product.new_product(product_data_2)

    print("=== Созданные продукты ===")
    print(product1)
    print(product2)

    # Создание категории и добавление продуктов
    category = Category("Смартфоны", "Мобильные телефоны")
    category.add_product(product1)
    category.add_product(product2)

    print("\n=== Товары в категории ===")
    print(category.products)

    # Работа с сеттером цены
    print("=== Изменение цены ===")
    print(f"Цена до изменения: {product1.price}")
    product1.price = 79990
    print(f"Цена после изменения: {product1.price}")

    # Попытка установить нулевую цену
    print("\n=== Попытка установить нулевую цену ===")
    product1.price = 0

    # Проверка счётчиков
    print(f"\n=== Счётчики ===")
    print(f"Всего категорий: {Category.category_count}")
    print(f"Всего продуктов: {Category.product_count}")


if __name__ == "__main__":
    main()
