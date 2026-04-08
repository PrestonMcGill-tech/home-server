import os 
from classes import * 
from dotenv import load_dotenv

load_dotenv()

PORT = os.getenv("SERIAL_PORT")
DB_FILE = os.getenv("DB_FILE")

serial = SerialInterface("Arduino", PORT)
parser = DataParser()
logger = DataLogger(DB_FILE)
db = DataBase(DB_FILE)

serial.connect()

while True:  
        raw = serial.read()
        parsed = parser.temp(raw)
        if parsed is None:
            continue 
        logger.log(parsed)
        time.sleep(30)
    
    



