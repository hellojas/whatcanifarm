#############################################################
# @author: jasmine hsu
# @contact: jch550@nyu.edu
# @description:
#   web app server manager
#   usage:
#		python manager.py runserver
#############################################################

from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import os

from app import app, db
app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
