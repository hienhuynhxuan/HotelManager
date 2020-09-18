from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView
from flask_login import LoginManager
from .enums import *


app = Flask(__name__)
app.secret_key = "o\x8b\xfd\xbf@4a\x8a\xbe\x8f\x85\xa7\x9fmyF"
app.config["SQLALCHEMY_DATABASE_URI"] ="mysql+pymysql://root:123456@localhost/hoteldb?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)

admin = Admin(app=app, name="QUẢN LÝ KHÁCH SẠN", template_mode="bootstrap3", index_view=AdminIndexView(name="Trang chủ"))

login = LoginManager(app=app)