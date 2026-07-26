from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail


from config import Config
# //用户登录
from flask_login import LoginManager
app = Flask(__name__)
login=LoginManager(app)
login.login_view='login'
# print(__name__)
app.config.from_object(Config)
print(app.config['SECRET_KEY'])
db=SQLAlchemy(app)
migrate=Migrate(app,db)
mail=Mail(app)

# 延迟导入，解决循环导入报错

from app import routes, models