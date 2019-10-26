from datetime import datetime
from flask import Flask, render_template
from flask_wtf import FlaskForm
from json import loads
from os import environ
from wtforms.fields import StringField, SubmitField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, length


application = Flask(__name__)
application.secret_key = environ['FLASK_SECRET_KEY']


@application.route('/')
class ContactForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(), length(max=200)],
                       render_kw={"placeholder": "Name", "class": "input"})
    email = EmailField('Email Address',
                       validators=[DataRequired(), length(max=200)],
                       render_kw={"placeholder": "Email", "class": "input"})
    message = TextAreaField('Message',
                            validators=[DataRequired(), length(max=5000)],
                            render_kw={"placeholder": "Enter your message here...",
                                       "class": "input"})
    submit = SubmitField('Send', render_kw={"class": "button is-link"})


def about():
    with open('data/skills.json') as skills_f:
        skills = loads(skills_f.read())

    return render_template('index.html', year=datetime.now().year, skills=skills['skills'])


if __name__ == '__main__':
    application.debug = True
    application.run()
