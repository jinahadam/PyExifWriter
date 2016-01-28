#!/usr/bin/env python
from fractions import Fraction
from PIL import Image
import piexif
import csv

def to_deg(value, loc):
        if value < 0:
            loc_value = loc[0]
        elif value > 0:
            loc_value = loc[1]
        else:
            loc_value = ""
        abs_value = abs(value)
        deg =  int(abs_value)
        t1 = (abs_value-deg)*60
        min = int(t1)
        sec = round((t1 - min)* 60, 5)
        return (deg, min, sec, loc_value)



def set_gps_location(file_name, lat, lng):
    lat_deg = to_deg(lat, ["S", "N"])
    lng_deg = to_deg(lng, ["W", "E"])

    print lat_deg
    print lng_deg

    exif_dict = piexif.load("images/"+file_name)
    im = Image.open("images/"+file_name)
    exif_dict["GPS"][piexif.GPSIFD.GPSLatitudeRef] = lat_deg[3]
    exif_dict["GPS"][piexif.GPSIFD.GPSLatitude] = (int(lat*1000000), 1000000)
    exif_dict["GPS"][piexif.GPSIFD.GPSLongitudeRef] = lng_deg[3]
    exif_dict["GPS"][piexif.GPSIFD.GPSLongitude] =  (int(lng*1000000), 1000000)

    print(exif_dict)
    exif_bytes = piexif.dump(exif_dict)
    im.save("results/"+file_name, "jpeg", exif=exif_bytes)


with open('exifgps.txt', 'rb') as csvfile:
   data = csv.reader(csvfile, delimiter=',', quotechar='|')
   for row in data:
       print(row[0],row[1],row[2])
       set_gps_location(row[0],float(row[1]),float(row[2]))
