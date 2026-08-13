import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    DISK_TOKEN = os.getenv('DISK_TOKEN')
    SECRET_KEY = os.getenv('SECRET_KEY')