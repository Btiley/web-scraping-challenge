from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import Scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")
print("Getting started")

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars = mongo.db.collection.find_one()

    print("Here I Am",mars)

    # Return template and data
    return render_template("index.html", mars=mars)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape_func():

    # Run the scrape function
    mars_data = Scrape_mars.scrape_all()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({},mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True) 