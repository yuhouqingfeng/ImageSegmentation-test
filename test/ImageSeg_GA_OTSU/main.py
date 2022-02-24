from PIL import Image
import numpy as np
import cv2
from matplotlib import pyplot as plt
from ImageSeg_GA_OTSU.ImageSeg_GAclass import GA

filename = 'D:/littleDom/Python/picture/9.jpg'
N = 100 #迭代次数

def Threshold(t, image):
    image_tmp = np.asarray(image)
    intensity_array = list(np.where(image_tmp<t, 0, 255).reshape(-1))
    image.putdata(intensity_array)
    img = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)#将RGB转换成BGR
    plt.title("threshold is " + str(t))
    plt.imshow(img), plt.axis("off")
    plt.show()

def main():
    im = Image.open(filename)   # 读取的是RGB
    im.load()   #会自动resize到小尺寸，为了加快图片处理时间，且读取的数据类型为【0,1】范围内的double
    plt.imshow(im), plt.axis("off")
    plt.show()

    im_gray = im.convert('L') # 模式“L”为灰色图像，它的每个像素用8个bit表示，0表示黑，255表示白
    popular = np.array(im_gray).flatten()  # 像素一维数组  # 用np.array()将此数组变为numpy下的数组 ，flatten()将其变为一维数组，是numpy中的函数
    # 画直方图
    n, bins, patches = plt.hist(popular, bins=300, facecolor='blue', alpha=1)  # hist函数可以直接绘制直方图# arr: 需要计算直方图的一维数组# bins: 直方图的柱数，可选项，默认为10# facecolor: 直方图颜色 # alpha: 透明度
    plt.show()

    ga = GA(im_gray)
    for x in range(N):
        ga.Evolution()
    threshold = ga.Result()
    print(threshold)

    Threshold(threshold, im_gray)

if __name__ == "__main__":
    main()