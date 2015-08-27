#############################################################
# @author: jasmine hsu
# @contact: jch550@nyu.edu
# @description:
#   contact form for email page
#############################################################

from flask.ext.wtf import Form

from wtforms import TextField, TextAreaField, SubmitField
from wtforms.validators import Required, ValidationError

# generate a basic contact form object
# that takes a name, email, msg, spam
# value and submit field
# this is used on the contact page
class ContactForm(Form):
  name = TextField("Name")
  email = TextField("Email")
  message = TextAreaField("Message")
  spam = TextField("Spam")
  submit = SubmitField("Send")