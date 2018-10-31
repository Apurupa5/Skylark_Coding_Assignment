

"""
main file where user can give his inputs
"""

import utils
import kml

def main():
    ""
    images_path="C:/Users/Python/Desktop/pythonwork/skylark_assignment/software_dev/images"
    videos_path = "C:/Users/Python/Desktop/pythonwork/skylark_assignment/software_dev/videos"
    poi_path="C:/Users/Python/Desktop/pythonwork/skylark_assignment/software_dev"
    
    ## Assignment part 1 : Finding the images within a given distance for each second in the srt file(video) 
    image_distance=35 ## Gives all images within x meters of the drone position
    utils.find_images_within_distance(videos_path,images_path,image_distance)  ## calculates the distances for each second in srt and saves the images in a csv which are within specified distance


    ## Assignment part 2:  Finding the images within the given distance for the given points of interest
    poi_image_distance=50
   
    utils.find_poi_images_within_distance(poi_path,images_path,poi_image_distance)
    
    ## Assignment part 3: Generating kml of the drone path
    
    kml.generate_kml(videos_path)

if __name__ == '__main__':
    main()
