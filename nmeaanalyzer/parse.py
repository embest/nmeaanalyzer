#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2018 Embest
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import argparse
import sqlite3 as lite
import os
import time
from datetime import datetime, tzinfo, timezone
try:
    import nmeaparse
except ImportError:
    import pynmea2 as nmeaparse

def parse(src, database):
    try:
        con = lite.connect(database)
        cur = con.cursor()    
        cur.execute("DROP TABLE IF EXISTS GSV")
        cur.execute("CREATE TABLE IF NOT EXISTS GSV(Time INTEGER, Svid INTEGER, Cn0DbHz FLOAT, Constellation INTEGER, Azimuth FLOAT,  Elevation FLOAT, Type INTEGER);")

        cur.execute("DROP TABLE IF EXISTS GSA")
        cur.execute("CREATE TABLE IF NOT EXISTS GSA(Time INTEGER, FixType INTEGER, Svid INTEGER, Constellation INTEGER, Pdop FLOAT, Hdop FLOAT, Vdop FLOAT);")

        cur.execute("DROP TABLE IF EXISTS RMC")
        cur.execute("CREATE TABLE IF NOT EXISTS RMC(Time INTEGER, Validity Char, Latitude FLOAT, Longitude FLOAT, Speed FLOAT, Track FLOAT, Magnetic FLOAT);")
        
        utctime=datetime(1990,1,1,0,0,0, tzinfo=timezone.utc).time()
        utcdate=datetime(1990,1,1,0,0,0, tzinfo=timezone.utc).date()
        utcoffset=int((datetime.now()-datetime.utcnow()).total_seconds() + 0.1)

        timestamp = 0
        cur.execute("BEGIN TRANSACTION") 
        with open(src) as f:
            timesynced=False
            for line in f:
                if line.strip():
                    msg = nmeaparse.parse(line.strip())
                    if type(msg)==nmeaparse.types.talker.GGA:
                        utctime=msg.timestamp
                        timestamp=time.mktime(datetime.combine(utcdate, utctime).timetuple())+utcoffset
                        print(datetime.combine(utcdate, utctime), timestamp)
                    elif type(msg)==nmeaparse.types.talker.RMC:
                        if msg.datestamp:
                            utcdate=msg.datestamp
                            if not timesynced:
                                timestamp1=time.mktime(datetime.combine(utcdate, utctime).timetuple())+utcoffset
                                cur.execute('''UPDATE GSV SET Time=? WHERE Time=?''',(timestamp1,timestamp))
                            timesynced=True
                        cur.execute('''INSERT INTO RMC (Time, Validity, Latitude, Longitude, Speed, Track, Magnetic) VALUES (?,?,?,?,?,?,?)''',(timestamp, msg.status, msg.lat, msg.lon, msg.spd_over_grnd, msg.true_course, msg.mag_variation))
                    elif timesynced:
                        if type(msg)==nmeaparse.types.talker.GSV:
                            constellation=0
                            if msg.talker=="GP":
                                constellation=1
                            elif msg.talker=="GL":
                                constellation=2
                            elif msg.talker=="QZ":
                                constellation=3
                            elif msg.talker=="BD":
                                constellation=4
                            elif msg.talker=="GA":
                                constellation=5
                            elif msg.talker=="NC":
                                constellation=6

                            if len(msg.data) == 8:
                                l1_l2_l5=msg.sv_prn_num_2
                                cur.execute('''INSERT INTO GSV (Time, Azimuth, Cn0DbHz, Constellation, Elevation, Svid, Type) VALUES (?,?,?,?,?,?,?)''',(timestamp, msg.azimuth_1, msg.snr_1, constellation, msg.elevation_deg_1, msg.sv_prn_num_1, l1_l2_l5))
                            elif len(msg.data) == 12:
                                l1_l2_l5=msg.sv_prn_num_3
                                cur.execute('''INSERT INTO GSV (Time, Azimuth, Cn0DbHz, Constellation, Elevation, Svid, Type) VALUES (?,?,?,?,?,?,?)''',(timestamp, msg.azimuth_1, msg.snr_1, constellation, msg.elevation_deg_1, msg.sv_prn_num_1, l1_l2_l5))
                                cur.execute('''INSERT INTO GSV (Time, Azimuth, Cn0DbHz, Constellation, Elevation, Svid, Type) VALUES (?,?,?,?,?,?,?)''',(timestamp, msg.azimuth_2, msg.snr_2, constellation, msg.elevation_deg_2, msg.sv_prn_num_2, l1_l2_l5))
                            elif len(msg.data) == 16:
                                l1_l2_l5=msg.sv_prn_num_4
                                cur.execute('''INSERT INTO GSV (Time, Azimuth, Cn0DbHz, Constellation, Elevation, Svid, Type) VALUES (?,?,?,?,?,?,?)''',(timestamp, msg.azimuth_1, msg.snr_1, constellation, msg.elevation_deg_1, msg.sv_prn_num_1, l1_l2_l5))
                                cur.execute('''INSERT INTO GSV (Time, Azimuth, Cn0DbHz, Constellation, Elevation, Svid, Type) VALUES (?,?,?,?,?,?,?)''',(timestamp, msg.azimuth_2, msg.snr_2, constellation, msg.elevation_deg_2, msg.sv_prn_num_2, l1_l2_l5))
                                cur.execute('''INSERT INTO GSV (Time, Azimuth, Cn0DbHz, Constellation, Elevation, Svid, Type) VALUES (?,?,?,?,?,?,?)''',(timestamp, msg.azimuth_3, msg.snr_3, constellation, msg.elevation_deg_3, msg.sv_prn_num_3, l1_l2_l5))
                            elif len(msg.data) == 20:
                                l1_l2_l5=msg.data[19]
                                cur.execute('''INSERT INTO GSV (Time, Azimuth, Cn0DbHz, Constellation, Elevation, Svid, Type) VALUES (?,?,?,?,?,?,?)''',(timestamp, msg.azimuth_1, msg.snr_1, constellation, msg.elevation_deg_1, msg.sv_prn_num_1, l1_l2_l5))
                                cur.execute('''INSERT INTO GSV (Time, Azimuth, Cn0DbHz, Constellation, Elevation, Svid, Type) VALUES (?,?,?,?,?,?,?)''',(timestamp, msg.azimuth_2, msg.snr_2, constellation, msg.elevation_deg_2, msg.sv_prn_num_2, l1_l2_l5))
                                cur.execute('''INSERT INTO GSV (Time, Azimuth, Cn0DbHz, Constellation, Elevation, Svid, Type) VALUES (?,?,?,?,?,?,?)''',(timestamp, msg.azimuth_3, msg.snr_3, constellation, msg.elevation_deg_3, msg.sv_prn_num_3, l1_l2_l5))
                                cur.execute('''INSERT INTO GSV (Time, Azimuth, Cn0DbHz, Constellation, Elevation, Svid, Type) VALUES (?,?,?,?,?,?,?)''',(timestamp, msg.azimuth_4, msg.snr_4, constellation, msg.elevation_deg_4, msg.sv_prn_num_4, l1_l2_l5))
                            elif len(msg.data) == 7:
                                cur.execute('''INSERT INTO GSV (Time, Azimuth, Cn0DbHz, Constellation, Elevation, Svid, Type) VALUES (?,?,?,?,?,?,?)''',(timestamp, msg.azimuth_1, msg.snr_1, constellation, msg.elevation_deg_1, msg.sv_prn_num_1, 0))
                            elif len(msg.data) == 11:
                                cur.execute('''INSERT INTO GSV (Time, Azimuth, Cn0DbHz, Constellation, Elevation, Svid, Type) VALUES (?,?,?,?,?,?,?)''',(timestamp, msg.azimuth_1, msg.snr_1, constellation, msg.elevation_deg_1, msg.sv_prn_num_1, 0))
                                cur.execute('''INSERT INTO GSV (Time, Azimuth, Cn0DbHz, Constellation, Elevation, Svid, Type) VALUES (?,?,?,?,?,?,?)''',(timestamp, msg.azimuth_2, msg.snr_2, constellation, msg.elevation_deg_2, msg.sv_prn_num_2, 0))
                            elif len(msg.data) == 15:
                                cur.execute('''INSERT INTO GSV (Time, Azimuth, Cn0DbHz, Constellation, Elevation, Svid, Type) VALUES (?,?,?,?,?,?,?)''',(timestamp, msg.azimuth_1, msg.snr_1, constellation, msg.elevation_deg_1, msg.sv_prn_num_1, 0))
                                cur.execute('''INSERT INTO GSV (Time, Azimuth, Cn0DbHz, Constellation, Elevation, Svid, Type) VALUES (?,?,?,?,?,?,?)''',(timestamp, msg.azimuth_2, msg.snr_2, constellation, msg.elevation_deg_2, msg.sv_prn_num_2, 0))
                                cur.execute('''INSERT INTO GSV (Time, Azimuth, Cn0DbHz, Constellation, Elevation, Svid, Type) VALUES (?,?,?,?,?,?,?)''',(timestamp, msg.azimuth_3, msg.snr_3, constellation, msg.elevation_deg_3, msg.sv_prn_num_3, 0))
                            elif len(msg.data) == 19:
                                cur.execute('''INSERT INTO GSV (Time, Azimuth, Cn0DbHz, Constellation, Elevation, Svid, Type) VALUES (?,?,?,?,?,?,?)''',(timestamp, msg.azimuth_1, msg.snr_1, constellation, msg.elevation_deg_1, msg.sv_prn_num_1, 0))
                                cur.execute('''INSERT INTO GSV (Time, Azimuth, Cn0DbHz, Constellation, Elevation, Svid, Type) VALUES (?,?,?,?,?,?,?)''',(timestamp, msg.azimuth_2, msg.snr_2, constellation, msg.elevation_deg_2, msg.sv_prn_num_2, 0))
                                cur.execute('''INSERT INTO GSV (Time, Azimuth, Cn0DbHz, Constellation, Elevation, Svid, Type) VALUES (?,?,?,?,?,?,?)''',(timestamp, msg.azimuth_3, msg.snr_3, constellation, msg.elevation_deg_3, msg.sv_prn_num_3, 0))
                                cur.execute('''INSERT INTO GSV (Time, Azimuth, Cn0DbHz, Constellation, Elevation, Svid, Type) VALUES (?,?,?,?,?,?,?)''',(timestamp, msg.azimuth_4, msg.snr_4, constellation, msg.elevation_deg_4, msg.sv_prn_num_4, 0))
                        elif type(msg)==nmeaparse.types.talker.GSA:
                            constellation=0
                            if msg.talker=="GP":
                                constellation=1
                            elif msg.talker=="GL":
                                constellation=2
                            elif msg.talker=="QZ":
                                constellation=3
                            elif msg.talker=="BD":
                                constellation=4
                            elif msg.talker=="GA":
                                constellation=5
                            elif msg.talker=="NC":
                                constellation=6
                            if msg.sv_id01:
                                cur.execute('''INSERT INTO GSA (Time, FixType, Svid, Constellation, Pdop, Hdop, Vdop) VALUES (?,?,?,?,?,?,?)''',(timestamp, msg.mode_fix_type, msg.sv_id01, constellation, msg.pdop, msg.hdop, msg.vdop))
                            if msg.sv_id02:
                                cur.execute('''INSERT INTO GSA (Time, FixType, Svid, Constellation, Pdop, Hdop, Vdop) VALUES (?,?,?,?,?,?,?)''',(timestamp, msg.mode_fix_type, msg.sv_id02, constellation, msg.pdop, msg.hdop, msg.vdop))
                            if msg.sv_id03:
                                cur.execute('''INSERT INTO GSA (Time, FixType, Svid, Constellation, Pdop, Hdop, Vdop) VALUES (?,?,?,?,?,?,?)''',(timestamp, msg.mode_fix_type, msg.sv_id03, constellation, msg.pdop, msg.hdop, msg.vdop))
                            if msg.sv_id04:
                                cur.execute('''INSERT INTO GSA (Time, FixType, Svid, Constellation, Pdop, Hdop, Vdop) VALUES (?,?,?,?,?,?,?)''',(timestamp, msg.mode_fix_type, msg.sv_id04, constellation, msg.pdop, msg.hdop, msg.vdop))
                            if msg.sv_id05:
                                cur.execute('''INSERT INTO GSA (Time, FixType, Svid, Constellation, Pdop, Hdop, Vdop) VALUES (?,?,?,?,?,?,?)''',(timestamp, msg.mode_fix_type, msg.sv_id05, constellation, msg.pdop, msg.hdop, msg.vdop))
                            if msg.sv_id06:
                                cur.execute('''INSERT INTO GSA (Time, FixType, Svid, Constellation, Pdop, Hdop, Vdop) VALUES (?,?,?,?,?,?,?)''',(timestamp, msg.mode_fix_type, msg.sv_id06, constellation, msg.pdop, msg.hdop, msg.vdop))
                            if msg.sv_id07:
                                cur.execute('''INSERT INTO GSA (Time, FixType, Svid, Constellation, Pdop, Hdop, Vdop) VALUES (?,?,?,?,?,?,?)''',(timestamp, msg.mode_fix_type, msg.sv_id07, constellation, msg.pdop, msg.hdop, msg.vdop))
                            if msg.sv_id08:
                                cur.execute('''INSERT INTO GSA (Time, FixType, Svid, Constellation, Pdop, Hdop, Vdop) VALUES (?,?,?,?,?,?,?)''',(timestamp, msg.mode_fix_type, msg.sv_id08, constellation, msg.pdop, msg.hdop, msg.vdop))
                            if msg.sv_id09:
                                cur.execute('''INSERT INTO GSA (Time, FixType, Svid, Constellation, Pdop, Hdop, Vdop) VALUES (?,?,?,?,?,?,?)''',(timestamp, msg.mode_fix_type, msg.sv_id09, constellation, msg.pdop, msg.hdop, msg.vdop))
                            if msg.sv_id10:
                                cur.execute('''INSERT INTO GSA (Time, FixType, Svid, Constellation, Pdop, Hdop, Vdop) VALUES (?,?,?,?,?,?,?)''',(timestamp, msg.mode_fix_type, msg.sv_id10, constellation, msg.pdop, msg.hdop, msg.vdop))
                            if msg.sv_id11:
                                cur.execute('''INSERT INTO GSA (Time, FixType, Svid, Constellation, Pdop, Hdop, Vdop) VALUES (?,?,?,?,?,?,?)''',(timestamp, msg.mode_fix_type, msg.sv_id11, constellation, msg.pdop, msg.hdop, msg.vdop))
                            if msg.sv_id12:
                                cur.execute('''INSERT INTO GSA (Time, FixType, Svid, Constellation, Pdop, Hdop, Vdop) VALUES (?,?,?,?,?,?,?)''',(timestamp, msg.mode_fix_type, msg.sv_id12, constellation, msg.pdop, msg.hdop, msg.vdop))
                        else :
                            print("Unsupport message", msg)
        cur.execute("COMMIT") 
        con.commit()
                
    except:
        print("Unexpected error")
        if con:
            con.rollback()
        exit(1)
        
    finally:
        if con:
            con.close() 


def main():
    parser = argparse.ArgumentParser(description='NMEA Analyzer Parser Tool', 
                                     epilog='Example>> nmeaparse gps.nmea')
    parser.add_argument('input', type=str , help= "input file")
    args = parser.parse_args()
    print(args)
    src=args.input
    des=src+".db"
    print(src, des)
    if(os.path.isfile(des)):
        print("Database exists")
        os.remove(des)
    parse(src, des)    

if __name__ == '__main__':
    main()

