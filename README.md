# temperature-server
Temperature Web Server and Daemons for managing Temperature Sensors based on DS18b20. Special for RaspberryPi // C.H.I.P. devices. For ESP8266 there is another project ;)

## Installation

From now on sudo. 

Download and copy all source files in the destination directory. I.e. execute this on your RPi or CHIP device 

    mkdir -p /usr/local/bin/temp-server
    cd /usr/local/bin/temp-server
    git clone https://github.com/ernitron/temperature-server

Install requirements

    pip install -r requirements.txt
    
To initialize database:

    python DatabaseModel.py
    
## Usage

    python server.py
    
Of course it can be started at boot:

    cp tempserver.sh /etc/init.d
    update-rc.d tempserver.sh defaults
    
## 1 Wire setup at boot in the kernel 

Add to /boot/config.txt the following line:

    dtoverlay=w1-gpio,pullup="y"

Modprobe with:

        # sudo modprobe w1_gpio pullup=1
        # sudo modprobe w1_therm strong_pullup=1 (or =2)

In Raspberry PI: 1-Wire Default reading is on GPIO 4
In C.H.I.P. : 1-Wire is on LCD-D2 

    
## See on browser

    http://yourdevice-ip-address:8805
    
## Plotting

Plotting is in place if TemperatureDemon.py is launched regularly. For instance at crontab

    crontab -e
    
Add a line like:

    */5 * * * * /usr/local/bin/tempserver/TemperatureDemon.py --root /usr/local/bin/tempserver

On RPi can also send mqtt messages


## Disclaimer

Sorry but the server was not intended to serve anyone else but me and my personal sensor network of IoT device in my house. I can not be of much support. Sorry.




