from PIL import Image
from PIL import ImageFilter
import os

inputDir = "./cleanedImg"
outputDir = "./ImgWithBackground"
bgDir = "./BackgroundDir"

newSize = (500, 500)


try:
  os.mkdir(outputDir)
except:
  pass

ImgDirs = os.listdir(inputDir)
BgImgs = os.listdir(bgDir)

for bg in BgImgs:
  background = Image.open(bgDir+ "/" +bg)
  background = background.resize(newSize)
  for dir in ImgDirs:
    files = os.listdir(inputDir + "/" + dir)
    for index, f in enumerate(files):
      imgDir = inputDir + "/" + dir + "/" + f
      foreground = Image.open(imgDir)
      
      foreground = foreground.resize(newSize)
      #combine foreground and background
      background = background.convert("RGBA")
      foreground = foreground.convert("RGBA")
      composite_img = Image.alpha_composite(background, foreground)

      #blend/blur composite image with a Gaussian filter
      composite_img = composite_img.filter(ImageFilter.GaussianBlur(radius=0.7))

      #save final composite image
      try:
        composite_img.save(outputDir + "/" + dir + "/" + str(index) + " over " + bg.split('.')[0] + ".png", 'PNG')
      except:
        os.mkdir(outputDir + "/" + dir)
        composite_img.save(outputDir + "/" + dir + "/" + str(index) + " over " + bg.split('.')[0] + ".png", 'PNG')