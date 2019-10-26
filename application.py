from flask import Flask, render_template
from datetime import datetime
from json import loads
application = Flask(__name__)

@application.route('/')
def about():
    with open('data/skills.json') as skills_f:
        skills = loads(skills_f.read())

    return render_template('index.html', year=datetime.now().year, skills=skills['skills'])

if __name__ == '__main__':
    application.debug = True
    application.run()
