import matplotlib
matplotlib.use('Agg')
from PIL import Image
import numpy as np
import cv2
import os
import matplotlib.pyplot as plt
from skimage import color
import time 

def isGrayScale(img):
    if(len(img.shape)<3):
        return True
    else :
        return False


#https://stackoverflow.com/questions/6646371/detect-which-image-is-sharper
def sharpness(img): 
    if not isGrayScale(img):
        img = color.rgb2gray(img)
    array = np.array(img, dtype=np.int32)
    gy, gx = np.gradient(array)
    gnorm = np.sqrt(gx**2 + gy**2)
    sharpness = np.average(gnorm)
    return sharpness  


def filecount(dir_name):
    try:
        return len([f for f in os.listdir(dir_name) if os.path.isfile(os.path.join(dir_name, f))])
    except Exception:
        return None


## contains the folder location of the images generated by the GAN 
folderloc = '/data/shared/suhit/pgfakes'
sharp_dict = {}
## contains the fullpath name of the plot png  
targetGraphNameWithExt = '/data/shared/suhit/pg_sharpness_plot.png' 


ti = time.time()
for root, dirs, filenames in os.walk(folderloc):
    for file in filenames:
        fullpath = os.path.join(folderloc,file)
        img = cv2.imread(fullpath,0)       
        name = file[:-4]
        sval = sharpness(img)
        sharp_dict[name] = sval 
tf = time.time()


tdiff = tf-ti
nfiles = filecount(folderloc)
print("Total processing time: ",tdiff)
print("Total number of images: ",nfiles)
print("Average time per image: ",tdiff/nfiles)


lists = sorted(sharp_dict.items()) # sorted by key, return a list of tuples
x,y = zip(*lists) 
plt.title("ImgName vs Sharpness")
plt.xlabel('ImageName')
plt.ylabel('Sharpness')
xn = range(len(x))
plt.xticks(xn,x)
#plt.xticks(rotation=45)
plt.plot(xn,y,'.')
plt.savefig(targetGraphNameWithExt,format = 'png')
print("Plot created successfully at ",targetGraphNameWithExt)
