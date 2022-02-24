import numpy as np
from ImageSeg_GA_OTSU.ImageSeg_OTSUclass import otsu

N = 10                      # 初始种群数
length = 8                  # 染色体长度
retain_Rate = 0.2           # 自身保留率
random_Select_Rate = 0.5    # 随机选择率
Variation_Rate = 0.1        # 自身突变率


class GA:
    def __init__(self, image):
        self.image = image
        self.population = np.random.randint(0, 256,N)
        self.length = length
        self.retain_Rate = retain_Rate
        self.random_Select_Rate = random_Select_Rate
        self.Variation_Rate = Variation_Rate


    def Evolution(self):
        parents = self.Selection()              # 选择
        self.Crossing(parents)                  # 交叉
        self.Variation(self.Variation_Rate)     # 突变

    def Selection(self):
        graded = [(self.Fitness(chromosome), chromosome) for chromosome in self.population]
        graded = [x[1] for x in sorted(graded, reverse=True)]
        # 选出适应性强的染色体
        retain_length = int(len(graded) * self.retain_Rate)
        parents = graded[:retain_length]
        # 选出适应性不强，但是幸存的染色体
        for chromosome in graded[retain_length:]:
            if np.random.random() < self.random_Select_Rate:
                parents.append(chromosome)
        return parents

    def Fitness(self, chromosome):
        fitness = otsu(self.image, chromosome)
        return fitness

    def Crossing(self, parents):
        children = []
        target_count = len(self.population) - len(parents)
        while len(children) < target_count:
            male = np.random.randint(0, len(parents) - 1)
            female = np.random.randint(0, len(parents) - 1)
            if male != female:
                male = parents[male]
                female = parents[female]

                # 随机选取交叉点
                cross_pos = np.random.randint(0, self.length)
                mask = 0
                for i in range(cross_pos):
                    mask |= (1 << i)
                probability = np.random.uniform(0,1)  #后代个数比率
                # 孩子将获得父亲在交叉点前的基因和母亲在交叉点后（包括交叉点）的基因
                child = ((male & mask) | (female & ~mask)) & ((1 << self.length) - 1)  #255
                children.append(child)
                if probability < 0.02: #产生两个后代
                    cross = np.random.randint(0, self.length)
                    ma = 0
                    for i in range(cross):
                        ma |= (1 << i)
                    child = ((male & ma) | (female & ~ma)) & ((1 << self.length) - 1)
                    children.append(child)
        self.population = parents + children

    def Variation(self, rate):
        for i in range(len(self.population)):
            if np.random.random() < rate:
                j = np.random.randint(0, self.length - 1)
                self.population[i] ^= 1 << j

    def Result(self):
        graded = [(self.Fitness(chromosome), chromosome) for chromosome in self.population]
        graded = [x[1] for x in sorted(graded, reverse=True)]
        return graded[0]