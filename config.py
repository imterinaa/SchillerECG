import os

class Config:
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'default_user')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'default_password')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'default_db')
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://admin:admin@two-tier-flask-app-mysql-1:3306/myDb'
