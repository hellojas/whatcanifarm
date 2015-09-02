#############################################################
# @title: WHAT CAN I FARM? 
#   A crop recommendation tool for the novice organic farmer.
# @author: jasmine hsu
# @contact: jch550@nyu.edu
# @description:
#   the main web application that generates an 
#   intelligent and responsive site for organic farming.
#############################################################


#################
# imports #
#################
from flask import Flask, render_template, request, flash
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask_s3 import FlaskS3
import operator
import os
import requests
import keys
import pyowm

### other pages
from flask.ext.mail import Mail, Message
from forms import ContactForm

### imports for model ###
import pandas as pd
import numpy as np

### custom model ###
from model import *
from weather import * 

import keys
#################
# configuration #
#################

app = Flask(__name__)
app.secret_key = keys.APP_KEY

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['S3_BUCKET_NAME'] = keys.AWS_BUCKET_NAME
s3 = FlaskS3(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

from model import * 

#########
# utils #
#########

# sending mail for contact form
mail = Mail()
mail.init_app(app)
app_email = keys.APP_EMAIL

# this generates the current weather
# conditions based on zipcode
weatherModel = Weather()

# @param zipcode, zipcode to query
def getWeather(zipcode):
    weatherModel.update(zipcode)
    return weatherModel.display()

##########
# routes #
##########

# the about page
# renders about.html
@app.route('/about', methods=['GET'])
def about():
    results = {} # data struct to hold vars
    return render_template('about.html', results=results)

# the contact page, generates email to recipient
# renders contact.html
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    results = {} # data struct to hold vars
    form = ContactForm()
    results["status"] = None

    # get all the data from what the user entered
    # onto the form and validate the spam checker
    if request.method == 'POST':
        print form.spam.data

        # validate the spam checker
        # return error if it is not correct
        if form.spam.data != "1":
            results["status"] = "error"
            form.name.data = form.name.data
            return render_template('contact.html', results=results, form=form)

        # if pass the spam checker, generate a message and send it
        msg = Message("[whatcanifarm] email has arrived!", sender=app_email, recipients=[app_email])
        msg.body = """ 
        From: %s <%s> 
        %s
        """ % (form.name.data, form.email.data, form.message.data)
        mail.send(msg)

        # set success status and render the same page with the success alert
        results["status"] = "success"
        return render_template('contact.html', results=results, form=form)

    elif request.method == 'GET':
        return render_template('contact.html', results=results, form=form)

# the faq page, renders faq.html
@app.route('/faq', methods=['GET'])
def faq():
    results = {} # data struct to hold vars
    return render_template('faq.html', results=results)

# the home page, renders index.html
# at the start of the root page,
# the model will run a live prediction when
# the user enters a zipcode to query
@app.route('/', methods=['GET', 'POST'])
def index():
    # set initial variables
    results = {} # data struct to hold vars
    errors = False # errors
    farmsList = pd.DataFrame() # list of local farms
    pred = pd.DataFrame() # generated predictions
    weather = {} # weather data
    limit = 10 # limit number of reccs

    # default flags
    printFarms = False
    printPred = False
    invalidZip = False

    # load the prediction model
    # see -> model.py
    mymodel = loadModel()

    if request.method == "POST":
        # get zip that the person has entered

        try:
            zipcode = request.form['zip']

            if not zipcode.isdigit():
                results["errors"] = "Not a valid zipcode. Must be numeric! Try again?"
                errors = True
                return render_template('index.html', errors=errors, results=results)
            mapImageUrl = 'http://maps.googleapis.com/maps/api/staticmap?center=%s&zoom=13&scale=1&size=500x300&maptype=hybrid&format=png&visual_refresh=true&markers=size:mid|color:0xff0000|label:A|%s' %(zipcode,zipcode)
            
            # model and weather computations
            # see modelExp.py for object method descriptions
            x = mymodel.submitZip(int(zipcode))
            if x is None: 
                invalidZip = True 
            else:
                if len(x) != 0:
                    pred = pd.DataFrame(mymodel.predict(x, limit), columns=["Class","Prob"])
                    farmsList = mymodel.getFarms(zipcode)
                    weather = getWeather(zipcode)
                    printFarms = True

            # hold computations and push to jinja
            results = {"zipcode":zipcode, "mapImageUrl":mapImageUrl, 
                "farms":farmsList, "preds":pred, "printFarms":printFarms, "invalidZip":invalidZip,
                "weather":weather}
        except:
            # display errors if zipcode is not found
            errors = True
            results["errors"] = "No data for this zipcode, try another?"
            return render_template('index.html', errors=errors,  results=results)
    return render_template('index.html', errors=errors, results=results)


if __name__ == '__main__':
    app.run()