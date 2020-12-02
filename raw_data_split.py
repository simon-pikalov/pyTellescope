import csv
from PIL import Image, ImageDraw
from numpy import genfromtxt
import numpy as np

import os

dir="csvFilesForExp"
for filename in os.listdir(dir):
    print(filename)
    #thermReader = csv.reader(open('term_data_2018_01_09_13_29_09.csv', newline=''), delimiter=',', quotechar='|')
    thermReader = csv.reader(open(dir+'/'+filename, newline=''), delimiter=',', quotechar='|')
    for row in thermReader:
        if(len(row)!=0):
            time=row[0]
            width=row[1]
            length=row[2]
            #remove "["
            #print(row[3], row[len(row)-1])
            row[3]=row[3].replace("[","")
            row[len(row)-1] = row[len(row)-1].replace("]", "")
            #print (time, width,length,row[3],row[len(row)-1])
            #go over the raw_frame and create csv.
            index=0
            with open('RawCSV/ '+time+'_.csv', 'w', newline="") as csvfile:
                raw_frame = csv.writer(csvfile, delimiter=" " )
                pictureMap = []
                for x in range(int(length)):
                    nrow=""
                    tempRow=[]
                    #print(x)
                    for y in range(int(width)):
                        tmp=int(row[ x*(int(width)) +y+3].replace(" ",""))
                        tempRow.append(tmp/10)
                        ftemp=tmp/100
                        nrow=nrow+str(ftemp)+","
                        #print( (x)*(int(width)) +y+3)
                    #print(nrow+'\n')
                    pictureMap.append(tempRow)
                    raw_frame.writerow(nrow + '')
                #convert to numpy array.
                array = np.array(pictureMap, dtype=np.uint8)
                #clear list.
                pictureMap=[]
                new_image = Image.fromarray(array)
                new_image.save("rawData/"+time+'.png')
                    # im = Image.fromarray(pictureMap).convert('RGB')
                    # print(pictureMap)
                    # pix = im.load()
                    # print("pix", pix)
                    # smallest = np.amin(im)
                    # biggest = np.amax(im)



            index = index + 1