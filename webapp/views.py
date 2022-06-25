from webapp import digiapp
from flask import render_template


@digiapp.route('/')
def index():
    return render_template('index.html')

@digiapp.route('/mechanisms')
def about():
    return render_template('mechanisms.html')

@digiapp.route('/team')
def team():
    return render_template('team.html')