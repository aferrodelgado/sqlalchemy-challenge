# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import func
import datetime as dt

#################################################
# Database Setup

# Create an app, being sure to pass __name__
app = Flask(__name__)

#Create database engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)

# reflect the tables and save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Routes

@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
        f"Welcome to Honolulu, Hawaii Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs")

@app.route("/api/v1.0/precipitation")
def precipitation():
    #Create session (link) from Python to DB
    session = Session(engine)

    #Calculate last 12 months of precipitation data
    last_date = session.query(func.max(Measurement.date)).scalar()
    last_date = dt.datetime.strptime(last_date, "%Y-%m-%d")
    one_year_ago = last_date - dt.timedelta(days=365)

    #Query last 12 months of precipitation data
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).all()

    #Close session
    session.close()

    #Convert query results to a dictionary
    precipitation_data = {date: prcp for date, prcp in results}
    
    #Return the JSON representation of the dictionary
    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():
    #Create session (link) from Python to DB
    session = Session(engine)

    #Query all stations
    results = session.query(Station.station).all()

    #Close session
    session.close()

    #Convert query results to a list
    stations_list = [station[0] for station in results]

    #Return the JSON representation of the list
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    #Create session (link) from Python to DB
    session = Session(engine)

    #Calculate last 12 months of precipitation data
    last_date = session.query(func.max(Measurement.date)).scalar()
    last_date = dt.datetime.strptime(last_date, "%Y-%m-%d")
    one_year_ago = last_date - dt.timedelta(days=365)

    #Find most active station (station with most temp observations)
    most_active_station = session.query(Measurement.station).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).\
        first()[0]
    
    #Query dates and temp observations for most active station
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station).\
        filter(Measurement.date >= one_year_ago).\
        all()
    
    #Close session
    session.close()

    #Convert query results to list
    temp_data = [{"date": date, "tobs": tobs} for date, tobs in results]

    #Return the JSON representation of the list
    return jsonify(temp_data)

if __name__ == "__main__":
    app.run(debug=True)
