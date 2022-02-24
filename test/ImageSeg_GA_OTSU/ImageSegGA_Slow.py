import numpy as np
import random
import  cv2
from PIL import Image
from matplotlib import pyplot as plt


filename = 'D:/littleDom/Python/picture/4.jpg'

#图像分割
def threshold(gray,num):#  gray灰度图 num阈值
    image_tmp = np.asarray(gray)
    intensity_array = list(np.where(image_tmp < num, 0, 255).reshape(-1))
    gray.putdata(intensity_array)
    img = cv2.cvtColor(np.asarray(gray), cv2.COLOR_RGB2BGR)
    plt.imshow(img), plt.axis("off"),plt.show()


def ori_popular(num):
    ori_popular = []
    for i in range(num):
        x = random.randint(0,255)  # 在此范围内生成一个随机浮点数
        ori_popular.append(x)
    return ori_popular

def encode(ori_popular):  # 为图像像素进行基因编码
    popular_gene = []
    for i in range(len(ori_popular)):
        data = bin(ori_popular[i])
        popular_gene.append(data)
    return popular_gene

def decode(popular_gene):  #新种群解码
    new_popular = []
    for i in range(len(popular_gene)):
        data = int(popular_gene[i],2)
        new_popular.append(data)
    return new_popular


def total_pix(image):
    size = image.shape[0] * image.shape[1]
    return size

def fast_otsu(image, threshold):
    image = np.transpose(np.asarray(image))  #矩阵转置
    total  = total_pix(image)   #像素总数
    bin_image = image < threshold #得到True和False数组
    sumT = np.sum(image)
    N1 = np.sum(bin_image)
    sum1 = np.sum(bin_image * image)
    N2 = total - N1
    if N2 == 0  or N1 == 0:
        return 0
    sum2 = sumT - sum1
    U1 = sum1 / (N1 * 1.0)
    U2 = sum2 / (N2 * 1.0)
    g = N1 / (total * 1.0) * N2 / (total * 1.0) * (U1 - U2) * (U1 - U2)
    return g

def enfitness(image,new_popular):  #适应性函数 sum总像素值
    fitness = []
    for i in range(len(new_popular)):
        fitness.append(fast_otsu(image,new_popular[i]))
    return fitness

# 选择and交叉。选择用轮牌赌，交叉概率为0.66
def  Selection_Crossing(image,popular_gene):
    new_popular = decode(popular_gene)
    fitness = enfitness(image,new_popular)
    sum = 0 #函数总值
    for i in range(len(fitness)):
        sum += fitness[i]
    # 各个个体被选择的概率
    probability = []
    for i in range(len(fitness)):
        probability.append(fitness[i] / sum)
    # 概率分布
    probability_sum = []
    for i in range(len(fitness)):
        if i == 0:
            probability_sum.append(probability[i])
        else:
            probability_sum.append(probability_sum[i - 1] + probability[i])

    # 选择
    new_popular_gene = []
    for i in range(int(len(fitness) / 2)):
        temp = []
        for j in range(2):
            rand = random.uniform(0, 1)  # 在0-1之间随机一个浮点数
            for k in range(len(fitness)):
                if k == 0:
                    if rand < probability_sum[k]:
                        temp.append(popular_gene[k])
                else:
                    if (rand > probability_sum[k - 1]) and (rand < probability_sum[k]):
                        temp.append(popular_gene[k])

        # 交叉，交叉率为0.66。
        is_change = random.randint(0, 2)
        if is_change:
            temp_s = temp[0][3:5]
            temp[0] = temp[0][0:3] + temp[1][3:5] + temp[0][5:]
            temp[1] = temp[1][0:3] + temp_s + temp[1][5:]

        new_popular_gene.append(temp[0])
        new_popular_gene.append(temp[1])
    return new_popular_gene


# 变异.概率为0.05
def Variation(new_popular_gene):
    for i in range(len(new_popular_gene)):
        is_variation = random.uniform(0, 1)
        # print([len(k) for k in popular_new])
        if is_variation < 0.05:
            rand = random.randint(2, 9)
            if new_popular_gene[i][rand] == '0':
                new_popular_gene[i] = new_popular_gene[i][0:rand] + '1' + new_popular_gene[i][rand + 1:]
            else:
                new_popular_gene[i] = new_popular_gene[i][0:rand] + '0' + new_popular_gene[i][rand + 1:]
    return new_popular_gene



if __name__ == '__main__':
 # 显示原图
 image = Image.open(filename) # 打开图像并转化为数字矩阵,原图RGB
 plt.imshow(image),plt.axis("off"), plt.show()

 # 显示灰度图
 img = cv2.cvtColor(np.asarray(image),cv2.COLOR_RGB2BGR)
 plt.imshow(img), plt.axis("off"), plt.show()

 ####### 灰度图分割
 gray = image.convert('L')
 rows, cols = np.shape(gray)

 popular = np.array(gray).flatten() # 像素一维数组  # 用np.array()将此数组变为numpy下的数组 ，flatten()将其变为一维数组，是numpy中的函数
 #画直方图
 n, bins, patches = plt.hist(popular, bins=300, facecolor='blue', alpha=1)# hist函数可以直接绘制直方图# arr: 需要计算直方图的一维数组# bins: 直方图的柱数，可选项，默认为10# facecolor: 直方图颜色 # alpha: 透明度
 plt.show()
 print('灰度图像长度',len(popular))



 num = 10  #初始种群数
 ori_popular = ori_popular(num) # 得到原始种群的基因
 ori_popular_gene = encode(ori_popular)  # 8位基因
 new_popular_gene = ori_popular_gene
 y = []
 a = 0
 # 繁衍代数
 for i in range(10):
    new_popular_gene = Selection_Crossing(gray,new_popular_gene)
    new_popular_gene = Variation(new_popular_gene)

    # 求当前函数值的平均值
    new_popular = decode(new_popular_gene)  # 解码==适应性函数
    fitness = enfitness(gray,new_popular)
    sum = 0
    for j in fitness:
        sum += j
    a = sum / len(fitness)
    y.append(a)

 plt.plot(y)
 plt.show()
 print('阈值',a)

 ####### 显示分割图像
 threshold(gray, a)  # 1.png 164


















