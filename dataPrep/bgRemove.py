
import numpy as np
from PIL import Image
from statistics import mode
import operator as op
import os

# Dir where images are stored
imageDir = "./img"

# Dir where processed images should be saved
outputDir = "./cleanedImg"

# How close to the background color does a pixel have to be to be removed
colorThreshold = 65

# How much of the image has to be the same color to be considered the background
backgroundColorPercentage = 0.15

bgRemoveCounter = 0
totalCounter = 0

def equalsThreshold(c1, c2, threshold):
    return (
        c2[0] >= c1[0] - threshold and c2[0] <= c1[0] + threshold and
        c2[1] >= c1[1] - threshold and c2[1] <= c1[1] + threshold and
        c2[2] >= c1[2] - threshold and c2[2] <= c1[2] + threshold
    )

def removeBackground(img):
    global bgRemoveCounter
    global totalCounter
    imgData = img.getdata()
    m = mode(imgData)
    count = op.countOf(imgData, m)
    totalPixels = len(imgData)
    colorPercentage = count / totalPixels

    if(colorPercentage >= backgroundColorPercentage):
        bgRemoveCounter += 1
        newData = []
        for pix in imgData:
            if(equalsThreshold(m, pix, 60)):
                newData.append((0, 0, 0, 0))
            else:
                newData.append((pix[0], pix[1], pix[2], pix[3]))
            
        
        img.putdata(newData)

    totalCounter += 1    
    return img

def cleanImagesInDir(dir):
    files = os.listdir(dir)
    subdir = dir.removeprefix(f'{imageDir}')

    if subdir.startswith(os.sep):
        subdir = subdir[1:]

    newdir = os.path.join(outputDir, subdir)

    oppositeSep = '\\' if os.sep != '\\' else '/'
    newdir = newdir.replace(oppositeSep, os.sep)

    try:
        os.mkdir(newdir)
    except:
        pass

    for file in files:
        listedFile = os.path.join(dir, file)
        if os.path.isdir(listedFile):
            cleanImagesInDir(listedFile)
            continue

        try:
            img = Image.open(listedFile)
            img = img.convert("RGBA")
            img = removeBackground(img)
            fileName = file.split('/')[-1]
            fileName = fileName.split('.')[0] + '.png'
            savedir = os.path.join(newdir, fileName)
            img.save(savedir, 'PNG')
            print(f'saving: {savedir}')
        except Exception as e:
            print(f'Exception converting {listedFile} ==> {e}')


cleanImagesInDir(imageDir)
print(f"Done! Removed bakgrounds from {bgRemoveCounter} out of {totalCounter} images")


