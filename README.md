# NMEA Analyzer  [![Build Status](https://travis-ci.org/embest/nmeaanalyzer.svg?branch=master)](https://travis-ci.org/embest/nmeaanalyzer)

## Install (Python3)

```
python3 -m venv nmea
source ./nmea/bin/activate
pip install nmeaanalyzer
```
It will install pynmea2, six, cycler, pyparsing, python-dateutil, numpy, pytz, kiwisolver, matplotlib, nmeaanalyzer.

## Use  

- Parse NMEA file to sqlite database

	```
	nmeaparse test.nmea
	```
	It will create a database file named `test.nmea.db`.

- Plot SNR
	
	```
	nmeaplot test.nmea.db snr -c 0 -t 4
	```
	-c : Constellations.
	
		* 0: All
		* 1: GPS
		* 2: Glonass
		* 3: Qzss
		* 4: Beidou
		* 5: Galileo 
		* 6: NavIC
	-t : Display TopN satellites averaged SNR 
- Plot Speed

   ```
	nmeaplot test.nmea.db speed
	```
	
## Tips

- OSX issue

	```
	RuntimeError: Python is not installed as a framework. The Mac OS X backend will not be able to function correctly if Python is not installed as a framework. See the Python documentation for more information on installing Python as a framework on Mac OS X. Please either reinstall Python as a framework, or try one of the other backends. If you are using (Ana)Conda please install python.app and replace the use of 'python' with 'pythonw'. See 'Working with Matplotlib on OSX' in the Matplotlib FAQ for more information.
	```
	
	Fix:
	Add `backend: TkAgg` to the bottom of `lib/python3.6/site-packages/matplotlib/mpl-data/matplotlibrc`
	

- ModuleNotFoundError: No module named 'tkinter'
	
	Fix Ubuntu:
	
	```
	sudo apt install python3-tk
	```
	Fix CentOS:
	
	```
	sudo yum install tkinter
	``` 
