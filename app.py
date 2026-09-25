from flask import Flask, request, Response, render_template, jsonify # pip install Flask
import json
from flask_cors import CORS, cross_origin # pip install flask-cors
import sqlite3

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

#measurements = []

DB_PATH = "/home/data/sensoridata.db"

@app.route("/")
def home():
    return render_template('index.html')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mittaukset (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aika DATETIME DEFAULT CURRENT_TIMESTAMP,
        lampotila REAL,
        kosteus REAL
        )
    """)

    conn.commit()
    conn.close()

@app.route("/api/measurement", methods=["POST"])
def get_measurement():
    data = request.get_json()
    temp = data[0]
    humi = data[1] 

    #measurements.append(data)
    print("saatiin mittaus")
    print(data)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
            INSERT INTO mittaukset (temp, humi)
            VALUES (?, ?)
            """, (temp, humi))
    conn.commit()
    conn.close()
            
    data_json = json.dumps(data)

    return data_json

@app.route("/api/showmeasurements")
def show_measurements():
    paivamaara = request.args.get("date")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT aika, lampotila, kosteus
        FROM mittaukset
        WHERE date(aika) = ?
        ORDER BY aika
    """, (paivamaara,))
    
    rows = cursor.fetchall()
    conn.close()
    
    return jsonify(rows)
    
@app.route("/api/latestmeasurements")
def latest_measurements():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT aika, lampotila, kosteus
        FROM mittaukset
        WHERE datetime(aika) >= datetime('now', '-6 hours')
        ORDER BY aika
    """)
        
    rows = cursor.fetchall()
    conn.close()
        
    return jsonify(rows)
    
@app.route("/api/availabledates")
def available_dates():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT DISTINCT date(aika)
        FROM mittaukset
        ORDER BY date(aika)
    """)
    
    dates = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(dates)

@app.route("/api/testdb")
def test_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM mittaukset
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return jsonify(rows)

init_db()

if __name__ == "__main__":
    app.run(debug=True)
    
