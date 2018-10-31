# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 22:08:15 2018

@author: Python
"""

import simplekml
import io_oper
import utils


def generate_kml(videos_path):
    #videos_path = "C:/Users/Python/Desktop/pythonwork/skylark_assignment/software_dev/videos"
    
    srts,srt_names=io_oper.read_video_srt_files(videos_path)
    coords,times=utils.extract_gps_data_from_srt(srts,srt_names)
    print(coords)
    i=0
    for key,value in coords.items():
        kml=simplekml.Kml()
        srt_name=srt_names[i].split(".")[0]
        kml.newlinestring(name="dronepath", description="Path followed by the drone in the Video for file"+srt_name,coords=value)
        ########### Writing to the KML file
     
        kml_file_name=srt_name+".kml"
        with open(kml_file_name, mode='w') as k:
                k.write(kml.kml())
        i=i+1     