# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 16:39:32 2018

@author: NB VENKATESHWARULU
"""

import geopy.distance
from math import sin, cos, sqrt, atan2, radians

def  vincenty_distance(coords_1,coords_2):
    dist_km=geopy.distance.vincenty(coords_1, coords_2).meters
    return dist_km

def haversine_distance(coords_1,coords_2):
    # approximate radius of earth in km
    R = 6373.0
   
    lat1 = radians(coords_1[0])
    lon1 = radians(coords_1[1])
    lat2 = radians(coords_2[0])
    lon2 = radians(coords_2[1])
    
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    distance = R * c
    return distance*1000
  