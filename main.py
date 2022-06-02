import cv2
import numpy as np

maskHeight, maskWidth = 8, 6

img = cv2.imread('img.png', 0)         # enter path to image here
imgHeight, imgWidth = img.shape
img = cv2.bitwise_not(img)

digitDen = [33, 18, 28, 25, 28, 31, 31, 21, 33, 29]

img = np.divide(img, 255)

def calcPixelSum(x,y):
    sum = 0
    for a in range(x, x + maskHeight):
        for b in range(y, y + maskWidth):
            sum += img[a][b]
    
    return sum

def closestDig(num):
    temp = abs(num - digitDen[0])
    dig = 0
    for a in range(1, len(digitDen)):
        if abs(num - digitDen[a]) < temp:
            temp = abs(num - digitDen[a])
            dig = a
    
    return dig

if __name__ == "__main__":

    numBox = []
    for a in range(0, imgHeight, maskHeight):
        row = []
        for b in range(0, imgWidth, maskWidth):
            if a > (imgHeight - maskHeight - 1) or b > (imgWidth - maskWidth - 1):
                break
            sum = calcPixelSum(a,b)
            dig = closestDig(sum)
            row.append(dig)

        numBox.append(row)


    for a in range(len(numBox)):
        for b in range(len(numBox[a])):
            print(numBox[a][b], end="")
        print()
