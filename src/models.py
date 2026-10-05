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
        self.__price = price
        self.quantity = quantity

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return
        if new_price < self.__price:
            answer = input(f"Цена снижается с {self.__price} до {new_price}. Подтвердите (y/n): ")
            if answer.lower() != "y":
                return
        self.__price = new_price

    def total_cost(self) -> float:
        """Вспомогательный метод: цена * количество."""
        return self.price * self.quantity

    def __str__(self) -> str:
        # Формат: Название продукта, X руб. Остаток: X шт.
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: "Product") -> float:
        """Сложение двух продуктов: сумма их полной стоимости (цена × количество)."""
        if not isinstance(other, Product):
            return NotImplemented
        return self.total_cost() + other.total_cost()

    @classmethod
    def new_product(
        cls,
        data: dict,
        products_list: List[Product] | None = None,
    ) -> Product:
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
        self.__products = products if products else []

        Category.category_count += 1
        Category.product_count += len(self.__products)

    def add_product(self, product: Product) -> None:
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """Геттер: возвращает строку со всеми продуктами (используя __str__)."""
        lines = [str(p) for p in self.__products]
        return "\n".join(lines) + ("\n" if lines else "")

    def total_quantity(self) -> int:
        """Общее количество товаров на складе в категории."""
        return sum(p.quantity for p in self.__products)

    def __str__(self) -> str:
        # Формат: Название категории, количество продуктов: X шт.
        qty = self.total_quantity()
        return f"{self.name}, количество продуктов: {qty} шт."
