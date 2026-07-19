import os

basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KE') or 'dev-test-key-123456-microblog'
    # 优先读取环境变量，无环境变量则使用本地sqlite

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI") or f"sqlite:///{os.path.join(basedir, 'data.db')}"
    # 关闭变更追踪，优化性能
    SQLALCHEMY_TRACK_MODIFICATIONS = False