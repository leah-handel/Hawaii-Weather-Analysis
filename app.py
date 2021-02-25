import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

######################################

engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Station = Base.classes.Station
Measurement = Base.classes.Measurement

#####################################

app = Flask(__name__)

@app.route("/")
def home():

@app.route("/api/v1.0/precipitation")
def precipitation():

@app.route("/api/v1.0/stations")
def stations():

@app.route("/api/v1.0/tobs")
def temperature():

@app.route("/api/v1.0/<start>")
def start_date(start):

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):




if __name__ == '__main__':
    app.run(debug=True)