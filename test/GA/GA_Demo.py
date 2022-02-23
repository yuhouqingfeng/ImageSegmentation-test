import matplotlib.pyplot as plt
import numpy as np
import random
import  cv2

def ori_popular(num):
    popular = []
    for i in range(num):
        x = random.randint(0, 255)  # 在此范围内生成一个随机浮点数
        popular.append(x)
    return popular

def encode(popular):  # 为图像像素进行基因编码
    popular_gene = []
    for i in range(len(popular)):
        data = bin(popular[i])
        popular_gene.append(data)
    return popular_gene

def decode(popular_gene):  #新种群解码
    fitness = []
    for i in range(len(popular_gene)):
        data = int(popular_gene[i],2)

        fitness.append(data)
    return fitness

# 选择and交叉。选择用轮牌赌，交叉概率为0.66
def  Selection_Crossing(popular_gene):
    fitness = decode(popular_gene)
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
    num = 10
    ori_popular = ori_popular(num)  # 得到原始种群的基因
    ori_popular_gene = encode(ori_popular)  # 8位基因
    new_popular_gene = ori_popular_gene
    y = []
    #繁衍代数
    for i in range(100):
        new_popular_gene = Selection_Crossing(new_popular_gene)
        new_popular_gene = Variation(new_popular_gene)

        #求当前函数值的平均值
        fitness = decode(new_popular_gene)  # 解码==适应性函数
        print(fitness)
        sum = 0
        for j in fitness:
            sum += j
        a = sum / len(fitness)
        y.append(a)


    plt.plot(y)
    plt.show()