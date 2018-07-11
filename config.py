import os, json

class Config(object):
    # you should change the secrete key in your application
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secrete-key'
    SQLALCHEMY_DATABASE_URI = '<database-url>'
    UPLOAD_FOLDER = '/tmp/'
