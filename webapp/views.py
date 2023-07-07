from flask import Blueprint, render_template, request, redirect, url_for
from . import db
from .models import User, Category, Product, Booking

views = Blueprint("views", __name__)

@views.route("/admin_dashboard")
def admin_dashboard():
    categories = Category.query.all()
    products = Product.query.all()
    return render_template("admin_dashboard", categories = categories, products = products)

@views.route("/create_category")
def create_category():
    cname = request.form.get("cname")
    category = Category(cname = cname)
    db.session.add(category)
    db.session.commit()
    return redirect(url_for("views.admin_dashboard"))

@views.route("/edit_category/category/<int:category_id>")
def edit_category(category_id):
    this_category = Category.query.get(category_id)
    cname = request.form.get("CategoryName")
    this_category.cname = cname
    db.session.commit()
    return redirect(url_for("views.admin_dashboard"))

@views.route("/delete_category/category/<int:category_id>")
def delete_category(category_id):
    category = Category.query.get(category_id)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for("views.admin_dashboard"))

@views.route("/create_product")
def create_product():
    pname = request.form.get("ProductName")
    manf_date = request.form.get("manf_date")
    exp_date = request.form.get("exp_date")
    unit = request.form.get("Unit")
    rateperunit = request.form.get("Rate/unit")
    quantity = request.form.get("Quantity")
    product = Product(pname = pname, manf_date = manf_date, exp_date = exp_date, unit = unit, rateperunit = rateperunit, quantity = quantity)
    db.session.add(product)
    db.session.commit()
    return redirect(url_for("views.admin_dashboard"))

@views.route("/edit_product/product/<int:product_id>")
def edit_product(product_id):
    this_product = Product.query.get(product_id)
    pname = request.form.get("ProductName")
    manf_date = request.form.get("manf_date")
    exp_date = request.form.get("exp_date")
    unit = request.form.get("Unit")
    rateperunit = request.form.get("Rate/unit")
    quantity = request.form.get("Quantity")
    this_product.pname = pname
    this_product.manf_date = manf_date
    this_product.exp_date = exp_date
    this_product.unit = unit
    this_product.rateperunit = rateperunit
    this_product.quantity = quantity
    db.session.commit()
    return redirect(url_for("views.admin_dashboard"))

@views.route("/delete_product/product/<int:product_id>")
def delete_product(product_id):
    product = Product.query.get(product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for("views.admin_dashboard"))

@views.route("/admin_summary")
def admin_summary():
    return render_template("admin_summary")

@views.route("/user_dashboard")
def user_dashboard():
    categories = Category.query.all()
    products = Product.query.all()
    return render_template("user_dashboard", categories = categories, products = products)

@views.route("/create_booking/bookings/<int:category_id>/<int:product_id>")
def create_booking(category_id, product_id):
    category = Category.query.get(category_id)
    product = Product.query.get(product_id)
    return redirect(url_for("views.user_dashboard"))

@views.route("/delete_booking")
def delete_booking():
    return redirect(url_for("views.user_dashboard"))

@views.route("/user_bookings")
def user_bookings():
    return render_template("user_bookings")