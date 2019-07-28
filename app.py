import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station
app = Flask(__name__)

@app.route("/")
def home():
    return( 
    f"Available routes below!<br/>"
    f"/api/v1.0/precipitation/<date><br/>"
    f"Data is from 2010-2017. Date after precipitation must include 4 digit year- 2 digit month - 2 digit day ex 2016-01-28.  <br/>"
    f"/api/v1.0/stations<br/>"
    f"/api/v1.0/tobs<br/>"
    f"/api/v1.0/<start><br/>"
    f"Start date only will return the minimum, average and maximum temperature for all dates greater than or equal to the start date<br/>"
    f"/api/v1.0/<start>/<end><br/>"
    f"Start date and end date will return the minimum, average and maximum temperature for dates in between the entered dates.<br/>")
@app.route("/api/v1.0/precipitation/<date>")
def precipitation(date):
    session = Session(engine)
    results = session.query(Measurement.station, Measurement.date, Measurement.prcp, Measurement.tobs).all()
    search_term = str(date)
    for row in results:
        if search_term in row:
            return jsonify(row)
            

@app.route("/api/v1.0/stations")
def stations():
    session=Session(engine)
    results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()
    all_stations = []
    for station, name, latitude, longitude, elevation in results:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        
        all_stations.append(station_dict)



    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def observed():
    session=Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > '2016-08-23' )
    last_year = []
    for date, tobs in results:
        tobs_dict= {}
        tobs_dict['date']= date
        tobs_dict['tobs']= tobs
        last_year.append(tobs_dict)
    return jsonify(last_year)


@app.route("/api/v1.0/<start>")
def start_date(start):
  temps = session.query(func.min(Measurement.tobs),\
    func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).all()
    
  return jsonify(temps)  

@app.route("/api/v1.0/<start>/<end>")
def range_dates(start, end):
  temps = session.query(func.min(Measurement.tobs),\
    func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end).all()
    
  return jsonify(temps)



if __name__ == "__main__":
    app.run(debug=True)


