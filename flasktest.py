"""
@Author: 600490
@Email: xianrong.song@resvent.com
@FileName: flasktest.py
@DataTime: 2023/01/10 19:24
"""
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# MySQL所在的主机名
HOSTNAME = "127.0.0.1"
# MySQL监听的端口号，默认3306
PORT = 3306
# 连接MySQL的用户名
USERNAME = "root"
# 连接MySQL的密码
PASSWORD = "root"
# MySQL上创建的数据库名称
DATABASE = "apidata"
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"
# 是否追踪数据库修改，一般不开启, 会影响性能
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 是否显示底层执行的SQL语句
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)
migrate = Migrate(app, db)
# flask db init 终端运行，只需要执行一次
# flask db migrate 创建副本
# flask db upgrade 提交到数据库

# with db.engine.connect() as conn:
#     rs = conn.execute("select 1")
#     print(rs.fetchone())


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    extension = db.relationship("UserExtension", back_populates="user", uselist=False)

    # articles = db.relationship("Article")
# if __name__ == '__main__':
#     db.create_all()
#     app.run(debug=True)

class UserExtension(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    school = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), unique=True)
    user = db.relationship("User", back_populates="extension")


article_tag_table = db.Table(
    "article_tag_table",
    db.Column("article_id", db.Integer, db.ForeignKey("article.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id"), primary_key=True)
)


class Article(db.Model):
    __tablename__ = "article"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship("User", backref="articles")

    tags = db.relationship("Tag", secondary=article_tag_table, back_populates="articles")


class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))

    articles = db.relationship("Article", secondary=article_tag_table, back_populates="tags")


class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    newses = db.relationship("News", back_populates="category", cascade="merge")


class News(db.Model):
    __tablename__ = "news"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    category = db.relationship("Category", back_populates="newses", cascade="expunge")

# with app.app_context():
#     db.create_all()


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/user/add')
def user_add():
    user1 = User(username="张三", password="444444")
    user2 = User(username="李四", password="555555")
    user3 = User(username="王五", password="666666")
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.commit()
    return "用户添加成功！"


@app.route("/user/fetch")
def user_fetch():
    # 1. 获取User中所有数据
    users = User.query.all()

    # 2. 获取主键为1的User对象
    user = User.query.get(1)
    # print(f'{users}这个是user')
    # 3. 获取第一条数据
    user = User.query.first()
    # print(f'{user}这个是user2')

    return "数据提取成功！"

@app.route("/user/filter")
def user_filter():
    # 1. filter方法：
    users = User.query.filter(User.username == "张三").all()

    # 2. filter_by方法：
    users = User.query.filter_by(username="张三").all()

    # 3. order_by方法：
    # 3.1. 正序排序
    users = User.query.order_by("id")
    users = User.query.order_by(User.id)

    # 3.2. 倒序排序
    from sqlalchemy import desc
    users = User.query.order_by(db.text("-id"))
    users = User.query.order_by(User.id.desc())

    from sqlalchemy import desc
    users = User.query.order_by(desc("id"))

    # 4. group_by方法：
    from sqlalchemy import func
    users = db.session.query(User.username, func.count(User.id)).group_by("username").all()
    # print(users)

    # 5. 查询条件
    # 5.1. like
    users = User.query.filter(User.username.contains("张"))
    users = User.query.filter(User.username.like("%张%"))

    # 5.2. in
    users = User.query.filter(User.username.in_(["张三", "李四", "王五"]))

    # 5.3. not in
    users = User.query.filter(~User.username.in_(['张三']))

    # 5.4. is null
    users = User.query.filter(User.username == None)
    users = User.query.filter(User.username.is_(None))

    # 5.5. is not null
    users = User.query.filter(User.username != None)
    users = User.query.filter(User.username.isnot(None))

    # 5.6. and
    from sqlalchemy import and_
    users = User.query.filter(and_(User.username == "张三", User.id < 10))

    # 5.7. or
    from sqlalchemy import or_
    users = User.query.filter(or_(User.username == "张三", User.username == "李四"))
    print(users)

    return "数据过滤成功！"


@app.route("/user/update")
def user_update():
    # 1. 修改一条数据
    user = User.query.get(1)
    user.username = "张三_重新修改的"
    db.session.commit()

    # 2. 批量修改数据
    User.query.filter(User.username.like("%张三%")).update({"password": User.password + "_被修改的"})
    db.session.commit()
    return "数据修改成功！"


@app.route("/user/delete")
def user_delete():
    # user = User.query.get(1)
    # db.session.delete(user)
    # db.session.commit()

    # User.query.filter(User.username.contains("张三")).delete(synchronize_session=False)
    # db.session.commit()

    users = User.query.filter(User.username.contains("张三"))
    print(type(users))

    return "数据删除成功"


@app.route("/article/add")
def article_add():
    user = User.query.first()
    article = Article(title="aa", content="bb", author=user)
    db.session.add(article)
    db.session.commit()

    article = Article.query.filter_by(title="aa").first()
    print(article.author.username)


@app.route("/user/visit")
def user_visit_articles():
    user = User.query.first()
    for article in user.articles:
        print(article.title)
    return "user visit"


@app.route("/one2one")
def one2one():
    user = User.query.first()
    extension1 = UserExtension(school="清华大学", user=user)
    # extension2 = UserExtension(school="北京大学",user=user)
    db.session.add(extension1)
    # db.session.add(extension2)
    db.session.commit()
    return "一对一成功！"


@app.route('/many2many')
def many2many():
    article1 = Article(title="11", content="aa")
    article2 = Article(title="22", content="bb")

    tag1 = Tag(name="python")
    tag2 = Tag(name="flask")

    article1.tags.append(tag1)
    article1.tags.append(tag2)

    article2.tags.append(tag1)
    article2.tags.append(tag2)

    db.session.add_all([article1, article2])
    db.session.commit()
    return "多对多数据添加成功！"


@app.route("/save_update")
def save_update():
    category = Category(name="军事")
    news = News(title="新闻1", content="新闻内容1")
    news.category = category
    db.session.add(category)
    db.session.commit()
    return "success"


@app.route('/delete')
def delete_view():
    news = News.query.first()
    db.session.delete(news)
    db.session.commit()
    return "success"


@app.route('/delete-orphan')
def delete_orphan_view():
    category = Category.query.first()
    news = News(title="新闻2", content="新闻内容2")
    category.newses.append(news)
    db.session.commit()

    # 将news从category中解除关联
    category.newses.remove(news)
    db.session.commit()
    return "success"


@app.route("/merge")
def merge_view():
    news1 = News.query.first()

    category = Category(name="分类2")
    news2 = News(title="标题2", category=category)

    # 将news2.id设置为news1.id，在merge的时候就会根据news2的id去寻找需要merge的对象
    # 这里需要merge的就是news1，然后将news2上和news1上不同的数据复制到news1上
    news2.id = news1.id
    db.session.merge(news2)
    db.session.commit()

    return "新闻合并成功"


@app.route("/expunge")
def expunge_view():
    news = News.query.first()
    category = news.category

    db.session.expunge(news)
    category.name = '测试分类'
    db.session.commit()

    return "expunge success"


if __name__ == '__main__':
    app.run()
    users = User.query.all()
    print(f'zhegeshi {users}')
