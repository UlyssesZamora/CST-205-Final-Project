from PIL import Image
import requests
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
import random
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import datetime

# create an instance of Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'csumb-otter'
bootstrap = Bootstrap(app)

class City(FlaskForm):
    city_name = StringField(
        'City Name:', 
        validators=[DataRequired()]
    )
    submit = SubmitField('Submit')

cities = []
def store_song(user_city):
    cities.append(dict(cities = user_city))

base = datetime.datetime.today()

# route decorator binds a function to a URL
@app.route('/', methods = ('GET', 'POST'))
def hello():
    cities.append(dict(cities = 'Marina'))
    form = City()
    if form.validate_on_submit():
        store_song(form.city_name.data)
        return redirect(url_for('.page2', entered_city = cities[-1]['cities']))

    url = "https://api.openweathermap.org/data/2.5/weather?q=Marina&appid=a59706eae8794ea64370ea2d6ab95f7e"
    response = requests.request("GET", url)

    lon = response.json()['coord']['lon']
    lat = response.json()['coord']['lat']

    response = requests.request("GET", 
    url=f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=imperial&appid=a59706eae8794ea64370ea2d6ab95f7e")

    return render_template('index.html', form=form, cities = cities, response = response)

@app.route('/city_forecast/<entered_city>')
def page2(entered_city):

    url = f"https://api.openweathermap.org/data/2.5/weather?q={entered_city}&appid=a59706eae8794ea64370ea2d6ab95f7e"
    response = requests.request("GET", url)
    lon = response.json()['coord']['lon']
    lat = response.json()['coord']['lat']

    response = requests.request("GET", 
    url=f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=imperial&appid=a59706eae8794ea64370ea2d6ab95f7e")

    form = City()
    if form.validate_on_submit():
        store_song(form.city_name.data)
        return redirect(url_for('.page2', entered_city = cities[-1]['cities']))
    return render_template('city_data.html', cities = cities, base = base, 
    response = response, form = form, entered_city = entered_city)

@app.route('/contact')
def contact():
    form = City()
    if form.validate_on_submit():
        store_song(form.city_name.data)
        return redirect(url_for('.page2', entered_city = cities[-1]['cities']))
    return render_template('contact.html', form=form, cities=cities)

@app.route('/images/<city_images>')
def displayImages(city_images):

    url = f'https://pixabay.com/api/?key=23607491-4f8a35a8da7fcbdd1bf29aa18&q={city_images}&image_type=vector%27'
    response = requests.request("GET", url)

    form = City()
    if form.validate_on_submit():
        store_song(form.city_name.data)
        return redirect(url_for('.page2', entered_city = cities[-1]['cities']))
    return render_template('display_images.html', form=form, cities=cities, city_images=city_images, response=response.json())

