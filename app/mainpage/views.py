from flask import render_template
from . import portfolio

@portfolio.route('/')
@portfolio.route('/homepage')
def homepage():
    return render_template('homepage.html')



