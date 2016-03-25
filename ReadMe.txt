
Quick Start (This has been tested on a Pi2 running Raspian Jessie, and is using Python 2.7):
First, hook up some supported sensors on to your Pi
Set your Pi up, and make sure that it can see the network and access the I2C bus (I'm running pretty much everything headless)
You may want to hit this link to test your I2C bus:  https://learn.adafruit.com/using-the-bmp085-with-raspberry-pi/overview
Know the IP's of each of your Pi's (beaconing and auto-network detection are not even started)
On each Pi that you want to use, you'll need to run the following commands:
	sudo git clone https://github.com/StaticDet5/PiSensorNode
	sudo git clone https://github.com/adafruit/Adafruit_Python_BMP
	sudo git clone https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code
Then, on the main logging Node (you may only have one, in which case you can runn all of these following on the same Pi):
	sudo python test.py
Finally, on each Pi that is sending data to the main logging Node (if you only have one Node, then run this in a new terminal window or process):
	sudo python Node.py
The sesnor Node will probably ask you a couple of questions to configure the system.  I've tried to make it as painless as possible.  As you proceed
through the configuration, you'll see lines appearing in the Main Logging Node's terminal window. This indicates that it is receiving data.






Sensors supported:
BMP180 (using the Adafruit Adafruit_Python_BMP library)
ADXL345 (using the Adafruit Python Library.  Currently the ADXL345 library needs to be in the SensorNode directory)

Works in progress:
MPL115A2 (using the Adafruit Adafruit_MPL115A2 library)
DS18B20 (custom discovery and drivers to detect and return sensors attached)
PiNetworkMonitor

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


