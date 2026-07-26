from app import app,db
from app.models import User,Post
@app.shell_context_processor
def make_shell_context():
    return {'db':db,'User':User,'Post':Post}
if __name__ == '__main__':


    print("当前数据库地址：", app.config["SQLALCHEMY_DATABASE_URI"])
    app.run(debug=True)