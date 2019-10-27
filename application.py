from datetime import datetime
from email.message import EmailMessage
from flask import Flask, flash, render_template, request, redirect, url_for
from os import environ
from smtplib import SMTP_SSL
from wtforms import Form, StringField, SubmitField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, length

from models import db, About, Skill


def create_application():
    app = Flask(__name__)
    app.secret_key = environ['FLASK_SECRET_KEY']
    sqlalchemy_database_uri = (
        'mysql+mysqlconnector://{}:{}@{}:{}/benjilevine.com'.format(
            environ['BENJI_LEVINE_DB_USERNAME'],
            environ['BENJI_LEVINE_DB_PASSWORD'],
            environ['BENJI_LEVINE_DB_HOST'],
            environ['BENJI_LEVINE_DB_PORT']
        )
    )
    app.config['SQLALCHEMY_DATABASE_URI'] = sqlalchemy_database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    return app


application = create_application()


class ContactForm(Form):
    name = StringField('Name',
                       validators=[DataRequired(), length(max=200)],
                       render_kw={
                           "placeholder": "Name",
                           "class": "input",
                           "maxlength": 200
                       })
    email = EmailField('Email Address',
                       validators=[
                           DataRequired(),
                           Email(message="Invalid email address"),
                           length(max=200)
                       ],
                       render_kw={
                           "placeholder": "Email",
                           "class": "input",
                           "maxlength": 200
                       })
    message = TextAreaField('Message',
                            validators=[DataRequired(), length(max=5000)],
                            render_kw={
                                "placeholder": "Enter your message here...",
                                "class": "textarea",
                                "rows": 5,
                                "maxlength": 5000
                            })
    submit = SubmitField('Send',
                         render_kw={
                             "class": "button is-link"
                         })


@application.route('/', methods=['POST', 'GET'])
def about():
    skills = Skill.query.all()
    about = About.query.order_by(About.priority).all()

    form = ContactForm(request.form)
    if request.method == 'POST':
        if form.validate():
            send_message(form.name.data, form.email.data, form.message.data)
            flash('Message successfully sent!')
        else:
            flash('Invalid data supplied, message not sent.')
        return redirect(url_for('about', _anchor='contact'))

    return render_template('index.html',
                           year=datetime.now().year,
                           about=about,
                           skills=skills,
                           form=form
                           )


def send_message(name, email, message):
    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = name + ' - benjilevine.com Contact Form'
    msg['From'] = email
    msg['To'] = 'contactform@benjilevine.com'

    sender = SMTP_SSL(
        environ['BENJI_LEVINE_SMTP_HOST'],
        environ['BENJI_LEVINE_SMTP_PORT'],
        'benjilevine.com'
    )

    sender.login(
        environ['BENJI_LEVINE_SMTP_USERNAME'],
        environ['BENJI_LEVINE_SMTP_PASSWORD']
    )

    sender.send_message(msg)
    sender.quit()


if __name__ == '__main__':
    application.debug = True
    application.run()
