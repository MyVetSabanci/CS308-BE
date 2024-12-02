from sqlalchemy import Column, String, Integer, ForeignKey, Text, DECIMAL, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime


 
Base = declarative_base()
"""
# Customer Table
class Customer(Base):
    _tablename_ = 'customers'
    
    user_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), nullable=False)
    middlename = Column(String(50), nullable=True)
    surname = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    phone_number = Column(String(20), nullable=True)

    # Define the relationship with the Address table
    addresses = relationship("Address", back_populates="customer", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="customer")
    shopping_cart = relationship("ShoppingCart", back_populates="customer")
"""
class Customer(Base):
    __tablename__ = 'customers'  # Corrected to use double underscores

    user_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), nullable=False)
    middlename = Column(String(50), nullable=True)
    surname = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    # Define the relationship with the Address table
    addresses = relationship("Address", back_populates="customer", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="customer")
    shopping_cart = relationship("ShoppingCart", back_populates="customer")



# Address Table
"""
class Address(Base):
    
    _tablename_ = 'address'

    customer_adres_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(CHAR(36), ForeignKey('customers.user_id', ondelete="CASCADE"), nullable=False)  # Foreign key
    street = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    zip_code = Column(String(20), nullable=False)
    country = Column(String(50), nullable=False)
    

    # Relationship with the Customer table
    customer = relationship("Customer", back_populates="addresses")
    """
    # Address Table
class Address(Base):
    __tablename__ = 'adres'

    customer_adres_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    address = Column(Text, nullable=False)
    type_ = Column(String(50), nullable=False)
    name = Column(String(100), nullable=True)
    customer_id = Column(CHAR(36), ForeignKey('customers.user_id', ondelete="CASCADE"))  # Fixed relationship with Customer

    # Relationships
    customer = relationship("Customer", back_populates="addresses")  # Fixed back_populates name
    deliveries = relationship("Delivery", back_populates="address", cascade="all, delete-orphan")  # Added relationship with Delivery


# Order Table
class Order(Base):
    __tablename__ = 'orders'

    order_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    customer_id = Column(CHAR(36), ForeignKey('customers.user_id', ondelete="SET NULL"), nullable=True)
    total_price = Column(DECIMAL(10, 2), nullable=False)
    order_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    payment_status = Column(String(50), nullable=False)
    invoice_link = Column(String(255), nullable=True)
    order_status = Column(Integer, nullable=False)

    customer = relationship("Customer", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")  # String-based reference
    delivery = relationship("Delivery", back_populates="order", cascade="all, delete-orphan")


# Order Items Table
class OrderItem(Base):
    __tablename__ = 'order_items'

    order_item_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    product_id = Column(CHAR(36), ForeignKey('products.product_id'))
    order_id = Column(CHAR(36), ForeignKey('orders.order_id'))
    price_at_purchase = Column(DECIMAL(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)

    order = relationship("Order", back_populates="order_items")  # String-based reference
    product = relationship("Product", back_populates="order_items")

"""
# Delivery Table
class Delivery(Base):
    _tablename_ = 'delivery'

    delivery_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id = Column(CHAR(36), ForeignKey('orders.order_id', ondelete="CASCADE"))
    delivery_status = Column(String(50), nullable=False)
    addres_id = Column(CHAR(36), ForeignKey('address.customer_adres_id', ondelete="SET NULL"))

    order = relationship("Order", back_populates="delivery")
    address = relationship("Address")
"""
class Delivery(Base):
    __tablename__ = 'delivery'

    delivery_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id = Column(CHAR(36), ForeignKey('orders.order_id', ondelete="CASCADE"))
    delivery_status = Column(String(50), nullable=False)
    addres_id = Column(CHAR(36), ForeignKey('adres.customer_adres_id', ondelete="SET NULL"))  # Fixed table and column name

    order = relationship("Order", back_populates="delivery")
    address = relationship("Address", back_populates="deliveries")  # Fixed back_populates name


class Product(Base):
    __tablename__ = 'products'

    product_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    model = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    category_id = Column(Integer, ForeignKey('category.category_id'), nullable=True)
    serial_number = Column(String(100), unique=True, nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    price = Column(DECIMAL(10, 2), nullable=False, default=0.00)
    cost = Column(DECIMAL(65, 2), nullable=False, default=0.0)
    distributor = Column(String(100), nullable=True)
    image_url = Column(String(255), nullable=True)
    item_sold = Column(Integer, nullable=False, default=0)
    warranty_status = Column(Integer, nullable=True)

    category = relationship("Category", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product", cascade="all, delete-orphan")  # Correctly define the relationship here
    shopping_cart_items = relationship("ShoppingCartItem", back_populates="product", cascade="all, delete-orphan")



# Shopping Cart Table
class ShoppingCart(Base):
    __tablename__ = 'shoppingcart'

    cart_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    customer_id = Column(CHAR(36), ForeignKey('customers.user_id', ondelete="CASCADE"), nullable=True)
    cart_status = Column(String(50), nullable=False)

    customer = relationship("Customer", back_populates="shopping_cart")
    items = relationship("ShoppingCartItem", back_populates="cart", cascade="all, delete-orphan")


# Shopping Cart Item Table
class ShoppingCartItem(Base):
    __tablename__ = 'shoppingcart_item'

    shopping_cart_item_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    cart_id = Column(CHAR(36), ForeignKey('shoppingcart.cart_id', ondelete="CASCADE"))
    product_id = Column(CHAR(36), ForeignKey('products.product_id', ondelete="CASCADE"))
    quantity = Column(Integer, nullable=False, default=1)

    cart = relationship("ShoppingCart", back_populates="items")
    product = relationship("Product", back_populates="shopping_cart_items")



# Category Table
class Category(Base):
    __tablename__ = 'category'

    category_id = Column(Integer, primary_key=True, autoincrement=True)
    parentcategory_id = Column(Integer, ForeignKey('category.category_id', ondelete="SET NULL"), nullable=True)
    category_name = Column(String(100), nullable=False)

    parent_category = relationship("Category", remote_side=[category_id], back_populates="subcategories")
    subcategories = relationship("Category", back_populates="parent_category")
    products = relationship("Product", back_populates="category")



from pydantic import BaseModel

# pdyanctic model for the cart item which is to be used when adding an item to the cart with certain quantity
class CartItem(BaseModel):
    product_id: str
    quantity: int

# Pydantic model for product quantity adjustments coming from the frontend (for proper type hinting)
class CartAdjustment(BaseModel):
    product_id: str
    customer_id: str