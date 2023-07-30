from flask import Blueprint, g, url_for, flash, redirect, request, render_template
from flask_login import login_required, login_user, logout_user, current_user
from .models import User
from . import db

auth = Blueprint('auth', __name__)



@auth.route('/admin_login', methods=['GET','POST'])
def admin_login():
    if request.method=='POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username, role='admin').first()
        if user and user.password==password:
            flash('Logged in successfully!', category='success')
            login_user(user, remember=True)
            return redirect(url_for('views.admin_dashboard'))
        else:
            flash('Invalid credentials! Please try again!', category='error')
    
    return render_template('admin_login.html', user=current_user)

@auth.route('/user_login', methods=['GET','POST'])
def user_login():
    if request.method=='POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username, role='user').first()
        if user and user.password==password:
            flash('Logged in successfully!', category='success')
            login_user(user, remember=True)
            return redirect(url_for('views.user_dashboard'))
        else:
            flash('Invalid credentials! Please try again!', category='error')
    
    return render_template('user_login.html', user=current_user)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user:
            flash('User already exists! Try another email.', category='error')
        else:
            new_user = User(fname=fname, lname=lname, username=username, password=password, role='user')
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.user_dashboard'))

    return render_template('user_register.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.user_login'))