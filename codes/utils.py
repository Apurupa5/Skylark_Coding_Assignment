# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 22:33:08 2018

@author: Python
"""

import io_oper
from PIL import Image, ExifTags
from PIL.ExifTags import TAGS, GPSTAGS
import distances as dt
import csv
import gps

def find_images_within_distance(videos_path,images_path,image_distance):
    """ calculates the distances for each second in srt and saves the images in a csv 
    which are within specified distance
    
    videos_path--- path where srt of video files are stored
    images_path--- path where images are stored
    image_distance -- distance within which we require images
    """
    
    images,image_names=io_oper.read_images(images_path) ## reading images from the images folder
     
    extracted_image_coords=extract_gps_data_from_images(images,image_names)  ### image coordinates extracted from the exif data
   
    
    srts,srt_names=io_oper.read_video_srt_files(videos_path)  ### reading video srt files in the given path
    count=0
    
    for sub in srts:
        file_name=srt_names[count]
        new_file_name=file_name.split(".")[0]+"_imagelist.csv"
        csvfile=open(new_file_name, 'w',newline='')
        fieldnames = ['Time(sec)', 'Images']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(0,len(sub)):
            srt_coords=sub[i].text
            sec=sub[i].start.seconds
            sec_end=sub[i].end.minutes
            playtime = gps.convert_timestamp2sec(sub[i].start)
            #print "sec",playtime
            
            srt_coords =str(srt_coords).split(",")
            srt_lng=float(srt_coords[0])
            srt_lat=float(srt_coords[1])
            srt_coords=(srt_lat,srt_lng)
            
            #dist=dt.vincent_distance()
            img_lst=[] 
            for key,value in extracted_image_coords.items():
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


  

def find_poi_images_within_distance(poi_path,images_path,poi_image_distance):
    
    """ 
    calculates the images for the specified points of interest and saves it in a CSV format
    input to this function are
    poi_path---path for the csv file containting points of interest and their gps coordinates
    image_path -- path where images are stored
    poi_distance -- distance within which we need the images(meteres)
    
    """
    
    poi_dfs,poi_csv_names=io_oper.read_poi(poi_path)
    images,image_names=io_oper.read_images(images_path) ## reading images from the images folder
     
    image_data=extract_gps_data_from_images(images,image_names)  ### image coordinates extracted from the exif data
   
    count=0
    
    for df in poi_dfs:
        file_name=poi_csv_names[count]
        new_file_name=file_name.split(".")[0]+"_poi_imagelist.csv"
        csvfile=open(new_file_name, 'w',newline='')
        fieldnames = ['asset_name', 'Images']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
       
        points_of_interest=df['asset_name']
        latitudes=df['latitude']
        longitudes=df['longitude']
              
        for i in range(0,len(points_of_interest)):

            poi_lng=float(longitudes[i])
            poi_lat=float(latitudes[i])
            poi_coords=(poi_lat,poi_lng)
            
          
            #dist=dt.vincent_distance()
            img_lst=[] 
            for key,value in image_data.items():
                dist=dt.vincenty_distance(poi_coords,value)
                #dist2=dt.haversine_distance(srt_coords,value)
                ## list of all the images within the given distance of the drone position at the present second
               
                if dist<=poi_image_distance:
                    print("dist between",poi_coords ,"and" , value, "with key",key,"is ", dist,"m ")
                    img_lst.append(key.split(".")[0])
                    
           
            img_lst = ",".join(img_lst)
       
            writer.writerow({'asset_name':points_of_interest[i],'Images':img_lst }) ## Saving in CSV file
            
        count=count+1
        
        
def extract_gps_data_from_srt(srts,srt_names):
    
    """
    This method extracts gps data from each srt file and returns coordinates in (lng,lat) format
    return type is dictionary of srt_filenames and coordinates, srt_filenames and playtime(sec)
    """
    coordinate_data={}
    play_times={}
    srt_coords_lst=[]
    playtimes_lst=[]
    count=0
    for sub in srts:
        file_name=srt_names[count]
        for i in range(0,len(sub)):
            srt_coords=sub[i].text
            sec=sub[i].start.seconds
            sec_end=sub[i].end.minutes
            playtime = gps.convert_timestamp2sec(sub[i].start)
            #print "sec",playtime
            
            srt_coords =str(srt_coords).split(",")
            srt_lng=float(srt_coords[0])
            srt_lat=float(srt_coords[1])
            srt_coords=(srt_lng,srt_lat)  ## (coordinates in lat,lng format)
            srt_coords_lst.append(srt_coords)
            playtimes_lst.append(playtime)
        coordinate_data[file_name]=srt_coords_lst
        play_times[file_name]=playtimes_lst
        count=count+1
    return coordinate_data,play_times
    
    
    
def extract_gps_data_from_images(images,names):
    
    """ extracts the exif coordinate data from images """
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
                            tup= gps.get_lat_lng(gps_data)
                            coordinate_data[names[l]]=tup
        l=l+1
    
    return coordinate_data


