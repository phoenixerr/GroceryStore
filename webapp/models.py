from . import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    fname = db.Column(db.String(150))
    lname = db.Column(db.String(150))
    username = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    items = db.relationship("Booking", backref = "user")

class Category(db.Model):
    __tablename__ = "categories"
    cid = db.Column(db.Integer, primary_key = True)
    cname = db.Column(db.String(150))
    products = db.relationship("Product", backref = "category", passive_deletes = True)

class Product(db.Model):
    __tablename__ = "products"
    pid = db.Column(db.Integer, primary_key = True)
    pname = db.Column(db.String(50))
    manf_date = db.Column(db.Date)
    exp_date = db.Column(db.Date)
    unit = db.Column(db.String(10))
    rateperunit = db.Column(db.Numeric)
    quantity = db.Column(db.Numeric)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.cid", ondelete = "CASCADE"))

class Booking(db.Model):
    bookingid = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.cid'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.pid'))
    quantity_of_item = db.Column(db.Integer)
    item_name = db.Column(db.String(50))
    rating = db.Column(db.Integer, default=1)