from flask import Flask, render_template, url_for, request
import requests
from googlesearch.googlesearch import GoogleSearch

listing_params = {
    "item": "Guitar",
    "brand": "Gibson"
}

google_search = GoogleSearch().search(listing_params)

app = Flask(__name__)


@app.route('/')
def show_app():
    return render_template('home.html')


@app.route('/new')
def new_listings():

    return render_template('new_listings.html', google_search=google_search)
