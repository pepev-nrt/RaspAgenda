# Installation

There are some python libraries that are necesary for this project. I recommend creating a virtual enviroment to have all of those libraries isolated from your system packages.

You can install them using the `requirements.txt` or just with `pip install <library>`.
I've tested both methods and both works, in case any library is updated and gives any problem, the `requirements.txt` should still work.

### `requirements.txt` method

```
cd /path/to/project
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
deactivate
```

### `pip install <library>` method

```
cd /path/to/project
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip

# Required for the waveshare library
pip install Pillow numpy spidev

# Required to interact with the gpio pins and the screen
pip install gpiozero rpi.gpio lgpio

# Required to connect to the caldav server
pip install caldav

# Required to use the open-meteo API
pip install openmeteo-requests
pip install requests-cache retry-requests numpy pandas 

deactivate
```

https://open-meteo.com/en/docs
https://www.waveshare.com/wiki/2.13inch_e-Paper_HAT+#Working_With_Raspberry_Pi
https://pypi.org/project/caldav/

