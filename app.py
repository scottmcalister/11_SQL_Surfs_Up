from flask import Flask, jsonify

import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

app = Flask(__name__)

engine = create_engine("sqlite:///hawaii.sqlite")
Base=automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurements
Station = Base.classes.stations 

session = Session(engine)

@app.route("/")
def home():
	print("requested: Home page")
	return("Welcome to the Surf's Up Weather API!")

@app.route("/welcome")
def welcome():
	return(
		f"Welcome to the Surf's Up API <br>"
		f"Available Routes: <br>"
		f"/api/v1.0/precipitation <br>"
		f"/api/v1.0/stations<br>"
		f"/api/v1.0/tobs <br>"
		f"/api/v1.0/temp/start/end"
		)
@app.route("/api/v1.0/precipitation")
def precipitation():
	p_year = dt.datetime.today() - dt.timedelta(days=365)
	precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= p_year).all()
	precipitat = {date: prcp for date, prcp in precipitation}
	return jsonify(precipitat)

@app.route("/api/v1.0/stations")
def stations():
	response=session.query(Station.station).all()
	statns = list(np.ravel(results))
	return jsonify(statns)

@app.route("/api/v1.0/tobs")
def temp():
	p_year = dt.date.today() - dt.timedelta(days=365)
	response = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= p_year).all()

	temps = list(np.ravel(results))
	return jsonify (temps)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def date_stat(start, end):
	select = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
	if not end:
		response = session.query(*select).filter(Measurement.date >= start).all()
		temper = list(np.ravel(response))
		return jsonify(temper)

	response = session.query(*select).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
	temper = list(np.ravel(response))
	return jsonify(temper)

if __name__  ==  '__main__':
	app.run()















