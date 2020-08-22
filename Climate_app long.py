import numpy as np
import datetime as dt
import sqlalchemy
import statistics
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from statistics import mean 
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Hawaii = Base.classes.keys
Station=Base.classes.station
Measurement=Base.classes.measurement
#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

   
    # Query all prcp
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

   # Create a dictionary from the row data and append to a list of all_prcp
    all_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["precipitation"] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(Station.name).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

        
   
    # Convert list of tuples into normal list
    recent_date=session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    recent_date=dt.date(2017,8,23)
    year_ago=recent_date-dt.timedelta(days=365)
    yearly=session.query(Measurement.station, Measurement.date, Measurement.prcp, Measurement.tobs).\
    filter(Measurement.station=='USC00519281', Measurement.date >=year_ago).all()
   

    session.close()
    all_tobs = list(np.ravel(yearly))

    return jsonify(all_tobs)


@app.route("/api/v1.0/<start>")
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    temp=[Measurement.date,
        func.count(Measurement.tobs),
        func.max(Measurement.tobs),
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs)]
    temp=session.query(*temp).\
        filter (Measurement.date>=start).all()

    # temp=session.query(Measurement.date,Measurement.tobs).\
    #     filter (Measurement.date>=start).all() 
    # avg=[Measurement.date,
    #     func.count(Measurement.tobs),
    #     func.max(Measurement.tobs),
    #     func.min(Measurement.tobs),
    #     func.avg(Measurement.tobs)]
    # out=session.query(*avg).all()
          

    # start_date=session.query(Measurement.date, Measurement.tobs).\
    # filter(Measurement.date >=start).all()

   
    # print(start_date)
    # sum=0
    # for each_line in start_date: 
    #     sum=sum+(each_line[1])
    # avg_temp=sum/len(start_date)
    # max_temp=max(start_date)[1]
    # min_temp=min(start_date)[1]
    # avg_temp=func.mean(start_date)
    # sum_temp=sum(start_date)[1]
    # count=len(start_date)[1]
    # avg_temp=sum_temp/count

    # print(max_temp)
    # avg_data = []
    # for tobs in start_date:
    #     avg_dict = {}
    #     max_dict["Max Temp"] = max(start_date)[3]
    #     min_dict["Min Temp"] = min(start_date)[3]
    #     ave_dict["Ave Temp"] = mean(start_date)[3]
    #     avg_data.append(avg_dict)  

    session.close()
    # avg_temp = list(np.ravel(avg_data))

    # return jsonify(max_temp, min_temp, avg_temp)
    return jsonify(temp)



if __name__ == '__main__':
    app.run(debug=True)