from tkinter import *
from PIL import ImageTk
from PIL import Image
import google_streetview.api
import random
import csv
from time import sleep
key = open("apiKey.txt").read()


def getRandomLocation():
    #top right  50.120468, -122.95421
    #bottom right 50.113189, -122.952032
    #bottom left 50.112061, -122.956806
    #top left 50.120924, -122.958889
    lowLat = 50112061
    highLat = 50120924
    lowLon = 122952032
    highLon = 122958889
    lat = (random.randrange(lowLat,highLat))/1000000
    lon = (random.randrange(lowLon,highLon))/1000000*-1
    loc = str(lat) + "," + str(lon)
    return loc

def setParams():
    loc = getRandomLocation()
    heading = random.choice([0,90,180,270])
    params = [{
    'size': '640x640',
    'location': loc,
    'heading': heading,
    'fov': '180',
    'key': key
    }]
    return params

def getStreetView(params):
    # Create a results object
    results = google_streetview.api.results(params)
    # Download images to directory 'downloads'
    results.download_links('downloads')

def writeData(data):
    f = open('checked.csv','a')
    f.write(data)
    f.close()
    print(data)

def nextImg():
    global params
    params = setParams()
    getStreetView(params)
    sleep(.3)
    img = ImageTk.PhotoImage(Image.open("downloads/gsv_0.jpg"))
    panel.configure(image=img)
    panel.image = img

def changeLast(event):
    global data
    if "TRUE" in data:
        data = data[:-5]
        data += "FALSE\n"
    else:
        data = data[:-6]
        data += "TRUE\n"
    file = open("checked.csv")
    lines = file.readlines()
    file.close()
    w = open("checked.csv",'w')
    w.writelines([item for item in lines[:-1]])
    w.write(data)
    w.close()
    print("Changed:")
    print(data)


def left(event):
    print('left')
    #not a match
    global params
    global data 
    data = str(params[0]['location']) + "," + str(params[0]['heading']) + ",FALSE\n"
    writeData(data)
    nextImg()

def right(event):
    print('right')
    #match
    global params
    global data 
    data = str(params[0]['location']) + "," + str(params[0]['heading']) + ",TRUE\n"
    writeData(data)
    nextImg()

def skip(event):
    print("skip")
    nextImg()

#init the params
params = setParams()

main = Tk()
main.title("Beaver Findr")
main.geometry("640x640")
main.bind('<Left>',left)
main.bind('<Right>',right)
main.bind('<Down>',skip)
main.bind('<Up>',changeLast)


getStreetView(params)
img = ImageTk.PhotoImage(Image.open("downloads/gsv_0.jpg"))

panel = Label(main, image=img)
panel.pack()
main.mainloop()