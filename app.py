from mars_scrape import scrapeAll
from flask import Flask, render_template, redirect

# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
import pymongo

# Create an instance of our Flask app.
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = client.scrape_hw_db

# Drops collection if available to remove duplicates
# db.scrape.drop()

# Creates a collection in the database and inserts two documents
# db.scrape.insert_many(scrapeAll)

# Set route
@app.route('/')
def index():
    # Store the entire team collection in a list
    mars_data = db.scrape.find_one()
    print(mars_data)

    # Return the template with the teams list passed in
    return render_template('index.html', data=mars_data)

@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_data = scrapeAll()

    # Update the Mongo database using update and upsert=True
    db.scrape.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)

