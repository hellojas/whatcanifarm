from flask.ext.wtf import Form

from wtforms import TextField, TextAreaField, SubmitField
from wtforms.validators import Required, ValidationError

class ContactForm(Form):
  name = TextField("Name")
  email = TextField("Email")
  message = TextAreaField("Message")
  spam = TextField("Spam")
  submit = SubmitField("Send")