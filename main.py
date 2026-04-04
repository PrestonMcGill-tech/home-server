from models import * 
import time


PORT = "/dev/ttyACM0"
DATA_FILE = "weather.json"
DEVICE_FILE = "devices.json"

serial = SerialInterface("Arduino", PORT)
parser = DataParser()
logger = DataLogger()

serial.connect()


while True:
    raw = serial.read()
    parsed = parser.temp(raw)
    if parsed is None:
        continue 
    logger.logToFile(parsed, DATA_FILE)
    time.sleep(30)
