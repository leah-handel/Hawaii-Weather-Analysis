import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import datetime as dt
import numpy as np

from flask import Flask, jsonify

######################################

engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Station = Base.classes.station
Measurement = Base.classes.measurement

#####################################

app = Flask(__name__)

@app.route("/")
def home():
    print("someone is accessing my homepage")
    return(
        "Welcome to my Hawaii weather API!<br><br>"
        "Available Routes:<br><br>"
        "<strong>/api/v1.0/precipitation:</strong> The last year of precipitation measurements in the dataset<br>"
        "<strong>/api/v1.0/stations:</strong> A list of stations in the dataset<br>"
        "<strong>/api/v1.0/tobs:</strong><br> The last year of temperatures recorded at station USC00519281"
        "/api/v1.0/<start_date><br>"
        "/api/v1.0/<start_date>/<end_date><br>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    start_date = datetime.datetime(2016, 8, 23, 0, 0)
    year = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > start_date).all()
    session.close()

    results={}
    for y in year:
        date = y.date
        precipitation=y.prcp
        results["date"].append(precipitation)
    
    


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station).all()
    session.close()

    station_names=np.ravel(results)
    return jsonify(station_names)


@app.route("/api/v1.0/tobs")
def temperature():
    session = Session(engine)
    station = 'USC00519281'
    start_date = datetime.datetime(2016, 8, 23, 0, 0)
    results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.station==station).\
    filter(Measurement.date > start_date).all()
    session.close()

    active_temps=np.ravel(results)
    return jsonify(active_temps)

@app.route("/api/v1.0/<start>")
def start_date(start):
    pass

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    pass




if __name__ == '__main__':
    app.run(debug=True)