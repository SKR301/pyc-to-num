import cv2
import numpy as np
import sys
from PIL import Image, ImageDraw

maskHeight, maskWidth = 12, 6


density="$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'."

length = len(density)

try:
    imgPath = sys.argv[1]       # input from 1st argument of cli
    outputType = sys.argv[2]    # type of output -t or -i
except:
    print('INVALID INPUT TYPE!!!\n')
    print('python main.py [relative-image-location] [output type]')
    print('\noutput type =>\t-t for text output')
    print('\t\t-i for image output')
    print('\n\nEg:\n   python main.py ./img -t')
    print('   python main.py ./img -i')
    exit()

# init
img = cv2.imread(imgPath, 0)
imgHeight, imgWidth = img.shape
img = cv2.bitwise_not(img)
digitDen = [33, 18, 28, 25, 28, 31, 31, 21, 33, 29]
img = np.divide(img, 255)

# calculate pixels in the masked box
def calcPixelSum(x,y):
    sum = 0
    for a in range(x, x + maskHeight):
        for b in range(y, y + maskWidth):
            sum += img[a][b]
    
    return sum

# find the digit that have similar no of pixel as in the masked area
def closestDig(num):
    return density[int(num*(length-1)/72)]
    temp = abs(num - digitDen[0])
    dig = 0
    for a in range(1, len(digitDen)):
        if abs(num - digitDen[a]) < temp:
            temp = abs(num - digitDen[a])
            dig = a
    
    return dig

# returns the size for output image
def getSize(txt):
    testImg = Image.new('RGB', (1, 1))
    testDraw = ImageDraw.Draw(testImg)
    return testDraw.textsize(txt)

# show/save output text to image
def asImg(text, savePath):
    colorText = "black"
    colorBackground = "white"
    width, height = getSize(text)
    img = Image.new('RGB', (width+4, height+4), colorBackground)
    d = ImageDraw.Draw(img)
    d.text((2, 2), text, fill=colorText)
    d.rectangle((0, 0, width+2, height))
    img.show()
    # img.save(savePath)    uncomment it to store it
    # make it user friendly not programmer friendly

if __name__ == "__main__":
    output = ''
    for a in range(0, imgHeight - maskHeight, maskHeight):
        row = []
        for b in range(0, imgWidth - maskWidth, maskWidth):
            if a > (imgHeight - maskHeight - 1) or b > (imgWidth - maskWidth - 1):
                break
            sum = calcPixelSum(a,b)
            dig = closestDig(sum)
            row.append(dig)
            output += str(dig)
        output += '\n'

    # generate output
    if outputType == '-t':
        print(output)           
    elif outputType == '-i':
        asImg(output, 'imgOutput.png')
    else:
        print('Invalid outputType. Please use -i for image or -t for text')

    