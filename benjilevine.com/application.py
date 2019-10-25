from flask import Flask, render_template
from datetime import datetime
application = Flask(__name__)

@application.route('/')
def about():
    return render_template('index.html', year=datetime.now().year)

