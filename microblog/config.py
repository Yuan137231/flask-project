
import os
from dotenv import load_dotenv


# 获取当前这个py文件所在文件夹绝对路径
basedir = os.path.abspath(os.path.dirname(__file__))
# 拼接路径，读取 microblog.env 环境变量文件
load_dotenv(os.path.join(basedir, 'microblog.env'))
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KE') or 'dev-test-key-123456-microblog'
    # 优先读取环境变量，无环境变量则使用本地sqlite

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI") or f"sqlite:///{os.path.join(basedir, 'data.db')}"
    # 关闭变更追踪，优化性能
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    import os

    POSTS_PER_PAGE = 3

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'false').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')  # 客户端授权密码