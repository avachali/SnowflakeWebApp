#Imports
from flask import Flask, render_template, request
import pandas as pd
from snowflakeConnection import sfConnect

app = Flask("Snowflake colors")

#Routes
@app.route('/')
def homepage():

    #Get data from color table
    cur = cnx.cursor().execute("select color_name, count(*) "
                                "from demo_db.public.colors "
                                "group by color_name "
                                "having count(*)>50 "
                                "order by count(*) desc ;")

    rows = pd.DataFrame(cur.fetchall(), columns=['COLOR_NAME', 'Votes'])

    # dataframe as html
    dfhtml = rows.to_html(index=False)
    # send dataframe html to template
    return render_template('index.html', dfhtml=dfhtml)

@app.route('/submit')
def submitpage():
    return render_template('submit.html')

@app.route('/thanks4submit', methods=["POST"])
def thankspage():
    colorName = request.form.get("cname")
    userName = request.form.get("uname")
    #insert into db
    cnx.cursor().execute("INSERT INTO COLORS(COLOR_UID, COLOR_NAME) " +
                         "SELECT COLOR_UID_SEQ.nextval, '" + colorName + "'")

    return render_template('thanks4submit.html',
                           colorName=colorName,
                           userName=userName)

@app.route('/coolcharts')
def coolcharts():

    # Get account Name
    cur = cnx.cursor().execute("select current_account()")
    accntName = cur.fetchone()

    cur = cnx.cursor().execute("select color_name, count(*) "
                               "from demo_db.public.colors "
                               "group by color_name "
                               "order by count(*) desc ;")

    data4charts = pd.DataFrame(cur.fetchall(), columns=['color', 'votes'])

    data4chartsJSON = data4charts.to_json(orient='records')
    return render_template('coolcharts.html', data4chartsJSON=data4chartsJSON, accntName=accntName)

# SF connect
cnx = sfConnect()

app.run()