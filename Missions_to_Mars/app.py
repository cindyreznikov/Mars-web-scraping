from flask import Flask, render_template
import pymongo
import scrape_mars

#  Flask Setup
app = Flask(__name__)

# create connection variable
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)


@app.route("/")
def echo():
    return render_template("index.html, text="dont know what to put here")

@app.route("/scrape")
def scrape():
    mars_data = scrape_mars.scrape()

if __name__ == "__main__":
    app.run(debug=True)