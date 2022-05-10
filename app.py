from flask import Flask, render_template, url_for, redirect
from flask_pymongo import PyMongo
import Scraping

# this sets up Flask
app = Flask(__name__)

# use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route('/')
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

# setting up the scraping route
@app.route("/scrape")
# below allows us to access the database, scrape new data using our Scraping.py
# script, update the database, and return a message when successful
def scrape():
    mars = mongo.db.mars
    mars_data = Scraping.scrape_all()
    mars.update_one({}, {"$set":mars_data}, upsert=True)
    return redirect('/', code=302)

if __name__ == "__main__":
    app.run()

