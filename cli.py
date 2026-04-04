import datetime
from models import *

DEVICE_FILE = "devices.json"
DATA_FILE = "weather.json"

def print_home(registry: Registry):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    online  = sum(1 for d in registry.devices.values() if d.status == "online")
    offline = sum(1 for d in registry.devices.values() if d.status == "offline")
    total   = len(registry.devices)

    print()
    print("=" * 45)
    print("        DEVICE MANAGER")
    print(f"        {now}")
    print("=" * 45)
    print(f"  Devices : {total}  |  Online : {online}  |  Offline : {offline}")
    print("=" * 45)
    print()
    print("  [1] List devices")
    print("  [2] Register device")
    print("  [3] Remove device")
    print("  [4] Read sensor")
    print("  [5] Weather")
    print("  [q] Quit")
    print()
    print("=" * 45)

def select_sensor(registry: Registry):
    sensors = {
        dev_id: device
        for dev_id, device in registry.devices.items()
        if device.dev_type == "sensor"
    }
 
    if not sensors:
        print("\n  No sensors registered.")
        input("\n  Press Enter to continue...")
        return
 
    while True:
        print()
        print("=" * 45)
        print("        SELECT SENSOR")
        print("=" * 45)
 
        sensor_list = list(sensors.values())
        for i, sensor in enumerate(sensor_list, start=1):
            print(f"  [{i}] {sensor.name}  ({sensor.dev_id})")
 
        print()
        print("  [b] Back")
        print()
        print("=" * 45)
 
        choice = input("  Select sensor: ").strip().lower()
 
        if choice == "b":
            return
 
        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(sensor_list):
                sensor = sensor_list[index]
                sensor_summary(sensor)
            else:
                print("\n  Invalid selection.\n")
        else:
            print("\n  Invalid input.\n")

def sensor_summary(sensor):
    while True:
        print()
        print("=" * 45)
        print(f"        {sensor.name.upper()}")
        print(f"        {sensor.dev_id}  |  type: {sensor.dev_type}")
        print("=" * 45)
        print()
        print("  [1] Latest reading")
        print("  [2] Today's summary  (coming soon)")
        print("  [3] Plot history     (coming soon)")
        print()
        print("  [b] Back")
        print()
        print("=" * 45)
 
        choice = input("  Select option: ").strip().lower()
 
        if choice == "b":
            return
 
        elif choice == "1":
            latest_reading(sensor)
 
        elif choice in ("2", "3"):
            print("\n  Not yet implemented.\n")
            input("  Press Enter to continue...")
 
        else:
            print("\n  Invalid input.\n")
 

def list_devices(registry: Registry):
    print()
    if not registry.devices:
        print("  No devices registered.")
        return

    print(f"  {'NAME':<20} {'ID':<10} {'TYPE':<10} {'STATUS'}")
    print("  " + "-" * 50)
    for device in registry.devices.values():
        print(f"  {device.name:<20} {device.dev_id:<10} {device.dev_type:<10} {device.status}")
    print()


def main():
    registry = Registry(DEVICE_FILE)
    registry.show_devices()

    analyser = Analyser(DATA_FILE)

    print_home(registry)
    while True:
        choice = input("  Enter command: ").strip().lower()

        if choice == "1":
            list_devices(registry)
            input("  Press Enter to continue...")

        elif choice == "2":
            print("Register Device: Name | dev_id | dev_type ")
            data = registry.user_get_device_info()
            device = registry.create_device(data)
            registry.register_device(device)
        
        elif choice == "3":
            list_devices(registry)
            dev = input("(D) Device ID: ")
            registry.remove_device(dev)

        elif choice == "4":
            select_sensor(registry)

        elif choice == "5":
            temp, hum, time = analyser.latest_reading("001")
            print(f"{time} - temperature: {temp}, humidity: {hum}")

        elif choice == "Quit":
            print("\n  Goodbye.\n")
            break

        else:
            print("\n  Command not yet implemented.\n")
            input("  Press Enter to continue...")



if __name__ == "__main__":
    main()

