# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 22:37:17 2018

@author: Python
"""


"""
This script contains functions for reading files and saving them

"""

import os
import pysrt
import pandas as pd
from PIL import Image, ExifTags
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

    

