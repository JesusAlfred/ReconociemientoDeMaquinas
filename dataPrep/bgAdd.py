from PIL import Image
from PIL import ImageFilter
import os

inputDir = "./cleanedImg"
outputDir = "./ImgWithBackground"
bgDir = "./BackgroundDir"

newSize = (500, 500)

def transparent_bg_square(img):
    #return a white-background-color image having the img in exact center
    size = tuple(int(1.5 * elem) for elem in img.size)
    layer = Image.new('RGBA', size, (0,0,0,0))
    layer.paste(img, tuple(map(lambda x:int((x[0]-x[1])/2), zip(size, img.size))))
    return layer

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
      
      foreground = transparent_bg_square(foreground)
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