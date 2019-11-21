import random
import math
import matplotlib.pyplot as plt
PI = math.pi

# x y范围为-1 1
# 假设保留小数点后5位
# 则1-(-1) =2
#   2**17 < 2*100000 < 2**18
#两个都是18位编码  共36位

#初始化种群
def init_Population(population_size,len_1,len_2):
    """
    种群大小  第一段染色体 与第二段染色体长度
    去初始化种群
    """
    population = []
    for i in range(population_size):
        chromosome = ''
        for j in range(len_1+len_2):
            chromosome += str(random.randint(0,1))
        population.append(chromosome)
    return population
#计算适应度
def calc_adaptability(population,len_1,len_2):
    #print("calc adaptability")
    eva = []
    for i in range(len(population)):
        temp_1 = int(population[i][:len_1],2)
        temp_2 = int(population[i][len_1:],2)
        x_1 = -1 + temp_1/(pow(2,len_1)-1)
        x_2 = -1 + temp_2/(pow(2,len_2)-1)
        temp = 1*x_1*math.sin(4*x_1*PI) - x_2 * math.sin(4*PI*x_2+PI)+1
        if temp<0:
            temp = 0.0
        eva.append(temp)
    #print("calc adaptability finished")
    return eva

#根据适应度选择
def selection(population,len_1,len_2):
    #print("begin selection")
    evalue = calc_adaptability(population,len_1,len_2)
    sum_evalue = sum(evalue)
    prob =[]
    temp = 0
    new_population = []
    for e in evalue:
        temp += e/sum_evalue
        prob.append(temp)
    for i in range(len(prob)):
        rand = random.random()
        j = 0
        while j<len(population):
            if rand<prob[j]:
                new_population.append(population[j])
                break
            else:
                j = j+1
    #print("selection finished")
    return new_population
#随机交叉拼接，概率为
def crossover(population,pc):
    '''
    小于交叉率交叉拼接
    '''
    #print("begin crossover")
    for i in range(len(population)-1):
        if random.random() > pc:
            continue
        rand = random.randint(0,len(population[0])-1)
        temp_1 = population[i][:rand]+population[i+1][rand:]
        if i==len(population)-2:
            temp_2 = population[i+1][:rand] + population[i][rand:]
            population[i+1]=temp_2
        population[i]=temp_1
    #print("crossover finished")
    return population
#随机位变异  小于pm才变异
def mutation(population,pm):
    #print("begin mutation")
    for i in range(len(population)):
        if random.random() > pm:
            continue
        rand_chr = random.randint(0,len(population[0])-1)
        if population[i][rand_chr]=='1':
            population[i] =population[i][:rand_chr] + '0' + population[i][rand_chr+1:]
        else:
            population[i] =population[i][:rand_chr] + '1' + population[i][rand_chr+1:]
    #print("mutation finished")
    return population

def get_max(population,len_1,len_2):
    max_val = 0
    X = []
    for i in range(len(population)):
        temp_1 = int(population[i][:len_1],2)
        temp_2 = int(population[i][len_1:],2)
        x_1 = -1 + temp_1/(pow(2,len_1)-1)
        x_2 = -1 + temp_2/(pow(2,len_2)-1)
        temp = 1*x_1*math.sin(4*x_1*PI) - x_2 * math.sin(4*PI*x_2+PI)+1
        if temp>max_val:
            max_val=temp
            X =[x_1,x_2]
    return max_val,X


def main():
    #初始种群大小
    population_size =1000
    #交叉拼接概率
    pc = 0.5
    #变异概率
    pm = 0.05
    #染色体上两个变量的所占长度
    len_1 = 18
    len_2 = 18
    population = init_Population(population_size,len_1,len_2)
    figure_index = []
    figure_value = []
    max_value = 0
    x_y = []
    for i in range(1000):
        population = selection(population,len_1,len_2)
        population = crossover(population,pc)
        population = mutation(population,pm)
        max_val,X = get_max(population,len_1,len_2)
        if max_val>max_value:
            max_value = max_val
            x_y = X
        print("After %d steps,max value is %.5f, with x=%.5f, y=%.5f" %(i,max_value,x_y[0],x_y[1]))
        figure_index.append(i)
        figure_value.append(max_val)
    print("max value: %.5f ,with x=%.5f, y=%.5f."% (max_value,x_y[0],x_y[1]))

    fig = plt.figure()
    plt.plot(figure_index, figure_value, color='r', linestyle='-')
    plt.show()

if __name__ == '__main__':
    main()