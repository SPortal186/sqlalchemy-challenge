import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False})

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
@app.route("/")
def Home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/station</br>"
        f"/api/v1.0/tobs</br>"
        f"/api/v1.0/start</br>"
        f"/api/v1.0/start/end"

    )


@app.route("/api/v1.0/precipitation")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precipitation and date"""
    # Query all precipitation and date
    p_results = session.query(Measurement.date, (Measurement.prcp)).\
                    filter(Measurement.date >= one_year_ago).\
                    group_by(Measurement.date).all()

    session.close()

    # Convert list of tuples into dictionary
    all_precipitation = []
    for date,prcp in p_results:
        precipitation_dict = {}
        precipitation_dict[date] = prcp
        all_precipitation.append(precipitation_dict)
    
    return jsonify(all_precipitation)


@app.route("/api/v1.0/station")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all passengers
    s_results = session.query(Measurement.station, func.count(Measurement.station)).\
            group_by(Measurement.station).\
            order_by(func.count(Measurement.station).desc()).all()
    
    session.close()

    # Convert list of tuples into dictionary
    all_station = []
    for name,station in s_results:
        station_dict = {}
        station_dict [name] = station
        all_station.append(station_dict)
    return jsonify(all_station)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)    


    # Return a list of temp observation
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= one_year_ago).\
    order_by(Measurement.date.desc()).all()
    session.close()
    all_temperature=[]
    for tobs,date in results:
        tobs_dict={}
        tobs_dict['date']=date
        tobs_dict['tobs']=tobs
        all_temperature.append(tobs_dict)
    return jsonify(all_temperature)


@app.route("/api/v1.0/<start>")
def trip1(start):

 # go back one year from start date and go to end of data for Min/Avg/Max temp   
    start = dt.date(2017, 8, 1)
    end =  dt.date(2017, 8, 7)
    trip_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    trip = list(np.ravel(trip_data))
    return jsonify(trip)

@app.route("/api/v1.0/<start>/<end>")
def trip2(start,end):

  # go back one year from start/end date and get Min/Avg/Max temp     
    start = dt.date(2017, 8, 1)
    end =  dt.date(2017, 8, 7)
    last_year_first_day = start - dt.timedelta(days=365)
    last_year_last_day = end - dt.timedelta(days=365)
    trip_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= last_year_first_day).filter(Measurement.date <= last_year_last_day).all()
    trip = list(np.ravel(trip_data))
    return jsonify(trip)

if __name__ == '__main__':
    app.run(debug=True)     
