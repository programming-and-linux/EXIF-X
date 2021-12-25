#Disclaimer:- This script is for educational purpose only.
#Please do not use this tool against the images that you don't own or have any access to test

#Please note:- The current version v1 supports only .jpg images in single image option and in remove exif data option,
# the other image formats will be getting support in the next version soon.
#If you want to read the exif data from other image formats you can use the multiple image option

#Note that most of the social media applications/sites strip data from uploaded photos

#installing the required packages
#installing Pillow:- pip install Pillow
#installing prettytable:- pip install prettytable
import getpass
import os
import platform
import subprocess
import sys

from PIL import Image
from PIL.ExifTags import GPSTAGS,TAGS
from prettytable import PrettyTable,ALL

#the below function is used to generate the google maps link based on the longitude and lattitude data present in the GPS of the image
def create_google_maps_url(gps_coords):
    dec_deg_lat = convert_decimal_degrees(float(gps_coords["lat"][0]),  float(gps_coords["lat"][1]), float(gps_coords["lat"][2]), gps_coords["lat_ref"])
    dec_deg_lon = convert_decimal_degrees(float(gps_coords["lon"][0]),  float(gps_coords["lon"][1]), float(gps_coords["lon"][2]), gps_coords["lon_ref"])
    return f"https://maps.google.com/?q={dec_deg_lat},{dec_deg_lon}"


#the below function helps conversion to decimal degrees for latitude and longitude is from degree/minutes/seconds format
def convert_decimal_degrees(degree, minutes, seconds, direction):
    decimal_degrees = degree + minutes / 60 + seconds / 3600
    if direction == "S" or direction == "W":
        decimal_degrees *= -1
    return decimal_degrees

#the below function is used to for the tabulation of the info and return it
def get_info(image):
    #creating an expty table with no header
    table = PrettyTable(header=False)
    #setting up the max. width of the table
    table.max_table_width = 250
    #used to set the horizontal rules for the table
    table.hrules = ALL
    #check if exif data is present
    if image._getexif() == None:
        table.add_row(["No exif data found"])
    else:
        try:
            #inserting the values inside the table
            table.add_row(["Image Location", image.filename])
            table.add_row(["Dimension", str(image.size[0]) + "x" + str(image.size[1])])
            for tag, value in image._getexif().items():
                if TAGS.get(tag) == "Make":
                    table.add_row(["Device", value])
                elif TAGS.get(tag) == "Model":
                    table.add_row(["Model", value])
                elif TAGS.get(tag) == "Software":
                    table.add_row(["Software", value])
                elif TAGS.get(tag) == "DateTime":
                    table.add_row(["DateTime", value])
                elif TAGS.get(tag) == "FocalLength":
                    table.add_row(["Focal Length", value])
                elif TAGS.get(tag) == "FocalLengthIn35mmFilm":
                    table.add_row(["Focal length in 35mm film", value])
                elif TAGS.get(tag) == "ApertureValue":
                    table.add_row(["Apperture", value])
                elif TAGS.get(tag) == "FNumber":
                    table.add_row(["F number", value])
                elif TAGS.get(tag) == "ISOSpeedRatings":
                    table.add_row(["ISO", value])
                elif TAGS.get(tag) == "GPSInfo":
                    gps_coords = {}
                    for key, val in value.items():
                        if GPSTAGS.get(key) == "GPSLatitude":
                            gps_coords["lat"] = val
                            table.add_row(["Latitude", val])
                        elif GPSTAGS.get(key) == "GPSLongitude":
                            gps_coords["lon"] = val
                            table.add_row(["Longitude", val])
                        elif GPSTAGS.get(key) == "GPSLatitudeRef":
                            gps_coords["lat_ref"] = val
                        elif GPSTAGS.get(key) == "GPSLongitudeRef":
                            gps_coords["lon_ref"] = val

                    if gps_coords:
                        table.add_row(["Google Maps Link", create_google_maps_url(gps_coords)])

        except AttributeError:
            print("Attribute Error")

    return table
