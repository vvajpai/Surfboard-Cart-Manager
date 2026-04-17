"""
Surfboard Shopping Cart Manager

A simple yet comprehensive example demonstrating:
- Object-oriented design principles
- Custom exception handling
- Input validation and error management
- Business logic implementation
"""

import datetime


class TooManyBoardsError(Exception):
    """Raised when attempting to add more than 4 surfboards to cart."""
    def __str__(self):
        return 'Cart cannot have more than 4 surfboards in it'


class CheckoutDateError(Exception):
    """Raised when checkout date is in the past or today."""
    pass


class ShoppingCart:
    """
    A shopping cart for purchasing surfboards with discount and checkout features.
    
    Attributes:
        num_surfboards (int): Current number of surfboards in cart
        checkout_date (datetime.datetime): Scheduled checkout date
        locals_discount (bool): Whether locals discount is applied
    """
    
    MAX_SURFBOARDS = 4
    
    def __init__(self):
        """Initialize an empty shopping cart."""
        self.num_surfboards = 0
        self.checkout_date = None
        self.locals_discount = False

    def add_surfboards(self, quantity=1):
        """
        Add surfboards to the cart.
        
        Args:
            quantity (int): Number of surfboards to add (default: 1)
            
        Returns:
            str: Success message with quantity added
            
        Raises:
            TooManyBoardsError: If total would exceed MAX_SURFBOARDS
            
        Example:
            >>> cart = ShoppingCart()
            >>> cart.add_surfboards(2)
            'Successfully added 2 surfboards to cart!'
        """
        if self.num_surfboards + quantity > self.MAX_SURFBOARDS:
            raise TooManyBoardsError
        
        self.num_surfboards += quantity
        suffix = '' if quantity == 1 else 's'
        return f'Successfully added {quantity} surfboard{suffix} to cart!'

    def set_checkout_date(self, date):
        """
        Set the checkout date for the purchase.
        
        Args:
            date (datetime.datetime): Desired checkout date
            
        Raises:
            CheckoutDateError: If date is in the past or today
            
        Example:
            >>> cart = ShoppingCart()
            >>> future = datetime.datetime.now() + datetime.timedelta(days=7)
            >>> cart.set_checkout_date(future)
        """
        if date <= datetime.datetime.now():
            raise CheckoutDateError('Checkout date must be in the future')
        self.checkout_date = date

    def apply_locals_discount(self):
        """Apply a discount for local residents."""
        self.locals_discount = True

    def get_cart_summary(self):
        """
        Get a summary of the current cart state.
        
        Returns:
            dict: Cart details including boards, discount status, and checkout date
        """
        return {
            'num_surfboards': self.num_surfboards,
            'locals_discount': self.locals_discount,
            'checkout_date': self.checkout_date
        }
