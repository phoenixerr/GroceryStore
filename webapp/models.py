from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    fname = db.Column(db.String(150))
    lname = db.Column(db.String(150))
    username = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    role = db.Column(db.String(10), nullable=False)
    items = db.relationship("Booking", backref = "user")

    def __init__(self, fname, lname, username, password, role):
        self.fname = fname
        self.lname = lname
        self.username = username
        self.password = password
        self.role = role

class Category(db.Model):
    __tablename__ = "categories"
    cid = db.Column(db.Integer, primary_key = True)
    cname = db.Column(db.String(150), unique=True)
    products = db.relationship("Product", backref = "category", cascade = "all, delete", passive_deletes = True)

class Product(db.Model):
    __tablename__ = "products"
    pid = db.Column(db.Integer, primary_key = True)
    pname = db.Column(db.String(50), unique=True)
    manf_date = db.Column(db.Date)
    exp_date = db.Column(db.Date)
    unit = db.Column(db.String(10))
    rateperunit = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.cid", ondelete = "CASCADE"))

class Booking(db.Model):
    bookingid = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.cid'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.pid'))
    category_name = db.Column(db.String(50))
    quantity_of_item = db.Column(db.Integer)
    total_price = db.Column(db.Integer)
    item_name = db.Column(db.String(50))

class Order(db.Model):
    orderid = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('users.id'))
    categoryid = db.Column(db.Integer, db.ForeignKey('categories.cid'))
    productid = db.Column(db.Integer, db.ForeignKey('products.pid'))
    categoryname = db.Column(db.String(50))
    quantity_of_product = db.Column(db.Integer)
    product_name = db.Column(db.String(50))