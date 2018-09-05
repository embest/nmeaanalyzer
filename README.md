# NMEA Analyzer  [![Build Status](https://travis-ci.org/embest/nmeaanalyzer.svg?branch=master)](https://travis-ci.org/embest/nmeaanalyzer)

## Install

```
virtualenv nmea
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
	
	