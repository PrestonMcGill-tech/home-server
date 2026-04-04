import json 
import serial
import datetime as datetime
import time
 
class Device:
    def __init__(
        self, 
        name: str, 
        dev_id: str , 
        dev_type: str,
        status: str = "offline"
        ):

        self.name : str = name  
        self.dev_id: str = dev_id
        self.dev_type: str = dev_type
        self.status: str = "offline" 

    def __repr__(self): 
        return f"Name: {self.name}\nID: {self.dev_id}\nType: {self.dev_type}\nStatus: {self.status}"

    def to_dict(self):         #not sure if this is necessary or if there is a better way to do it
        data = {
            "deviceName": self.name,
            "deviceId": self.dev_id,
            "deviceType": self.dev_type,
            "status": self.status,
            }
        return data

    @classmethod
    def from_dict(cls, data: dict):
        print(data)
        return cls(
                name=data["deviceName"],
                dev_id=data["deviceId"],
                dev_type=data["deviceType"],
                status=data.get("status", "offline"),
                )

class Registry:
    def __init__(self, device_file: str):
        self.device_file : str = device_file
        self.devices = []
        self.load_devices()
    
    def load_devices(self):
        try:
            with open(self.device_file, 'r') as f:
                raw_data = json.load(f)
        except FileNotFoundError:
            raw_data = {}
        except json.JSONDecodeError:  
            raw_data = {}
        self.devices = {}
        for dev_id, device_data in raw_data.items():
            self.devices[dev_id] = Device.from_dict(device_data)

    def save_devices(self):
        data = {}
        for dev_id, device in self.devices.items():
            data[dev_id] = device.to_dict()

        with open(self.device_file, "w") as f: 
            json.dump(data, f, indent=4)


    def register_device(self, device):
        if device.dev_id in self.devices:
            print(f"Device ID {device.dev_id} already exists.")
            return

        self.devices[device.dev_id] = device
        self.save_devices()
        print(f"Registered devcie {device.name}")

    def create_device(self, data):
        try: 
            device = Device.from_dict(data)
            print("device created")
        
        except Exception as e:
            print("could not create device object")
            device = None 
        
        return device

    def user_get_device_info(self):
        data = input("Device: ") #usr input should be DeviceName DevId DevType with spaces
        dev = data.split()
        device_data = { 
                        "deviceName" : dev[0],
                        "deviceId"   : dev[1],
                        "deviceType" : dev[2]
                        }
        return device_data

    def get_device(self, dev_id: str):
        return self.devices.get(dev_id)

    def remove_device(self, dev_id: str):
        if dev_id in self.devices:
            del self.devices[dev_id]
            self.save_devices()
            print(f"Removed device {dev_id}")
        else:
            print("Device not found")


    def show_devices(self):
        if not self.devices:
            print("No devices registered.")
            return

        for device in self.devices.keys():
            print(device)
            print("-" * 30)

### Types Of Devices 

class Sensor(Device):
    def __init__(self, name,  dev_id, unit, dev_type="sensor", status="offline"):
        super().__init__(name, dev_id, dev_type="sensor", status="offline")
        self.unit = unit


### Logging data 

###temperature things 
class SerialInterface:
    def __init__(self, name, port, baud=9600, timeout=1):
        self.name = name
        self.port = port
        self.baud = baud
        self.timeout = timeout
        self.connected = False
        self.ser = None 

    def connect(self):
        try:
            self.ser = serial.Serial(self.port, self.baud, timeout=self.timeout)
            self.connected = True 
            print(f"{self.name} connected to {self.port} at {self.baud} baud")
        
        except serial.SerialException as e:
            print(f"Failed to connect to port")

    def read(self):
        if not self.connected or self.ser is None:
            print("Not connected. Call connect() first.")
            return 

        data = self.ser.readline()
        return data 

class DataParser:
    def __init__(self):
        pass
         

    def temp(self, data):
        try:
            line = data.decode().strip()
            print(f'parsed line = {line}')
            if not line.startswith("Device_id:"):
                return None 

            parts = line.strip().split()
            if len(parts) != 6:
                   return None 
            
            dev_id = parts[1]
            temp = float(parts[3])
            humidity = float(parts[5])
            
            
            data = {"dev_id": dev_id, "temperature": temp, "humidity": humidity}
            return data

        except Exception as e: # (ValueError, IndexError, AttributeError, TypeError):
            print(F"Parse error: {e}")
            return None

class DataLogger:
    def __init__(self):
        pass 

    def logToFile(self, data, destination):
        if data is None:
            print("Data None value, not writing to memory.")
            return

        try:
            with open(destination, 'r') as f:
                existing = json.load(f)
    
        except (FileNotFoundError, json.JSONDecodeError):
            existing = []

        data["timestamp"] = datetime.datetime.now().isoformat(timespec="seconds")  # add this
        existing.append(data)

        with open(destination, 'w') as f:
            json.dump(existing, f, indent=4)

class Analyser:
    def __init__(self, file):
        self.file = file 

    def latest_reading(self, dev_id : str) -> tuple: 
        with open(self.file) as f:
            data = json.load(f)

        device_reading = [r for r in data if r["dev_id"] == dev_id]

        if not device_reading:
            return None 

        last = device_reading[-1]
        return (last["temperature"], last["humidity"], last["timestamp"])
    
    def device_summary():
        pass

    def plot_history():
        pass
