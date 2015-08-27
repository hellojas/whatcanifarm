#############################################################
# @author: jasmine hsu
# @contact: jch550@nyu.edu
# @description:
#   database model for postgres
#############################################################

from app import db
from sqlalchemy.dialects.postgresql import JSON

# this is an object that can
# be persisted into a postgres data
# base. the developer can choose
# to persist the user zipcode query
# and model predictions is necessary

class Result(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    loc = db.Column(db.String())
    crops = db.Column(JSON)
    farms = db.Column(JSON)

    def __init__(self, loc, crops, farms):
        self.loc = url
        self.crops = crops
        self.farms =farms

    def __repr__(self):
        return '<zip code {}>'.format(self.id)
