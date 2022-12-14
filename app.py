#====================================================================
# Project 3
#
# Issue Date:  29 Aug 2022
# Submit Date: 19 Sep 2022
#====================================================================
# 1. Import libraries
#====================================================================
import os
import pandas as pd
from flask import (
    Flask,
    render_template)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from db_conn import DB_conn     # db connection key

#=====================================================================
# 2. Flask Setup
#=====================================================================
app = Flask(__name__)

#======================================================================
# 3. Database Setup
#======================================================================

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_conn', '')

# Remove tracking modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

engine = create_engine(DB_conn)
conn = engine.connect()

#=======================================================================
# 4. Create route(s) that render template(s)
#=======================================================================
@app.route("/")
def compare():
    return render_template("compare_region.html")

@app.route("/api/searchRegion")
def search():
    return render_template("search_region.html")

@app.route("/api/policeData")
def policedata():
    return render_template("policedata.html")

#========================================================================
# 5. Define routes to retrieve data from database. These routes can be used/called in any app.js
#========================================================================
# Get unique Region Names
@app.route("/api/getRegionNames")
def getRegNames():
    
    df = pd.read_sql("Select distinct region_name from region_incident group by region_name",engine)
    conn.close()
    
    data = df.to_csv(index=False)
    return data

#==============================================================
# Get Region details
@app.route("/api/getRegionDetails")
def getRegDetails():
    
    df = pd.read_sql("Select * from region_incident order by 1 desc, 2, 4 desc",engine)
    conn.close()
    
    data = df.to_csv(index=False)
    return data

#===============================================================
# Get Offence summary details
@app.route("/api/getTotalByRegion")
def getTotByRegion():
    
    df = pd.read_sql("Select distinct year, region_name, sum(incident_count) from region_incident group by year, region_name order by 1 desc, 2",engine)
    conn.close()
    
    data = df.to_csv(index=False)
    return data

#===============================================================
# Get Offence summary details
@app.route("/api/getOffenceSummary")
def getOffSummary():
    
    df = pd.read_sql("Select * from lga_offence_summary",engine)
    conn.close()
    
    data = df.to_csv(index=False)
    return data

#==========================================================================
# 6. Run app
#==========================================================================
if __name__ == "__main__":
    app.run()
