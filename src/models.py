from __future__ import annotations

from typing import List


class Product:
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
    ) -> None:
        self.name = name
        self.description = description
        self._price = price  # приватный атрибут цены
        self.quantity = quantity

    @property
    def price(self) -> float:
        """Геттер цены."""
        return self._price

    @price.setter
    def price(self, new_price: float) -> None:
        """Сеттер цены с проверкой."""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return
        # Доп. задание: подтверждение при понижении цены
        if new_price < self._price:
            answer = input(f"Цена снижается с {self._price} до {new_price}. Подтвердите (y/n): ")
            if answer.lower() != "y":
                return
        self._price = new_price

    @classmethod
    def new_product(
            cls,
            data: dict,
            products_list: List[Product] | None = None,
    ) -> Product:
        """Создаёт объект Product из словаря.

        Задание: если товар с таким именем уже есть в products_list,
        складывает количество и выбирает более высокую цену.
        """
        name = data.get("name")
        if products_list:
            for product in products_list:
                if product.name == name:
                    product.quantity += data.get("quantity", 0)
                    new_price = data.get("price", 0)
                    if new_price > product.price:
                        product.price = new_price
                    return product
        return cls(
            name=name,
            description=data.get("description", ""),
            price=data.get("price", 0),
            quantity=data.get("quantity", 0),
        )


class Category:
    # Атрибуты класса: общие для всех объектов
    category_count: int = 0
    product_count: int = 0

    def __init__(
        self,
        name: str,
        description: str,
        products: List[Product],
    ) -> None:
        self.name = name
        self.description = description
        self.__products = products if products else []  # приватный атрибут

        # Увеличиваем счётчики
        Category.category_count += 1
        Category.product_count += len(self.__products)

    def add_product(self, product: Product) -> None:
        """Добавляет продукт в приватный список и увеличивает счётчик."""
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """Геттер: возвращает строку со всеми продуктами."""
        result = ""
        for product in self.__products:
            result += f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт.\n"
        return result