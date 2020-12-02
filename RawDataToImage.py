from PIL import Image, ImageDraw
from numpy import genfromtxt
import numpy as np


for round in range(1,100,10):
    g = open('raw xiomo.csv', 'rb')
    print(g)
    temp = genfromtxt(g, dtype=np.dtype('f') , delimiter=',')
    im = Image.fromarray(temp).convert('RGB')
    print(temp)
    pix = im.load()
    print("pix",pix)
    smallest = np.amin(im)
    biggest = np.amax(im)
    print(smallest)
    print(biggest)
    #rows, cols = im.size
    cols, rows = im.size
    print("cols", cols, "rows" , rows)

    #np.dot(pix[...,:3], [0.299, 0.587, 0.114])
    for x in range(cols):
        for y in range(rows):
            #print( str(x) + " " + str(y))
            #pix[x,y] = (int(temp[y,x] // 256 // 256 % 256) ,int(temp[y,x] // 256  % 256),int(temp[y,x] % 256))
            print((temp[y, x]))
            pix[x, y] = (int((temp[y, x])*round ))
    im.save('exp2/'+g.name[0:-4] + '_'+str(round)+'.jpeg')
    smallest = np.amin(im)
    biggest = np.amax(im)
    print (smallest)
    print (biggest)