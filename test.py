import unittest
from main import *


class TestUser(unittest.TestCase):
    def setUp(self):
        User.registered_users.clear()
        self.buyer = Buyer(user_id=1, user_name="buyer1", email="buyer1@example.com", password="password123")
        self.seller = Seller(user_id=2, user_name="seller1", email="seller1@example.com", password="password123")
        self.product = Product(product_id=1, product_name="Product1", price=100.0)
        self.order = Order(order_id=1)

    def test_buyer_registers_successfully(self):
        self.buyer.register()
        registered_buyer = next(user for user in User.registered_users if user.email == self.buyer.email)
        registered_buyer.is_logged_in = False
        self.assertEqual(self.buyer.__dict__, registered_buyer.__dict__)

    def test_seller_registers_successfully(self):
        self.seller.products.clear()
        self.seller.register()
        registered_seller = next(user for user in User.registered_users if user.email == self.seller.email)
        registered_seller.is_logged_in = False
        self.assertEqual(self.seller.__dict__, registered_seller.__dict__)

    def test_buyer_registers_with_existing_email(self):
        self.buyer.register()
        new_buyer = Buyer(user_id=3, user_name="buyer2", email="buyer1@example.com", password="password123")
        new_buyer.register()
        self.assertNotIn(new_buyer, User.registered_users)

    def test_seller_registers_with_existing_email(self):
        self.seller.register()
        new_seller = Seller(user_id=4, user_name="seller2", email="seller1@example.com", password="password123")
        new_seller.register()
        self.assertNotIn(new_seller, User.registered_users)

    def test_buyer_logs_in_with_correct_password(self):
        self.buyer.register()
        self.buyer.login("password123")
        self.assertTrue(self.buyer.is_logged_in)

    def test_buyer_logs_in_with_incorrect_password(self):
        self.buyer.register()
        self.buyer.login("wrongpassword")
        self.assertFalse(self.buyer.is_logged_in)

    def test_buyer_logs_out_successfully(self):
        self.buyer.register()
        self.buyer.login("password123")
        self.buyer.logout()
        self.assertFalse(self.buyer.is_logged_in)

    def test_seller_adds_product_successfully(self):
        self.seller.register()
        self.seller.add_product(self.product)
        self.assertIn(self.product, self.seller.products)

    def test_seller_removes_product_successfully(self):
        self.seller.register()
        self.seller.add_product(self.product)
        self.seller.remove_product(self.product.product_id)
        self.assertNotIn(self.product, self.seller.products)

    def test_seller_updates_product_successfully(self):
        self.seller.register()
        self.seller.add_product(self.product)
        new_product = Product(product_id=1, product_name="UpdatedProduct", price=150.0)
        self.seller.update_product(self.product.product_id, new_product)
        self.assertIn(new_product, self.seller.products)
        self.assertNotIn(self.product, self.seller.products)

    def test_buyer_views_orders(self):
        self.buyer.register()
        self.buyer.buy_product(self.product)
        self.assertEqual(len(self.buyer.orders), 1)

    def test_order_calculates_total_correctly(self):
        self.order.add_product(self.product)
        self.assertEqual(self.order.calculate_total(), 100.0)

    def test_order_cancels_successfully(self):
        self.order.add_product(self.product)
        self.order.cancel_order()
        self.assertEqual(len(self.order.products), 0)

    def test_user_places_order_successfully(self):
        self.buyer.register()
        self.buyer.buy_product(self.product)
        self.assertEqual(len(self.buyer.orders), 1)
        order = self.buyer.orders[0]
        self.assertEqual(order.order_id, 1)
        self.assertIn(self.product, order.products)


if __name__ == '__main__':
    unittest.main()