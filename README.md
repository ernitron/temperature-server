# temperature-server
Temperature Web Server and Daemons for managing Temperature Sensors based on DS18b20. Special for RaspberryPi // C.H.I.P. devices. For ESP8266 there is another project ;)

## Installation

From now on sudo

    pip install requirements.txt
    
To initialize database:

    python DatabaseModel.py
    
## Usage

    python server.py
    
Of course it can be started at boot:

    cp tempserver.sh /etc/init.d
    update-rc.d tempserver.sh defaults
    
    
## See on browser

    http://yourdevice-ip-address:8805
    
## Plotting

Plotting is in place if TemperatureDemon.py is launched regularly. For instance at crontab

    crontab -e
    
Add a line like:

    */5 * * * * /usr/local/bin/tempserver/TemperatureDemon.py --root /usr/local/bin/tempserver

On RPi can also send mqtt messages




