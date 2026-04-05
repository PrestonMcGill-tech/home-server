from flask import Flask, jsonify, render_template 
import json 
DATA_FILE = "weather.json"


app = Flask(__name__)

def get_latest():
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    return data[-1]

@app.route('/')
def home():
    reading = get_latest()
    return render_template('index.html', reading=reading)

@app.route('/api/weather')
def weather():
    reading = get_latest()
    return jsonify(reading)

@app.route('/api/weather/history')
def weather_history():
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
