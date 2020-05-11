from datetime import datetime
#from email.message import EmailMessage
from flask import Flask, flash, render_template, request, redirect, url_for
from os import environ
from smtplib import SMTP_SSL
from ssl import create_default_context
from wtforms import Form, StringField, SubmitField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, length

from benjilevinecom.models import db, Skill, Project, About


def create_application():
    application = Flask(__name__)
    application.secret_key = environ['FLASK_SECRET_KEY']
    sqlalchemy_database_uri = (
        'mysql+mysqlconnector://{}:{}@{}:{}/benjilevine.com'.format(
            environ['BENJI_LEVINE_DB_USERNAME'],
            environ['BENJI_LEVINE_DB_PASSWORD'],
            environ['BENJI_LEVINE_DB_HOST'],
            environ['BENJI_LEVINE_DB_PORT']
        )
    )
    application.config['SQLALCHEMY_DATABASE_URI'] = sqlalchemy_database_uri
    application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(application)
    return application


app = create_application()


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


@app.route('/', methods=['POST', 'GET'])
def about():
    skills = Skill.query.all()
    about_data = About.query.order_by(About.priority).all()
    projects = Project.query.order_by(Project.priority).all()

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
                           about=about_data,
                           projects=projects,
                           skills=skills,
                           form=form
                           )


def send_message(name, email, message):
    send_to = 'contactform@benjilevine.com'

    #msg = EmailMessage()
    #msg.set_content(message)
    #msg['Subject'] = name + ' - benjilevine.com Contact Form'
    #msg['From'] = email
    #msg['To'] = send_to

    #sender = SMTP_SSL(
    #    environ['BENJI_LEVINE_SMTP_HOST'],
    #    environ['BENJI_LEVINE_SMTP_PORT'],
    #    'benjilevine.com'
    #)

    #sender.login(
    #    environ['BENJI_LEVINE_SMTP_USERNAME'],
    #    environ['BENJI_LEVINE_SMTP_PASSWORD']
    #)

    #sender.send_message(msg)
    #sender.quit()

    context = create_default_context()
    with SMTP_SSL(
        environ['BENJI_LEVINE_SMTP_HOST'],
        environ['BENJI_LEVINE_SMTP_PORT'],
        context=context
        ) as server:
        
        server.login(
            environ['BENJI_LEVINE_SMTP_USERNAME'],
            environ['BENJI_LEVINE_SMTP_PASSWORD']
        )
        server.sendmail(
            email,
            send_to,
            message
        )





if __name__ == '__main__':
    app.debug = True
    app.run()
