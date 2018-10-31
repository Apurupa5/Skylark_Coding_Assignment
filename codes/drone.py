# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 21:42:42 2018

@author: NB VENKATESHWARULU
"""
import os
from PIL import Image, ExifTags
from PIL.ExifTags import TAGS, GPSTAGS
import distances as dt
import pysrt
import csv
import pandas as pd

def read_images(images_path):
    images=[]
    image_names=[]
    for root, dirs, files in os.walk(images_path):    
        for file in files:
            if file.endswith(".JPG"):
               
                img = Image.open(images_path + "/" + file)
                images.append(img)
                image_names.append(file)
    return images,image_names

                    
def get_value(data, key):
        if key in data:
            return data[key]
        return None
    
def convert_to_degress(value):

        
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
      
def extract_gps_data(images,names):
    coordinate_data={}
    l=0
    actual_len=0
    for img in images:
        info=img._getexif()
        if info is not None:
            actual_len=actual_len+1
            for tag, value in info.items():
                    decoded = TAGS.get(tag, tag)
                    if decoded == "GPSInfo":
                        gps_data = {}
                        for t in value:
                            sub_decoded = GPSTAGS.get(t, t)
                            gps_data[sub_decoded] = value[t]
                            tup= get_lat_lng(gps_data)
                            coordinate_data[names[l]]=tup
        l=l+1
    #print  "Actual length" , actual_len
    return coordinate_data


def read_video_srt_files(videos_path):
    
    video_srts=[]
    video_srt_names=[]
    for root, dirs, files in os.walk(videos_path): 
        
        for file in files:
            if file.endswith(".SRT"):
                
                srt= pysrt.open(videos_path + "/" + file)
                video_srts.append(srt)
                video_srt_names.append(file)
    return video_srts,video_srt_names

def convert_timestamp2sec(timestamp):
    
    return (float(0.001*timestamp.milliseconds)+int(timestamp.seconds) + 60 * int(timestamp.minutes) + 3600 * int(timestamp.hours) + float(int(timestamp.hours) / 1000))


def find_images(srts,srt_names,image_data,image_distance):
    count=0
    
    for sub in srts:
        file_name=srt_names[count]
        new_file_name=file_name.split(".")[0]+"_imagelist.csv"
        csvfile=open(new_file_name, 'wb')
        fieldnames = ['Time(sec)', 'Images']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        #print "length", len(sub)
        
 
        for i in range(0,len(sub)):
            srt_coords=sub[i].text
            sec=sub[i].start.seconds
            sec_end=sub[i].end.minutes
            playtime = convert_timestamp2sec(sub[i].start)
            #print "sec",playtime
            
            srt_coords =str(srt_coords).split(",")
            srt_lng=float(srt_coords[0])
            srt_lat=float(srt_coords[1])
            srt_coords=(srt_lat,srt_lng)
            
            #dist=dt.vincent_distance()
            img_lst=[] 
            for key,value in image_data.iteritems():
                dist=dt.vincenty_distance(srt_coords,value)
                dist2=dt.haversine_distance(srt_coords,value)
                ## list of all the images within the given distance of the drone position at the present second
               
                if dist<=image_distance:
                    #print "dist between",srt_coords ,"and" , value, "with key",key,"is ", dist,"m ", dist2, "m"
                    img_lst.append(key.split(".")[0])
                    
           
            img_lst = ",".join(img_lst)
            print("sec", playtime , "Images", img_lst)
            
            writer.writerow({'Time(sec)':playtime,'Images':img_lst })
            
        count=count+1


def find_poi_images(poi_dfs,poi_csv_names,image_data,poi_image_distance):
    count=0
    
    for df in poi_dfs:
        file_name=poi_csv_names[count]
        new_file_name=file_name.split(".")[0]+"_poi_imagelist.csv"
        csvfile=open(new_file_name, 'wb')
        fieldnames = ['asset_name', 'Images']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
       
        points_of_interest=df['asset_name']
        latitudes=df['latitude']
        longitudes=df['longitude']
        
        print points_of_interest
        print latitudes
        print longitudes
 
        for i in range(0,len(points_of_interest)):
            print "### Asset name", points_of_interest[i]
            poi_lng=float(longitudes[i])
            poi_lat=float(latitudes[i])
            poi_coords=(poi_lat,poi_lng)
            
            print "%%%%%%%%",poi_lng,poi_lat,poi_coords
            
            #dist=dt.vincent_distance()
            img_lst=[] 
            for key,value in image_data.iteritems():
                dist=dt.vincenty_distance(poi_coords,value)
                #dist2=dt.haversine_distance(srt_coords,value)
                ## list of all the images within the given distance of the drone position at the present second
               
                if dist<=poi_image_distance:
                    print "dist between",poi_coords ,"and" , value, "with key",key,"is ", dist,"m "
                    img_lst.append(key.split(".")[0])
                    
           
            img_lst = ",".join(img_lst)
       
            writer.writerow({'asset_name':points_of_interest[i],'Images':img_lst })
            
        count=count+1
            
                
def read_poi(poi_path):
    poi_dfs=[]
    poi_csv_names=[]
    
    for root, dirs, files in os.walk(poi_path):    
        for file in files:
            if file.endswith(".csv"):
                df = pd.read_csv(poi_path + "/" + file)
                poi_dfs.append(df)
                poi_csv_names.append(file)
    return poi_dfs,poi_csv_names
    


###main


images_path = "C:/Users/NB VENKATESHWARULU/Desktop/ML/software_dev/images"
videos_path = "C:/Users/NB VENKATESHWARULU/Desktop/ML/software_dev/videos"
poi_path="C:/Users/NB VENKATESHWARULU/Desktop/ML/software_dev"

images,image_names=read_images(images_path) ## reading images from the images folder
extracted_data=extract_gps_data(images,image_names)    
#print(extracted_data)

## reading srt video files

srts,srt_names=read_video_srt_files(videos_path)


## Assignment part 1 : Finding the images within a given distance for each second in the srt file(video) 
image_distance=35 ## Gives all images within 35meters of the drone position
#find_images(srts,srt_names,extracted_data,image_distance)  ## calculates the distances for each second in srt and saves the images in a csv which are within specified distance

## Assignment part 2:  Finding the images within the given distance for the given points of interest
poi_image_distance=50
poi_dfs,poi_csv_names=read_poi(poi_path)
find_poi_images(poi_dfs,poi_csv_names,extracted_data,poi_image_distance)

