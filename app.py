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
    return(
        "Welcome to my Hawaii weather API!<br><br>"
        "Available Routes:<br><br>"
        "<strong>/api/v1.0/precipitation:</strong> The last year of precipitation measurements in the dataset<br>"
        "<strong>/api/v1.0/stations:</strong> A list of stations in the dataset<br>"
        "<strong>/api/v1.0/tobs:</strong>The last year of temperatures recorded at station USC00519281 <br>"
        "<strong>/api/v1.0/<start_date>:</strong> The minimum, maximum, and average temperatures between the given date and 2017-08-23<br>"
        "<strong>/api/v1.0/<start_date>/<end_date>:</strong> The minimum, maximum, and average temperatures between the given dates.<br><br>"
        "please enter start and stop dates in the format yyyy-mm-dd, ie. 2016-03-14"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    start = dt.datetime(2016, 8, 23, 0, 0)
    year = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > start).all()
    session.close()

    results={}

    for y in year:

        date = y[0]
        precipitation=y[1]

        results[date] = precipitation

    return jsonify(results)
    
    


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station).all()
    session.close()

    station_names=list(results)
    return jsonify(station_names)


@app.route("/api/v1.0/tobs")
def temperature():
    session = Session(engine)
    station = 'USC00519281'
    start_date = dt.datetime(2016, 8, 23, 0, 0)
    results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.station==station).\
    filter(Measurement.date > start_date).all()
    session.close()

    #temps=list(np.ravel(results))
    #return jsonify(temps)

    temps = {}
    key=0

    for r in results:
        temps[key] = [r[0], r[1]]
        key = key+1

    return jsonify(temps)

@app.route("/api/v1.0/<start_date>")
def start_date(start_date):

    try:
        search_date = dt.datetime.strptime(start_date,"%Y-%m-%d")

    except: 
        return "Please enter the start date in the format yyyy-mm-dd, ie. 2016-03-14."

    if search_date <= dt.datetime(2017, 8, 23, 0, 0):
        session = Session(engine)

        min_temp = session.query(func.min(Measurement.tobs).filter(Measurement.date >= search_date)).all()
        max_temp = session.query(func.max(Measurement.tobs).filter(Measurement.date >= search_date)).all()
        avg_temp = session.query(func.avg(Measurement.tobs).filter(Measurement.date >= search_date)).all()

        session.close()

        results = {"minimum temperature": min_temp[0][0], "maximum temperature": max_temp[0][0], "average temperature": avg_temp[0][0]}
        return jsonify(results)

    else:
        return "Please enter a date before 2017-08-23"
    
    



@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end_date(start_date, end_date):
    
    try:
        search_date = dt.datetime.strptime(start_date,"%Y-%m-%d")
        stop_date = dt.datetime.strptime(end_date,"%Y-%m-%d")

    except: 
        return "Please enter the start and end dates in the format yyyy-mm-dd, ie. 2016-03-14."

    if search_date >= stop_date:
        return "start date must be before end date"

    elif search_date <= dt.datetime(2017, 8, 23, 0, 0) and stop_date <= dt.datetime(2017, 8, 23, 0, 0):
        session = Session(engine)

        min_temp = session.query(func.min(Measurement.tobs).filter(Measurement.date >= search_date).filter(Measurement.date <= stop_date)).all()
        max_temp = session.query(func.max(Measurement.tobs).filter(Measurement.date >= search_date).filter(Measurement.date <= stop_date)).all()
        avg_temp = session.query(func.avg(Measurement.tobs).filter(Measurement.date >= search_date).filter(Measurement.date <= stop_date)).all()

        session.close()

        results = {"minimum temperature": min_temp[0][0], "maximum temperature": max_temp[0][0], "average temperature": avg_temp[0][0]}
        return jsonify(results)

    else:
        return "Please enter dates before 2017-08-23"




if __name__ == '__main__':
    app.run(debug=True)