from webapp import digiapp
from flask import render_template


@digiapp.route('/')
def index():
    return render_template('index.html')

@digiapp.route('/mechanisms')
def about():
    return "About"

@digiapp.route('/team')
def team():
    return "Team tab here"