import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

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
        "/api/v1.0/precipitation<br>"
        "/api/v1.0/stations<br>"
        "/api/v1.0/tobs<br>"
        "/api/v1.0/<start><br>"
        "/api/v1.0/<start>/<end><br>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    pass

@app.route("/api/v1.0/stations")
def stations():
    pass

@app.route("/api/v1.0/tobs")
def temperature():
    pass

@app.route("/api/v1.0/<start>")
def start_date(start):
    pass

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    pass




if __name__ == '__main__':
    app.run(debug=True)