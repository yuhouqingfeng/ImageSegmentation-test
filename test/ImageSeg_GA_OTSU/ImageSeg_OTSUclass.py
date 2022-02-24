import numpy as np

def otsu(image, threshold):
    image = np.asarray(image)
    Sum  = image.shape[0] * image.shape[1]   #像素总数
    bin_image = image < threshold #得到True和False数组
    sumT = np.sum(image)
    N1 = np.sum(bin_image)
    sum1 = np.sum(bin_image * image)
    N2 = Sum - N1
    if N2 == 0 or N1 == 0:
        return 0
    sum2 = sumT - sum1
    U1 = sum1 / (N1 * 1.0)
    U2 = sum2 / (N2 * 1.0)
    g = N1 / (Sum * 1.0) * N2 / (Sum * 1.0) * (U1 - U2) * (U1 - U2)
    return g
