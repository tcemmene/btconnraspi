import time
from bluetoothctl import Bluetoothctl

def init():

    print("Init bluetooth...")
    bl = Bluetoothctl()
    bl.disable_power()
    bl.enable_power()
    bl.reset_agent()
    bl.set_agent("NoInputNoOutput")
    bl.set_agent_as_default()
    bl.make_discoverable()
    bl.make_pairable()
    return bl

def scan(bl):    
    bl.start_scan()
    print("Scanning for 10 seconds...")
    for i in range(0, 8):
        print(i)
        time.sleep(1)

    print("Discoverable")
    discoverable_devices = bl.get_discoverable_devices()
    for device in discoverable_devices:
        print(device)
        
    print("Available")
    available_devices = bl.get_available_devices()
    for device in available_devices:
        print(device)

def pair(bl, mac):
    bl.start_agent()
    bl.pair(mac)	

def main():
    bl = init()
    print("Ready!")
	
    scan(bl)
    #pair('<mac_address>')

if __name__ == "__main__":
    main()	