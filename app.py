from flask import Flask, render_template, request
from datetime import datetime
import sqlite3

app = Flask(__name__)


# CREATE DATABASE TABLE
def init_db():

    conn = sqlite3.connect('reports.db')

    cursor = conn.cursor()

    cursor.execute('''

    CREATE TABLE IF NOT EXISTS reports(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        location TEXT,
        issue TEXT,
        time TEXT

    )

    ''')

    conn.commit()
    conn.close()


# HOME PAGE
@app.route('/')
def home():
    return render_template('index.html')


# CONTACT PAGE
@app.route('/contacts')
def contacts():
    return render_template('contacts.html')


# TIPS PAGE
@app.route('/tips')
def tips():
    return render_template('tips.html')


# REPORT PAGE
@app.route('/report', methods=['GET', 'POST'])
def report():

    if request.method == 'POST':

        location = request.form['location']

        issue = request.form['issue']

        time = datetime.now().strftime("%d-%m-%Y %I:%M %p")


        # SAVE TO DATABASE
        conn = sqlite3.connect('reports.db')

        cursor = conn.cursor()

        cursor.execute(

            "INSERT INTO reports(location, issue, time) VALUES(?,?,?)",

            (location, issue, time)

        )

        conn.commit()
        conn.close()


        return render_template(

            'success.html',

            location=location,
            issue=issue,
            time=time,

        )

    return render_template('report.html')

# HISTORY PAGE
@app.route('/history')
def history():

    conn = sqlite3.connect('reports.db')

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM reports")

    reports = cursor.fetchall()

    conn.close()

    return render_template(

        'history.html',

        reports=reports

    )


@app.route('/sos', methods=['POST'])
def sos():

    data = request.get_json()

    latitude = data.get('latitude')
    longitude = data.get('longitude')
    map_link = data.get('map')

    print("\n🚨 EMERGENCY SOS ALERT 🚨")
    print("Latitude:", latitude)
    print("Longitude:", longitude)
    print("Map:", map_link)
    return {"status": "success"}


if __name__ == '__main__':
    init_db()

    app.run(    
        host='0.0.0.0',
        port=5000,
        debug=True
    )
