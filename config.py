"""
@Author: 600490
@Email: xianrong.song@resvent.com
@FileName: config.py
@DataTime: 2023/01/10 19:43
"""

SECRET_KEY = "123QWEASDZXCX"

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
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"
# 是否追踪数据库修改，一般不开启, 会影响性能
SQLALCHEMY_TRACK_MODIFICATIONS = False
# 是否显示底层执行的SQL语句
SQLALCHEMY_ECHO = True


MAILto_list = ["1002567463@qq.com"]  # 收件人的邮箱账号
MAIL_SERVER = "smtp.163.com"  # 设置服务器
MAIL_USERNAME = "s1002567463@163.com"  # 发件人的邮箱
MAIL_PASSWORD = "AKLPKUMYGMBGGEUN"  # 发件人的授权码
MAIL_postfix = "163.com"  # 发件箱的后缀
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_DEFAULT_SENDER = "s1002567463@163.com"
