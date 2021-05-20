# Setup bluetooth on raspi

1. Login to raspi: `ssh pi@192.168.1.13`

2. Download and unpack latest BlueZ target: 
```
cd ~
wget http://www.bluez.org/download/
tar xvf bluez-5.37.tar.xz
cd bluez-5.37
```

3. Install dependencies
```
sudo apt-get update
sudo apt-get install -y libusb-dev libdbus-1-dev libglib2.0-dev libudev-dev libical-dev libreadline-dev
```

4. Compile and install BlueZ:
```
./configure --enable-library
make
sudo make install
```

5. Check bluetooth status:
```
systemctl status bluetooth
```

6. Start/Stop BlueZ service manually:
```
sudo systemctl start bluetooth
sudo systemctl stop bluetooth
```

7. Start BlueZ service automatically on startup:
```
sudo systemctl enable bluetooth
```

8. Install bluetooth terminal for raspi:
```
sudo apt-get install minicom -y
```

9. Enable SPP:
```
sudo nano /etc/systemd/system/dbus-org.bluez.service
```
Find line `ExecStart` and add `-C` to the end:
```
ExecStart=/usr/lib/bluetooth/bluetoothd -C
```
Add a new line after this line (`ExecStart`):
```
ExecStartPost=/usr/bin/sdptool add SP
```
Save file and reload config file:
```
sudo systemctl daemon-reload
```
Restart service:
```
sudo systemctl restart bluetooth.service
```

10. Enable bluetooth power:
```
bluetoothctl power on
```

11. Set raspi bluetooth into pairing mode:
```
bluetoothctl
```
Then, in the bluetooth console, type:
```
discoverable on
pairable on
agent on
default-agent
scan on
```

12. Pair with phone, confirm the passcode on raspi. 

13. Listen for incoming connection on raspi:
```
sudo rfcomm watch hci0
```

14. Install and Launch the app "Serial Bluetooth Terminal".

15. In the app, go to "Devices" menu and select the raspi. If everything went ok, following output is displayed in the raspi console:
```
$ sudo rfcomm watch hci0
Waiting for connection on channel 1
Connection from 24:DA:33:85:2A:C3 to /dev/rfcomm0
Press CTRL-C for hangup
```

16. Open another terminal on raspi. Now you can connect the bluetooth terminal application on raspi to the phone:
```
minicom -b 9600 -o -D /dev/rfcomm0
```


## Prevent discoverable mode from turning off
You probably want to change the discoverable mode to not automatically turn off. Therefore, you can edit the bluetooth config file:
```
sudo nano /etc/bluetooth/main.conf
```
Search for the line `DiscoverableTimeout` and set it to `0` (disable timer):
```
DiscoverableTimeout = 0
```
Save the file and restart the bluetooth service:
```
sudo systemctl daemon-reload && sudo systemctl restart bluetooth.service
```
You probably have to reboot the device by `sudo reboot`.
Check for the applied settings by executing 
```
bluetoothctl show
```
If `DiscoverableTimeout: 0x000000b4` has changed to `DiscoverableTimeout: 0x00000000`, the configuration has been applied.

## Fix loading of configuration file
In any case BlueZ wont recognize the changed configuration from `/etc/bluetooth/main.conf`, it may be that it has beed loaded from a different location. Check for the loading path by inspecting the manual:
```
man bluetoothd
```
Under section `FILES`, you should see the config file path `/etc/bluetooth/main.conf`. However, if BlueZ is loading the config from the user settings, the path would be `/usr/local/etc/bluetooth/main.conf`. 
To fix this, we have to create the following symlink and restart the bluetooth service again:
```
cd /usr/local/etc
sudo ln -s /etc/bluetooth bluetooth
sudo systemctl daemon-reload && sudo systemctl restart bluetooth.service
```
You may have to reboot the device again by `sudo reboot`.
With the settings example from previous section (prevent discoverable mode from turning off), check again for the applied settings with:
```
bluetoothctl show
```
The discoverable timeout should now be applied: `DiscoverableTimeout: 0x00000000`.

## Autostart in discoverable mode
If you want to automatically start the bluetooth adapter in discoverable mode, open the local user settings:
```
sudo nano /etc/rc.local
```
Add following lines before the `exit 0` line:
```
# bluetooth settings
sudo bluetoothctl 
power on
discoverable on
pairable on
```
Reboot the device and check if the settings are applied by executing `bluetoothctl show`.


## Commands to connect after restart
If autostart in discoverable mode is not applied, you manually have to start the service and set the modes after each reboot:
```
sudo systemctl start bluetooth
bluetoothctl power on
bluetoothctl discoverable on
```



# More info:
https://scribles.net/setting-up-bluetooth-serial-port-profile-on-raspberry-pi/