from abc import ABC, abstractmethod
from typing import List


class ZeroQuantityError(Exception):
    """Пользовательское исключение: попытка добавить
    товар с нулевым количеством."""
    pass


# Миксин
class CreationLoggerMixin:
    def __init__(self, *args, **kwargs):
        print(f"[MIXIN] Запуск __init__ для {self.__class__.__name__}")
        super().__init__(*args, **kwargs)
        args_repr = ", ".join(repr(a) for a in args)
        kwargs_repr = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())
        all_args = args_repr + (", " if args and kwargs else "") + kwargs_repr
        print(f"{self.__class__.__name__}({all_args})")


# Абстрактные классы (можно оставить, если они используются где‑то ещё)
class BaseProduct(ABC):
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


class Orderable(ABC):
    @abstractmethod
    def calculate_total(self) -> float:
        pass


# Основной класс Product
class Product:
    def __init__(self, name: str, description: str,
                 price: float, quantity: int):
        print("[PRODUCT] Перед super()")
        super().__init__()
        print("[PRODUCT] После super()")
        self.name = name
        self.description = description
        # Используем сеттеры — они делают валидацию
        self.price = price
        self.quantity = quantity

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        if value <= 0:
            raise ValueError("Цена должна быть положительной")

        old_price = getattr(self, "_price", None)
        if old_price is not None and value < old_price:
            confirm = input(f"Цена снижается с {old_price} до "
                            f"{value}. Подтвердить? (y/n): ")
            if confirm.lower() != "y":
                raise ValueError("Изменение цены отклонено пользователем")

        self._price = value

    @property
    def quantity(self) -> int:
        return self._quantity

    @quantity.setter
    def quantity(self, value: int) -> None:
        if value <= 0:
            raise ValueError("Товар с нулевым количеством не "
                             "может быть добавлен")
        self._quantity = value

    def __str__(self) -> str:
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    @classmethod
    def new_product(cls, data: dict, products_list: list | None = None):
        name = data["name"]
        price = data["price"]
        quantity = data.get("quantity", 1)
        description = data.get("description", "")

        if products_list:
            for p in products_list:
                if p.name == name:
                    p.price = price
                    p.quantity = quantity
                    return p

        return cls(name, description, price, quantity)

    # __add__ возвращает число (суммарную стоимость)
    def __add__(self, other: object) -> float:
        # Если типы разные (не точно такой же класс) — выбрасываем
        # ыпонятную ошибку
        if type(other) is not type(self):
            raise TypeError("Нельзя складывать объекты разных классов")

        # Возвращаем суммарную стоимость двух товаров
        return (self.price * self.quantity) + (other.price * other.quantity)

    # Для совместимости с абстрактными классами
    # (если где‑то вызывается total_cost)
    def total_cost(self) -> float:
        return self.price * self.quantity


# Наследники
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


# Класс Order
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


# Категория
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

        # 2. Теперь безопасно обращаемся к quantity
        if product.quantity <= 0:
            raise ZeroQuantityError(
                "Товар с нулевым или отрицательным "
                "количеством нельзя добавить в категорию")

        self.__products.append(product)

    @property
    def products(self) -> str:
        lines = [str(p) for p in self.__products]
        return "\n".join(lines) + ("\n" if lines else "")

    def total_quantity(self) -> int:
        return sum(p.quantity for p in self.__products)

    def calculate_total(self) -> float:
        return sum(p.total_cost() for p in self.__products)

    def average_price(self) -> float:
        products = self.__products
        if not products:
            return 0.0
        total = sum(p.price for p in products)
        return total / len(products)

    def __str__(self) -> str:
        qty = self.total_quantity()
        return f"{self.name}, количество продуктов: {qty} шт."

    def __add__(self, other: "Category") -> float:
        if not isinstance(other, Category):
            return NotImplemented
        return sum(p.total_cost() for p in self.__products) + sum(
            p.total_cost() for p in other.__products
        )
