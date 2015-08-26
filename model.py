
#############################################################
# @author: jasmine hsu
# @contact: jch550@nyu.edu
# @description:
#   this loads the random forrest model that
#   generates the crop reccomendations
#   the data for the model was generated with
#   external preorcessing scripts and loaded
#   in as pickle dumps
#############################################################


## imports
import os
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.externals import joblib
import keys
import cPickle, urllib2
## model class that holds
# input = this years weather data by zip code
# classifier = the random forrest classifier
# mlb = the lable binarizer
# validZips = list of US zipcodes
# us_farms = list of ceritified US organic farms 

class model(object):
    def __init__(self, input, classifier, mlb, validZips, us_farms ):
        self.input = input
        self.classifier = classifier
        self.validZips = validZips
        self.farms = us_farms
        self.mlb = mlb

    def getFarms(self, zip):
        '''gets the farms by zipcode'''
        return self.farms[self.farms["Zip_Code"] == int(zip)]

    def submitZip(self, zip):
        '''validate the zipcode'''
        if int(zip) in self.validZips:
            return self.input[self.input.index==int(zip)]
        else:
            return None

    def predict(self,x_input,limit):
        '''load data into model and output probabilities'''
        x = x_input
        probabilities = np.zeros(self.mlb.classes_.shape)
        for c in range(len(self.classifier.estimators_)):
            probabilities[c] = self.classifier.estimators_[c].predict_proba(x)[0][1]
        rankings = zip(self.mlb.classes_, probabilities)
        rankings.sort(key=lambda x: x[1],reverse=True)
        return rankings[0:limit]

# this loads the model with the proper pickle dumps
def loadModel():
    resources_dir = os.getcwd() + "/static/res/" # main resource directory
    # aws_app_assets = "https://%s.s3.amazonaws.com/static/res/" % keys.AWS_BUCKET_NAME
    input = joblib.load(resources_dir + 'input.pkl')
    classifier = joblib.load(resources_dir + 'classifier.pkl')
    mlb = joblib.load(resources_dir + 'mlb.pkl')
    farms = joblib.load(resources_dir + 'farms.pkl')
    zipcodes = joblib.load(resources_dir + 'us_zips.pkl')

    # input = cPickle.load(urllib2.urlopen(aws_app_assets + 'input.pkl'))
    # classifier = cPickle.load(urllib2.urlopen(aws_app_assets + 'classifier.pkl'))
    # mlb = cPickle.load(urllib2.urlopen(aws_app_assets + 'mlb.pkl'))
    # farms = cPickle.load(urllib2.urlopen(aws_app_assets + 'farms.pkl'))
    # zipcodes = cPickle.load(urllib2.urlopen(aws_app_assets + 'us_zips.pkl'))

    mymodel = model(input, classifier, mlb, zipcodes, farms)
    return mymodel
    