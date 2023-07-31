from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from sqlalchemy.engine import Engine
from sqlalchemy import event
from flask_login import LoginManager, AnonymousUserMixin

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

db = SQLAlchemy()
DB_NAME = "dbase.db"

class Anonymous(AnonymousUserMixin):
  def __init__(self):
    self.role = 'Anon'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '0035d75b086a787e412b9eda'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    with app.app_context():
        db.create_all()

        admin_user = User.query.filter_by(username='admin', role='admin').first()

        if not admin_user:
            admin_fname = 'The'
            admin_lname = 'Admin'
            admin_username = 'admin'
            admin_password = 'pok*m0n'
            admin_role = 'admin'

            admin = User(fname=admin_fname, lname=admin_lname, username=admin_username, password=admin_password, role=admin_role)
            db.session.add(admin)
            db.session.commit()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.user_login'
    login_manager.anonymous_user = Anonymous
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

