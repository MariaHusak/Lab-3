from abc import ABC, abstractmethod
import datetime
import hashlib


class User(ABC):
    registered_users = []

    def __init__(self, user_id, user_name, email, password) -> None:
        self.user_id = user_id
        self.user_name = user_name
        self.email = email
        self.password = self.hash_password(password)
        self.is_logged_in = False

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    @abstractmethod
    def register(self):
        pass

    def login(self, password):
        if self.password == self.hash_password(password):
            self.is_logged_in = True
            print(f"{self.user_name} logged in successfully.")
        else:
            print("Invalid credentials.")

    def logout(self):
        self.is_logged_in = False
        print(f"{self.user_name} logged out successfully.")


class Buyer(User):
    def __init__(self, user_id, user_name, email, password) -> None:
        super().__init__(user_id, user_name, email, password)
        self.orders = []

    def register(self):
        for user in User.registered_users:
            if user.email == self.email:
                print(f"Email {self.email} is already registered.")
                return

        User.registered_users.append(self)
        print(f"Buyer {self.user_name} registered successfully.")

    def view_orders(self):
        if not self.orders:
            print("No orders found.")
        for order in self.orders:
            print(f"Order ID: {order.order_id}, Order Date: {order.order_date}, Total: {order.calculate_total()}")

    def buy_product(self, product):
        order = Order(order_id=len(self.orders) + 1)
        order.add_product(product)
        self.orders.append(order)
        print(f"Product '{product.product_name}' bought successfully.")


class Seller(User):
    def __init__(self, user_id, user_name, email, password) -> None:
        super().__init__(user_id, user_name, email, password)
        self.products = []

    def register(self):
        for user in User.registered_users:
            if user.email == self.email:
                print(f"Email {self.email} is already registered.")
                return

        User.registered_users.append(self)
        print(f"Seller {self.user_name} registered successfully.")

    def add_product(self, product):
        self.products.append(product)
        print(f"Product '{product.product_name}' added successfully.")

    def remove_product(self, product_id):
        self.products = [product for product in self.products if product.product_id != product_id]
        print(f"Product with ID {product_id} removed successfully.")

    def update_product(self, product_id, new_product):
        for i, product in enumerate(self.products):
            if product.product_id == product_id:
                self.products[i] = new_product
                print(f"Product with ID {product_id} updated successfully.")
                return
        print(f"Product with ID {product_id} not found.")


class Product:
    def __init__(self, product_id, product_name, price) -> None:
        self.product_id = product_id
        self.product_name = product_name
        self.price = price


class Order:
    def __init__(self, order_id) -> None:
        self.order_id = order_id
        self.order_date = datetime.datetime.now()
        self.products = []

    def add_product(self, product) -> str:
        self.products.append(product)
        print(f"Product '{product.product_name}' added to order.")

    def cancel_order(self) -> str:
        self.products.clear()
        print(f"Order {self.order_id} canceled successfully.")

    def calculate_total(self) -> float:
        return sum(product.price for product in self.products)

