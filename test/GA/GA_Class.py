import numpy
import matplotlib.pyplot as plt
import random
# import operator


x_label=[]
y_label=[]#将每一步迭代的结果存储到列表中,便于画图
class GA(object):
    def __init__(self,length,number,lower_boundary,upper_boundary,iter_number):
        self.length = length#确定染色体编码长度
        self.number = number#确定初始化种群数量
        self.lower_boundary = lower_boundary#定义域下界
        self.upper_boundary = upper_boundary#定义域上届
        self.population = self.initial_population(length,number)
        self.iteration(iter_number)

    def initial_population(self,length,number):#初始化种群
        return [self.initial_chromosome(length) for i in range(number)]

    def initial_chromosome(self,length):#编码
            chromosome = 0
            for i in range(self.length):
                chromosome |= (1 << i) * random.randint(0, 1)   #按位或运算
            return chromosome


    def decode(self,chromosome):#解码
        x = chromosome*(self.upper_boundary-self.lower_boundary)/(2**self.length-1)
        return x

    def fitness_function(self,chromosome):#适应度函数
        x = self.decode(chromosome)
        y = x + 10 * numpy.sin(5 * x) + 7 * numpy.cos(4 * x)
        return y

    def evolution(self, retain_rate=0.2, random_select_rate=0.5, mutation_rate=0.01):
        """
        对当前种群依次进行选择、交叉并生成新一代种群，然后对新一代种群进行变异
        """
        parents = self.selection(retain_rate, random_select_rate)
        self.crossover(parents)
        self.mutation(mutation_rate)

    def selection(self,retain_rate, random_select_rate):  #选择父代
        graded = [(self.fitness_function(chromosome), chromosome) for chromosome in self.population]
        sort = [x[1] for x in sorted(graded, reverse=True)]

        retain_length=int(len(sort)*retain_rate)

        #选出适应性强的个体，精英选择
        parents=sort[:retain_length]    #sort[0:retain_length]

        # 选出适应性不强，但是幸存的染色体
        for chromosome in sort[retain_length:]:   #sort[retain_length:len(sort)]
            if random.random() < random_select_rate:
                parents.append(chromosome)
        return parents

    def crossover(self,parents):#交叉
        children=[]
        #需要繁殖的子代数量
        target_number=len(self.population)-len(parents)
       #开始繁殖
        while len(children) < target_number:
            father = random.randint(0, len(parents) - 1)
            mother = random.randint(0, len(parents) - 1)
            if father != mother:
                father = parents[father]
                mother = parents[mother]

                # 随机选取交叉点
                cross_point = random.randint(0, self.length)
                # 生成掩码，方便位操作
                mark = 0
                for i in range(cross_point): # 0~16
                    mark |= (1 << i)  #将1左移i位
                print('cross_point = ',cross_point)
                print('mark = ',bin(mark),'\tfather = ',bin(father),'\t\tfather&mask = ',bin(father & mark))
                print('~mark = ', bin(~mark), '\tmother = ', bin(mother), '\t\tmother&~mask = ', bin(mother & ~mark))
                # 孩子将获得父亲在交叉点前的基因和母亲在交叉点后（包括交叉节点）的基因  0位是前
                child = ((father & mark) | (mother & ~mark)) # & ((1 << self.length) - 1)  # ~按位取反 ~mark = -mark-1
                children.append(child)
        self.population = parents + children

    def mutation(self,rate):
        for i in range(len(self.population)):
            if random.random() < rate:
                j = random.randint(0, self.length - 1)#s随机产生变异位置
                self.population[i] ^= 1 << j  #产生变异   <<左移    ^按位异或运算


    def result(self):
        graded = [(self.fitness_function(chromosome), chromosome) for chromosome in self.population]
        graded = [x[1] for x in sorted(graded, reverse=True)] #按第一个元素降序排列
        # print('近优的x值为：', self.decode(graded[0]),
        #       '近优的y值为：', self.fitness_function(graded[0]))
        #将每一步迭代的结果存储到列表中
        y_label.append(self.fitness_function(graded[0]))
    def iteration(self,iter_number):
        for i in range(iter_number):
            self.evolution()
            self.result()
            x_label.append(i)
g1=GA(17,100,0,9,50)#建立一个实例

plt.plot(x_label,y_label)
plt.show()

