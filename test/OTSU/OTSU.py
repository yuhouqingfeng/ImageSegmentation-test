from PIL import Image
import cv2
import numpy as np
from matplotlib import pyplot as plt

filename = 'D:/littleDom/Python/picture/1.jpg'

image = cv2.imread(filename)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

plt.subplot(121), plt.imshow(image)
plt.title("source image"), plt.xticks([]), plt.yticks([])

# plt.subplot(132), plt.hist(image.ravel(), 256) #ravel的功能是将duo
# plt.title("Histogram"),plt.xticks([]), plt.yticks([])

ret1, th1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)  #方法选择为THRESH_OTSU
plt.subplot(122), plt.imshow(th1, "gray")
plt.title("threshold is " + str(ret1)), plt.xticks([]), plt.yticks([])
plt.show()