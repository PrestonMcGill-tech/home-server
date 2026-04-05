from classes import * 
import time


PORT = "/dev/ttyACM0"
DB_FILE = "weather.db"
DEVICE_FILE = "devices.json"

serial = SerialInterface("Arduino", PORT)
parser = DataParser()
logger = DataLogger(DB_FILE)

serial.connect()

while True:
    raw = serial.read()
    parsed = parser.temp(raw)
    if parsed is None:
        continue 
    logger.log(parsed)
    time.sleep(30)
