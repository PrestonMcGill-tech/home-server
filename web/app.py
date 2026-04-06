from flask import Flask, jsonify, render_template 
from classes import Analyser 

DB_FILE = "/app/data/weather.db"
analyser = Analyser(DB_FILE)

app = Flask(__name__)

@app.route('/')
def home():
    reading = analyser.latest_reading("001")
    if reading is None:
        return render_template('index.html', reading=None)
    return render_template('index.html', reading={"temperature": reading[0], "humidity": reading[1], "timestamp": reading[2]})

@app.route('/api/weather')
def weather():
    reading = analyser.latest_reading("001")
    if reading is None:
        return jsonify({"error": "No data"}), 404
    return jsonify({"temperature": reading[0], "humidity": reading[1], "timestamp": reading[2]})

@app.route('/api/weather/history')
def weather_history():
    reading = analyser.all_readings("001")
    return jsonify(reading)

if __name__ == '__main__':
    app.run(debug=True)
