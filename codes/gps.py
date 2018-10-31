# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 23:16:30 2018

@author: Python
"""

""" Contains methods to deal with exif and gps data"""
from PIL import Image, ExifTags
def get_value(data, key):
      """ returns dat if key is present else returns none """
      if key in data:
          return data[key]
      return None
    
def convert_to_degress(value):

        """ converts the given latitude and longitude values to degrees"""
        d0 = value[0][0]
        d1 = value[0][1]
        d = float(d0) / float(d1)

        m0 = value[1][0]
        m1 = value[1][1]
        m = float(m0) / float(m1)

        s0 = value[2][0]
        s1 = value[2][1]
        s = float(s0) / float(s1)

        return d + (m / 60.0) + (s / 3600.0)
    
def get_lat_lng(gps_data):
          gps_latitude = get_value(gps_data, "GPSLatitude")
          gps_latitude_ref = get_value(gps_data, 'GPSLatitudeRef')
          gps_longitude = get_value(gps_data, 'GPSLongitude')
          gps_longitude_ref = get_value(gps_data, 'GPSLongitudeRef')
          if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
              lat = convert_to_degress(gps_latitude)
              if gps_latitude_ref != "N":                     
                  lat = 0 - lat
              lng = convert_to_degress(gps_longitude)
              if gps_longitude_ref != "E":
                  lng = 0 - lng
              return(lat,lng)
      



def convert_timestamp2sec(timestamp):
    """ converts given timestamp to sec"""
    
    return (float(0.001*timestamp.milliseconds)+int(timestamp.seconds) + 60 * int(timestamp.minutes) + 3600 * int(timestamp.hours) + float(int(timestamp.hours) / 1000))
