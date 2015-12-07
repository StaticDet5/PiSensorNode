Sensors supported:
BMP180 (using the Adafruit Adafruit_Python_BMP library)

Works in progress:
MPL115A2 (using the Adafruit Adafruit_MPL115A2 library)
DS18B20 (custom discovery and drivers to detect and return sensors attached)


I set a fixed IP address for this project, just so I didn't have to chase
things around on my network.
I changed the hostnames.

You're going to need to have Python 2.x, I used 2.7 to write this.

install pip
sudo apt-get install python-setuptools
sudo easy_install pip

install pygal
pip install pygal

install cairosvg for PNG support
sudo apt-get install python-cairosvg
sudo apt-get install python-lxml
sudo apt-get install python-cssselect
sudo pip install tinycss


