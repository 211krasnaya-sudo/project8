from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, List


# 1. Сначала миксин (он ничего не требует от других классов)
class CreationLoggerMixin:
    """Миксин, который выводит в консоль информацию о создании объекта."""

    def __init__(self, *args, **kwargs):
        # Сначала вызываем родительский __init__, чтобы инициализировать данные
        super().__init__(*args, **kwargs)

        args_repr = ", ".join(repr(a) for a in args)
        kwargs_repr = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())
        all_args = args_repr + (", " if args and kwargs else "") + kwargs_repr

        print(f"{self.__class__.__name__}({all_args})")


# 2. Абстрактный базовый класс (зависит только от ABC)
class BaseProduct(ABC):
    """Абстрактный базовый класс для всех продуктов."""

    @abstractmethod
    def __init__(
        self, name: str, description: str, price: float, quantity: int
    ):
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
            answer = input(
                f"Цена снижается с {self.__price} до {new_price}. "
                f"Подтвердите (y/n): "
            )
            if answer.lower() != "y":
                return
        self.__price = new_price

    @abstractmethod
    def total_cost(self) -> float:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass


# 3. Абстрактный класс Orderable (для единого интерфейса стоимости)
class Orderable(ABC):
    @abstractmethod
    def calculate_total(self) -> float:
        pass


# 4. Product — теперь он видит и миксин, и BaseProduct, и Orderable
class Product(CreationLoggerMixin, BaseProduct, Orderable):
    """Базовый продукт, реализующий общую логику."""

    def __init__(
        self, name: str, description: str, price: float, quantity: int
    ):
        super().__init__(name, description, price, quantity)

    def total_cost(self) -> float:
        return self.price * self.quantity

    def calculate_total(self) -> float:
        return self.total_cost()

    def __str__(self) -> str:
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: Any) -> float:
        if not isinstance(other, Product):
            raise TypeError(
                "Можно складывать только объекты Product и его наследников"
            )
        if type(self) is not type(other):
            raise TypeError(
                f"Нельзя складывать объекты разных классов: "
                f"{type(self).__name__} и {type(other).__name__}"
            )
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


# 5. Наследники (Smartphone, LawnGrass)
class Smartphone(Product):
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: float,
        model: str,
        memory: int,
        color: str,
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    def __str__(self) -> str:
        base = super().__str__()
        return (
            f"{base} | Смартфон: {self.model}, "
            f"память {self.memory} ГБ, цвет {self.color}"
        )


class LawnGrass(Product):
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: int,
        color: str,
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def __str__(self) -> str:
        base = super().__str__()
        return (
            f"{base} | Трава: страна {self.country}, "
            f"прорастание {self.germination_period} дней, цвет {self.color}"
        )


# 6. Класс Order
class Order(Orderable):
    def __init__(self, product: Product, quantity: int):
        if quantity <= 0:
            raise ValueError(
                "Количество товара в заказе должно быть положительным"
            )
        self.product = product
        self.quantity = quantity

    def calculate_total(self) -> float:
        return self.product.total_cost() * self.quantity

    def __str__(self) -> str:
        total = self.calculate_total()
        return (
            f"Заказ: {self.quantity} шт. товара '{self.product.name}'. "
            f"Итого: {total:.2f} руб."
        )


# 7. Категория (теперь тоже Orderable)
class Category(Orderable):
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

        for p in products:
            if not isinstance(p, Product):
                raise TypeError(
                    "В категорию можно добавлять только "
                    "объекты Product или его наследников"
                )

        self.__products = products if products else []

        Category.category_count += 1
        Category.product_count += len(self.__products)

    def add_product(self, product: Product) -> None:
        if not isinstance(product, Product):
            raise TypeError(
                "В категорию можно добавлять только "
                "объекты Product или его наследников"
            )
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        lines = [str(p) for p in self.__products]
        return "\n".join(lines) + ("\n" if lines else "")

    def total_quantity(self) -> int:
        return sum(p.quantity for p in self.__products)

    def calculate_total(self) -> float:
        return sum(p.total_cost() for p in self.__products)

    def __str__(self) -> str:
        qty = self.total_quantity()
        return f"{self.name}, количество продуктов: {qty} шт."

    def __add__(self, other: "Category") -> float:
        if not isinstance(other, Category):
            return NotImplemented
        return sum(p.total_cost() for p in self.__products) + sum(
            p.total_cost() for p in other.__products
        )
