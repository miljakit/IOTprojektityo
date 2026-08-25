import requests # pip install requests
import time
from datetime import datetime
import seeed_dht
import json
import sqlite3

sensor = seeed_dht.DHT("11", 12)
conn = sqlite3.connect("sensoridata.db")
cursor = conn.cursor()
print("DHT11 reading every hour, Ctrl+C to quit")

try:
	while True:
		if datetime.now().minute == 0:
			timestamp_ms = int(datetime.now().timestamp()*1000)
			humi, temp = sensor.read()
			print(f"DHT11  Humidity {humi:.1f}%  Temperature {temp:.1f}C")
			cursor.execute("""
			INSERT INTO mittaukset (lampotila, kosteus)
			VALUES (?, ?)
			""", (temp, humi))
			conn.commit()

			data = [timestamp_ms, temp, humi]
			response = requests.post("http://127.0.0.1:5000/api/measurement", json=data)

			print(response)
			time.sleep(60)

except KeyboardInterrupt:
    print("\nBye")

conn.close()
