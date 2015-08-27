#############################################################
# @author: jasmine hsu
# @contact: jch550@nyu.edu
# @description:
#   configuration file for web app
#############################################################

import os

# this is the base configuration 
# for all deployments
class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'temp'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    MEDIA_ROOT = 'media'
    STATIC_ROOT = 'static'
    # mail configs
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'whatcanifarm@gmail.com'
    MAIL_PASSWORD = 'capstone2015'

class ProductionConfig(Config):
    DEBUG = False

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    STATICFILES_DIRS = "/Users/jasminehsu/school/what-can-i-farm" # only for dev

class TestingConfig(Config):
    TESTING = True
