from datetime import datetime
from email.message import EmailMessage
from flask import Flask, flash, render_template, request, redirect, url_for
from flask_recaptcha import ReCaptcha
from os import environ
from smtplib import SMTP_SSL, SMTPRecipientsRefused
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

    application.config['RECAPTCHA_SITE_KEY'] = "6LccavsUAAAAALU3A0-Z7Q6YquHvk67gm4Uobwzc"
    application.config['RECAPTCHA_SECRET_KEY'] = "6LccavsUAAAAAMrQsvYaOoOVUzFBmAPlhdxy655_"

    db.init_app(application)
    return application


app = create_application()
recaptcha = ReCaptcha(app=app)

info = {
    'title' : 'Max Levine',
    'fname' : 'Max',
    'email' : 'max@maxlevine.co.uk',
    'linkedin' : 'https://www.linkedin.com/in/benjilevine/',
    'github' : 'https://github.com/benjilev08',
    'cv_file' : 'assets/Benji_Levine_CV.pdf',
    'main_photo' :  'assets/portrait.jpeg',
    'second_photo' : 'assets/Madrid.jpg',
    'logo' : 'assets/logo.png'
}

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
        if form.validate() and recaptcha.verify():
            try:
                send_message(form.name.data, form.email.data, form.message.data)
                flash('Message successfully sent!')
            except SMTPRecipientsRefused as e:
                flash('Invalid email address entered. Message not sent.')
                email_bug_report(
                    form.name.data,
                    form.email.data,
                    form.message.data,
                    e
                )
            except Exception as e:
                flash('Unknown error occurred. Message not sent.')
                email_bug_report(
                    form.name.data,
                    form.email.data,
                    form.message.data,
                    e
                )
        elif not form.validate():
            flash('Invalid data supplied, message not sent.')
        elif not recaptcha.verify():
            flash('Bot suspected, message not sent.')
        else:
            # flash(str(form.errors))
            # This condition should never be reached
            flash('Error occurred, message not sent.')
        return redirect(url_for('about', _anchor='contact'))

    return render_template('index.html',
                           year=datetime.now().year,
                           about=about_data,
                           projects=projects,
                           skills=skills,
                           form=form,
                           **info
                           )


def send_message(name, email, message, subject=None):
    send_to = 'contactform@benjilevine.com'

    s = SMTP_SSL(
        environ['BENJI_LEVINE_SMTP_HOST'],
        environ['BENJI_LEVINE_SMTP_PORT']
    )

    s.login(
        environ['BENJI_LEVINE_SMTP_USERNAME'],
        environ['BENJI_LEVINE_SMTP_PASSWORD']
    )

    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = f'{name} - benjilevine.com Contact Form' if subject is None else subject
    #msg['From'] = send_to
    #msg['From'] = name + ' <' + email + '>'
    msg['From'] = email
    msg['To'] = send_to
#    msg['Reply-To'] = name + ' <' + email + '>'

    s.send_message(msg)
    s.quit()


def email_bug_report(name, email, message, error):
    e_from = 'website@benjilevine.com'
    subject = 'Bug Report - benjilevine.com'
    message = (
        f'Name: {name}\n' +
        f'From: {email}\n' +
        f'Message: {message}\n' +
        f'Error: {error}'
    )

    send_message('Bug Report', e_from, message, subject=subject)


if __name__ == '__main__':
    app.debug = True
    app.run()
