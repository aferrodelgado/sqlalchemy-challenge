# import Flask
from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import func
import datetime as dt

# Create an app, being sure to pass __name__
app = Flask(__name__)

#Create database engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#Reflect exisiting database into new model
Base = automap_base()
Base.prepare(engine, reflect=True)

#Save references to tables
Measurement = Base.classes.measurement
Station = Base.classes.station

#Create session to interact with database
session = Session(engine)

#Define data range for one year ago
most_recent_date = session.query(func.max(Measurement.date)).scalar()
most_recent_date = dt.datetime.strptime(most_recent_date,'%Y-%m-%d')
one_year_ago = most_recent_date - dt.timedelta(days=365)


#Create a precipiation dictionary one year from last date in data set (08/23/16 - 08/23/17 )
precipitation_data = [
    {"date": }
]

# Define what to do when a user hits the index route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
        f"Welcome to Honolulu, Hawaii Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
    )

# Define what to do when a user hits the /api/v1.0/precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server received request for 'Precipitation' page...")
    return jsonify(precipitation_data)

# Define what to do when a user hits the /api/v1.0/stations route
@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'Stations' page...")
    return "Stations page!"

# Define what to do when a user hits the /api/v1.0/tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'Tobs' page...")
    return "Tobs page!"

if __name__ == "__main__":
    app.run(debug=True)
