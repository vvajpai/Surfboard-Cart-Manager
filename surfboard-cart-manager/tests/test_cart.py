"""
Unit tests for Surfboard Shopping Cart Manager

This test suite demonstrates:
- setUp/tearDown lifecycle management
- Parameterized testing with subtests
- Exception handling verification
- Edge case testing
- Test documentation
"""

import unittest
import datetime
import surfshop


class TestShoppingCartBasics(unittest.TestCase):
    """Test core shopping cart functionality."""

    def setUp(self):
        """Initialize a fresh cart before each test."""
        self.cart = surfshop.ShoppingCart()

    def test_add_single_surfboard(self):
        """Test adding a single surfboard to empty cart."""
        message = self.cart.add_surfboards(1)
        self.assertEqual(message, 'Successfully added 1 surfboard to cart!')
        self.assertEqual(self.cart.num_surfboards, 1)

    def test_add_multiple_surfboards(self):
        """Test adding multiple surfboards with correct grammar."""
        for quantity in range(2, 5):
            with self.subTest(quantity=quantity):
                cart = surfshop.ShoppingCart()
                expected = f"Successfully added {quantity} surfboards to cart!"
                self.assertEqual(cart.add_surfboards(quantity), expected)
                self.assertEqual(cart.num_surfboards, quantity)

    def test_add_surfboards_cumulative(self):
        """Test that surfboards accumulate correctly in cart."""
        self.cart.add_surfboards(1)
        self.cart.add_surfboards(2)
        self.assertEqual(self.cart.num_surfboards, 3)
        self.assertIn('Successfully added', self.cart.add_surfboards(1))

    def test_add_default_quantity(self):
        """Test that default quantity is 1 when not specified."""
        message = self.cart.add_surfboards()
        self.assertEqual(self.cart.num_surfboards, 1)
        self.assertIn('1 surfboard', message)


class TestShoppingCartErrors(unittest.TestCase):
    """Test error handling and edge cases."""

    def setUp(self):
        """Initialize a fresh cart before each test."""
        self.cart = surfshop.ShoppingCart()

    def test_add_too_many_surfboards_at_once(self):
        """Test that adding >4 boards raises TooManyBoardsError."""
        with self.assertRaises(surfshop.TooManyBoardsError):
            self.cart.add_surfboards(5)

    def test_add_surfboards_exceeding_limit(self):
        """Test that exceeding limit after partial add raises error."""
        self.cart.add_surfboards(3)
        with self.assertRaises(surfshop.TooManyBoardsError):
            self.cart.add_surfboards(2)

    def test_add_exactly_max_boards(self):
        """Test that exactly 4 boards is allowed."""
        message = self.cart.add_surfboards(4)
        self.assertEqual(self.cart.num_surfboards, 4)
        self.assertIn('4 surfboards', message)

    def test_exceed_limit_by_one(self):
        """Test boundary condition: 4 boards + 1 more fails."""
        self.cart.add_surfboards(4)
        with self.assertRaises(surfshop.TooManyBoardsError):
            self.cart.add_surfboards(1)

    def test_too_many_boards_error_message(self):
        """Test the error message for TooManyBoardsError."""
        with self.assertRaises(surfshop.TooManyBoardsError) as context:
            self.cart.add_surfboards(5)
        self.assertIn('4 surfboards', str(context.exception))


class TestDiscountFeature(unittest.TestCase):
    """Test locals discount functionality."""

    def setUp(self):
        """Initialize a fresh cart before each test."""
        self.cart = surfshop.ShoppingCart()

    def test_apply_locals_discount(self):
        """Test that discount flag is set when applied."""
        self.assertFalse(self.cart.locals_discount)
        self.cart.apply_locals_discount()
        self.assertTrue(self.cart.locals_discount)

    def test_discount_persists(self):
        """Test that discount remains applied after cart modifications."""
        self.cart.apply_locals_discount()
        self.cart.add_surfboards(2)
        self.assertTrue(self.cart.locals_discount)

    def test_discount_independent_from_boards(self):
        """Test that discount and boards are independent attributes."""
        self.cart.add_surfboards(3)
        self.cart.apply_locals_discount()
        self.assertEqual(self.cart.num_surfboards, 3)
        self.assertTrue(self.cart.locals_discount)


class TestCheckoutDateValidation(unittest.TestCase):
    """Test checkout date validation logic."""

    def setUp(self):
        """Initialize a fresh cart before each test."""
        self.cart = surfshop.ShoppingCart()

    def test_set_valid_future_date(self):
        """Test setting a valid future checkout date."""
        future_date = datetime.datetime.now() + datetime.timedelta(days=7)
        self.cart.set_checkout_date(future_date)
        self.assertEqual(self.cart.checkout_date, future_date)

    def test_set_multiple_future_dates(self):
        """Test updating checkout date multiple times."""
        date1 = datetime.datetime.now() + datetime.timedelta(days=3)
        date2 = datetime.datetime.now() + datetime.timedelta(days=7)
        
        self.cart.set_checkout_date(date1)
        self.assertEqual(self.cart.checkout_date, date1)
        
        self.cart.set_checkout_date(date2)
        self.assertEqual(self.cart.checkout_date, date2)

    def test_reject_past_date(self):
        """Test that past dates are rejected."""
        past_date = datetime.datetime.now() - datetime.timedelta(days=7)
        with self.assertRaises(surfshop.CheckoutDateError):
            self.cart.set_checkout_date(past_date)

    def test_reject_current_date(self):
        """Test that current/today's date is rejected."""
        # Get current date at midnight to ensure it's 'today'
        today = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        with self.assertRaises(surfshop.CheckoutDateError):
            self.cart.set_checkout_date(today)

    def test_accept_tomorrow(self):
        """Test that tomorrow's date is accepted."""
        tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
        self.cart.set_checkout_date(tomorrow)
        self.assertIsNotNone(self.cart.checkout_date)

    def test_checkout_date_unchanged_on_error(self):
        """Test that invalid date doesn't modify the cart's date."""
        future_date = datetime.datetime.now() + datetime.timedelta(days=7)
        self.cart.set_checkout_date(future_date)
        
        past_date = datetime.datetime.now() - datetime.timedelta(days=1)
        with self.assertRaises(surfshop.CheckoutDateError):
            self.cart.set_checkout_date(past_date)
        
        # Original date should remain unchanged
        self.assertEqual(self.cart.checkout_date, future_date)


class TestCartInitialization(unittest.TestCase):
    """Test cart initialization and defaults."""

    def test_cart_starts_empty(self):
        """Test that new cart is empty."""
        cart = surfshop.ShoppingCart()
        self.assertEqual(cart.num_surfboards, 0)

    def test_cart_has_no_discount_initially(self):
        """Test that discount is not applied by default."""
        cart = surfshop.ShoppingCart()
        self.assertFalse(cart.locals_discount)

    def test_cart_has_no_checkout_date_initially(self):
        """Test that checkout date is not set by default."""
        cart = surfshop.ShoppingCart()
        self.assertIsNone(cart.checkout_date)

    def test_cart_summary(self):
        """Test cart summary method returns correct state."""
        cart = surfshop.ShoppingCart()
        cart.add_surfboards(2)
        cart.apply_locals_discount()
        future_date = datetime.datetime.now() + datetime.timedelta(days=5)
        cart.set_checkout_date(future_date)
        
        summary = cart.get_cart_summary()
        self.assertEqual(summary['num_surfboards'], 2)
        self.assertTrue(summary['locals_discount'])
        self.assertEqual(summary['checkout_date'], future_date)


if __name__ == '__main__':
    unittest.main()