while True:
    # if you are running this code on windows change "clear" to "cls"
    subprocess.call("clear",shell=True)
    logo = """
     _______          _________ _______            
    (  ____ \|\     /|\__   __/(  ____ \  |\     /|
    | (    \/( \   / )   ) (   | (    \/  ( \   / )
    | (__     \ (_) /    | |   | (__  _____\ (_) / 
    |  __)     ) _ (     | |   |  __)(_____)) _ (  
    | (       / ( ) \    | |   | (         / ( ) \ 
    | (____/\( /   \ )___) (___| )        ( /   \ )
    (_______/|/     \|\_______/|/         |/     \|
                                                   
     +-+-+-+-+-+-+-+-+-+ +-+-+ +-+ +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     |D|e|v|e|l|o|p|e|d| |b|y| |:| |p|r|o|g|r|a|m|m|i|n|g|.|a|n|d|.|l|i|n|u|x|
     +-+-+-+-+-+-+-+-+-+ +-+-+-+-+ +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     |V|e|r|s|i|o|n| |:| |1|.|0|                                              
     +-+-+-+-+-+-+-+ +-+ +-+-+-+                                              
     --------------------------------------                                    
     | Instagram : @programming.and.linux |                                   
     --------------------------------------                                   
                                                                              """

    #print the logo
    print(logo)

    option = None
    try:
        option = int(input("\n    0. Exit\n    1. Single image\n    2. Multiple images\n    3. Remove exif data\n    Enter your choice: "))
    except:
        print("\n\n    Incorrect choice")
        close = input("\n\n    Press any key to continue...........")

    #checks for the option chose by the user
    if option == 0:
        #exit the code
        exit()
    elif option == 1:
        #this option is used to get exif data from the image
        #if you are running this code on windows change "clear" to "cls"
        subprocess.call("clear",shell=True)
        print(logo)
        try:
            #input image path
            path = input("\n    Enter the image path: ")
            #opens the image using pillow
            image = Image.open(path)
            #functional call to get the image info
            table = get_info(image)
            #displays the output
            print("\n\n    Image information: \n")
            print(table)
            #close the image
            image.close()
            #this input is used, to pause the loop that takes place unless the user wishes to
            close = input("\n\n    Press any key to continue...........")
        except IOError:
            #error message to be printed if the input file is unsupported or the file can't be opened
            print("\n\n    Incorrect file or path specified")
            #this input is used, to pause the loop that takes place unless the user wishes to
            close = input("\n\n    Press any key to continue...........")
    elif option == 2:
        # if you are running this code on windows change "clear" to "cls"
        subprocess.call("clear", shell=True)
        print(logo)
        try:
            #input the path of the directory consisting of numerous images
            path = input("\n    Enter the path of the directory: ")
            #store's the current working directory path
            cwd = os.getcwd()
            #change the working directory to the path specified by the user
            os.chdir(path)
            #list of files present in the folder
            files = os.listdir(path)
            #check if the directory is empty
            if len(files) == 0:
                print("\n\n    There aren't any files in the specified folder")
                close = input("\n\n    Press any key to continue...........")
            else:
                #store's the value of the output screen
                original = sys.stdout
                #prints the filename from which the exif data is going to be extracted
                for file in files:
                    print(f"\n\n    Extracting from {file}")
                    #redirects the output screen to a .txt file created in the images folder
                    if platform.system() == "Linux":
                        #if its a linux system it saves the data in the directory where the images are stored
                        sys.stdout = open("output.txt","a")
                    else:
                        #if its a windows system it save the output in downloads
                        sys.stdout = open("C:\\Users\\"+getpass.getuser()+"\\Downloads\\output.txt", "a")
                    try:
                        #open the image using Pillow
                        image = Image.open(file)
                        #function call to get the image info
                        table = get_info(image)
                        #print the image information
                        print(f"\n\n---------------------------------------------------{image.filename}---------------------------------------------------")
                        print("\n\nImage information: \n\n")
                        print(table)
                        #close the image
                        image.close()

                    except IOError:
                        pass

                    #redirects back the output to the screen from the .txt file
                    sys.stdout = original

            #extracting finished
            if(platform.system()=="Linux"):
                print("\n\n     Please check for output.txt file in "+path)
            else:
                print("\n\n     Check for 'output.txt' in Downloads to see the result")
            #change the current working directory back to the old one
            os.chdir(cwd)
            #this input is used, to pause the loop that takes place unless the user wishes to
            close = input("\n\n    Press any key to continue...........")

        except:
            #prints if inscorrect path is provided as input
            print("\n\n    Incorrect path specified")
            #this input is used, to pause the loop that takes place unless the user wishes to
            close = input("\n\n    Press any key to continue...........")

    elif option == 3:
        #this option is used to remove exif data from a image
        # if you are running this code on windows change "clear" to "cls"
        subprocess.call("clear",shell=True)
        print(logo)
        try:
            #enter the image path
            path = input("\n     Enter the image path: ")
            #print the file name from which the image is being removed
            print(f"\n\n    Removing exif from {path}.....")
            #open's the image
            image = Image.open(path)
            #get the image data
            image_data = list(image.getdata())
            #geneartes the new image with blank exif data
            image_no_exif = Image.new(image.mode,image.size)
            #insert image data to the generated image
            image_no_exif.putdata(image_data)
            #saves the generated image
            image_no_exif.save(path)
            #prints data is removed
            print(f"\n\n    Removed exif data from {path}")
            #this input is used, to pause the loop that takes place unless the user wishes to
            close = input("\n\n    Press any key to continue...........")

        except:
            #prints if incorrect file is specified as input
            print("\n\n    Incorrect file or path specified")
            #this input is used, to pause the loop that takes place unless the user wishes to
            close = input("\n\n    Press any key to continue...........")
    else:

        print("\n\n    Incorrect choice")
        #this input is used, to pause the loop that takes place unless the user wishes to
        close = input("\n\n    Press any key to continue...........")
