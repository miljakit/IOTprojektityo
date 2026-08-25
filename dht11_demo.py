import time
import datetime
import seeed_dht

sensor = seeed_dht.DHT("11", 12)
print("DHT11 reading every hour, Ctrl+C to quit")
file = open("mittaukset.txt", "w")
measurement = {}

try:
	while True:
		time_now = datetime.datetime.now()
		#if time_now.minute == 0 and 
		if time_now.second == 0:
			humi, temp = sensor.read()
			file = open("mittaukset.txt", "w")
			measurement = {}
			measurement["time"] = time_now
			measurement["temperature"] = temp
			measurement["humidity"] = humi
			row = str(measurement["time"]) + " " + str(measurement["temperature"]) + " " + str(measurement["humidity"])
			file.write(row + "\n")
			file.close()

			print(f"DHT11 Humidity {humi:.1f}% Temperature {temp:.1f}C")
			time.sleep(1)
except KeyboardInterrupt:
	print("\nBye")

