import os
from flask import Flask, render_template, request
from snowflake import connector
import pandas as pd

app = Flask("my website")

@app.route('/')
def homepage():
    # send dataframe html to template
    return render_template('index.html', dfhtml=dfhtml)

@app.route('/submit')
def submitpage():
    return render_template('submit.html')

@app.route('/thanks4submit', methods=["POST"])
def thankspage():
    colorName = request.form.get("cname")
    userName = request.form.get("uname")
    return render_template('thanks4submit.html',
                           colorName=colorName,
                           userName=userName)


#Snowflake stuff  - get sensitive deets from env variable
cnx = connector.connect(
    account = os.getenv('SF_GCP_ACCNT'),
    user = os.getenv('SF_GCP_USR'),
    password = os.getenv('SF_GCP_PWD'),
    warehouse ='compute_wh',
    database='demo_db',
    schema='public',
    role='sysadmin'
)

cur = cnx.cursor()
cur.execute("SELECT * from COLORS")

rows=pd.DataFrame(cur.fetchall(), columns=['COLOR_UID','COLOR_NAME'])

# dataframe as html
dfhtml=rows.to_html()

app.run()