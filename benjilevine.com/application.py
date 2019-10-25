from flask import Flask, render_template
from datetime import datetime
app = Flask(__name__)

@app.route('/')
def about():
    return render_template('index.html', year=datetime.now().year)

