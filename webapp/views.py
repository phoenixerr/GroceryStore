from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps
from . import db
from .models import User, Category, Product, Booking, Order
from datetime import datetime
from sqlalchemy import exc
from flask_login import AnonymousUserMixin, LoginManager
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator



views = Blueprint("views", __name__)

class DatesUnaligned(Exception):
    pass

def admin_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            if current_user.role != 'admin':
                flash('Unauthorised access! You need admin privileges to access this page!', category='error')
                return redirect(url_for('auth.user_login'))
        return func(*args, **kwargs)
    return decorated_function

def user_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            if current_user.role != 'user':
                flash('You need to be logged in as a user to access this page!', category='error')
                return redirect(url_for('auth.user_login'))
        return func(*args, **kwargs)
    return decorated_function

@views.route('/admin_dashboard')
@admin_required
@login_required
def admin_dashboard():
    categories = Category.query.all()
    products = Product.query.all()
    return render_template("admin_dashboard.html", categories = categories, products = products)

@views.route("/create/category", methods = ["POST"])
@admin_required
@login_required
def create_category():
    cname = request.form.get("CategoryName")
    category = Category(cname = cname)
    try:
        db.session.add(category)
        db.session.commit()
    except exc.IntegrityError as e:
        db.session.rollback()       
        flash("Category already exists!")
    return redirect(url_for("views.admin_dashboard"))

@views.route("/edit/category/<int:category_id>", methods = ["POST"])
@admin_required
@login_required
def edit_category(category_id):
    this_category = Category.query.get(category_id)
    cname = request.form.get("CategoryName")
    this_category.cname = cname
    try:
        db.session.commit()
    except exc.IntegrityError as e:
        db.session.rollback()       
        flash("Category already exists!")
    return redirect(url_for("views.admin_dashboard"))

@views.route("/delete/category/<int:category_id>")
@admin_required
@login_required
def delete_category(category_id):
    category = Category.query.get(category_id)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for("views.admin_dashboard"))

@views.route("/create/product/<int:category_id>", methods = ["POST"])
@admin_required
@login_required
def create_product(category_id):
    pname = request.form.get("ProductName")
    manf_date = datetime.strptime(request.form.get("manf_date"), '%Y-%m-%d')
    exp_date = datetime.strptime(request.form.get("exp_date"), '%Y-%m-%d')
    unit = request.form.get("Unit")
    rateperunit = format(float(request.form.get("Rate/unit")), ".2f")
    quantity = format(float(request.form.get("Quantity")), ".2f")
    cat_id = category_id  
    product = Product(pname = pname, manf_date = manf_date, exp_date = exp_date, unit = unit, rateperunit = rateperunit, quantity = quantity, category_id = cat_id)
    try:
        if manf_date>datetime.now() or exp_date<datetime.now():
            raise DatesUnaligned
        db.session.add(product)
        db.session.commit()
    except exc.IntegrityError as e:
        db.session.rollback()
        flash("Product already exists or invalid value entered! Try Again!")
    except DatesUnaligned:
        db.session.rollback()
        flash("Manufacture and Expiry dates not aligned")
    except ValueError:
        db.session.rollback()
        flash("Invalid value or time format!")
    return redirect(url_for("views.admin_dashboard"))

@views.route("/edit/product/<int:product_id>", methods = ["POST"])
@admin_required
@login_required
def edit_product(product_id):
    this_product = Product.query.get(product_id)
    pname = request.form.get("ProductName")
    manf_date = datetime.strptime(request.form.get("manf_date"), '%Y-%m-%d')
    exp_date = datetime.strptime(request.form.get("exp_date"), '%Y-%m-%d')
    unit = request.form.get("Unit")
    rateperunit = format(float(request.form.get("Rate/unit")), ".2f")
    quantity = format(float(request.form.get("Quantity")), ".2f")
    this_product.pname = pname
    this_product.manf_date = manf_date
    this_product.exp_date = exp_date
    this_product.unit = unit
    this_product.rateperunit = rateperunit
    this_product.quantity = quantity
    try:
        if manf_date>datetime.now() or exp_date<datetime.now():
            raise DatesUnaligned
        db.session.commit()
    except exc.IntegrityError as e:
        db.session.rollback()
        flash("Product already exists or invalid value entered! Try Again!")
    except DatesUnaligned:
        db.session.rollback()
        flash("Manufacture/Expiry date or both not aligned!")
    except ValueError:
        db.session.rollback()
        flash("Invalid value or time format!")
    return redirect(url_for("views.admin_dashboard"))

@views.route("/delete/product/<int:product_id>")
@admin_required
@login_required
def delete_product(product_id):
    product = Product.query.get(product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for("views.admin_dashboard"))

@views.route("/admin_summary")
@admin_required
@login_required
def admin_summary():
    dict = {}
        
    cat_list = Category.query.distinct(Category.cname).all()

    for cat in cat_list:
        products = Product.query.filter_by(category_id=cat.cid)
        count = products.count()
        dict.update({cat.cname : count})
    
    categories = list(dict.keys())
    product_count = list(dict.values())
    fig = plt.figure(figsize = (10, 5)).gca()
    fig.yaxis.set_major_locator(MaxNLocator(integer=True))

    # creating the bar plot
    plt.bar(categories, product_count, color ='green', width = 0.4)
    plt.xlabel("Categories")
    plt.ylabel("No. of Products")
    plt.title("Category_wise product distribution")
    plt.tight_layout()
    plt.savefig("D:\GroceryStore\webapp\static\Images\graph.png")
    return render_template("admin_summary.html")

@views.route("/")
@user_required
@login_required
def user_dashboard():
    categories = Category.query.all()
    products = Product.query.all()
    return render_template("user_dashboard.html", user=current_user, categories = categories, products = products)

@views.route("/create/bookings/<int:category_id>/<int:product_id>", methods=['POST'])
@user_required
@login_required
def create_booking(category_id, product_id):
    category = Category.query.get(category_id)
    product = Product.query.get(product_id)
    total_price = request.form.get("Total")
    quantity = request.form.get("Quantity")
    new_quantity = product.quantity - int(quantity)
    if new_quantity>=0:
        booking = Booking(user_id=current_user.id, category_id=category_id, product_id=product_id, category_name=category.cname, quantity_of_item=quantity, item_name=product.pname, total_price=total_price)
        db.session.add(booking)
        db.session.commit()
    else:
        flash("Requested quantity not available. Sorry for inconvenience!", category='error')
    return redirect(url_for("views.user_dashboard"))

@views.route("/edit/bookings/<int:booking_id>", methods=['POST'])
@user_required
@login_required
def edit_booking(booking_id):
    this_booking = Booking.query.get(booking_id)
    category = Category.query.get(this_booking.category_id)
    product = Product.query.get(this_booking.product_id)
    quantity = request.form.get("Quantity")
    new_quantity = product.quantity - int(quantity)
    if new_quantity>=0:
        this_booking.quantity_of_item = quantity
        db.session.commit()
    else:
        flash("Requested quantity not available. Sorry for inconvenience!", category='error')
    return redirect(url_for("views.user_dashboard"))

@views.route("/delete/booking/<int:booking_id>")
@user_required
@login_required
def delete_booking(booking_id):
    booking = Booking.query.get(booking_id)
    product = Product.query.get(booking.product_id)
    product.quantity = product.quantity + booking.quantity_of_item
    db.session.delete(booking)
    db.session.commit()
    return redirect(url_for("views.user_dashboard"))

@views.route("/bookings/buy/<int:booking_id>")
@user_required
@login_required
def buy(booking_id):
    booking = Booking.query.get(booking_id)
    category = Category.query.get(booking.category_id)
    product = Product.query.get(booking.product_id)
    quantity = booking.quantity_of_item
    new_quantity = product.quantity - int(quantity)
    product.quantity = new_quantity
    order = Order(userid=current_user.id, categoryid=category.cid, productid=product.pid, categoryname=category.cname, quantity_of_product=quantity, product_name=product.pname)
    db.session.add(order)
    db.session.delete(booking)
    db.session.commit()
    return redirect(url_for("views.user_dashboard"))


@views.route("/bookings/buy_all")
@user_required
@login_required
def buy_all():
    user_id = current_user.id
    bookings = Booking.query.filter_by(user_id=user_id).all()
    for booking in bookings:
        category = Category.query.get(booking.category_id)
        product = Product.query.get(booking.product_id)
        quantity = booking.quantity_of_item
        new_quantity = product.quantity - int(quantity)
        if new_quantity>=0:
            product.quantity = new_quantity
            order = Order(userid=user_id, categoryid=category.cid, productid=product.pid, categoryname=category.cname, quantity_of_product=quantity, product_name=product.pname)
            db.session.add(order)
            db.session.delete(booking)
    db.session.commit()

@views.route("/user_bookings")
@user_required
@login_required
def user_bookings():
    bookings = Booking.query.filter_by(user_id=current_user.id).all()
    total = 0
    for booking in bookings:
        product = Product.query.get(booking.product_id)
        quantity = booking.quantity_of_item
        new_quantity = product.quantity - int(quantity)
        if new_quantity>=0:
            pass #total = total + int(booking.total_price)

    return render_template("user_bookings.html", bookings=bookings, total=total)

@views.route("/user_orders")
@user_required
@login_required
def user_orders():
    user_id=current_user.id
    orders = Order.query.filter_by(userid=user_id).all()
    return render_template("user_orders.html", orders=orders)

@views.route("/search/category", methods=["POST"])
@user_required
@login_required
def search_category():
    cat_name = request.form.get("category")
    category = Category.query.filter_by(cname=cat_name).first()
    categories = [category]
    products = Product.query.filter_by(category_id=category.cid).all()
    return render_template("user_dashboard.html", user=current_user, categories = categories, products = products)

@views.route("/search/product", methods=["POST"])
@user_required
@login_required
def search_product():
    item_name = request.form.get("product")
    products = Product.query.filter_by(pname=item_name).all()
    return render_template("search_page.html", user=current_user, products = products)