#coding=utf-8
#问题规模假定为3x3  船每次装2个，初始为
#传教士   野人                传教士    野人
#  3      3   |船---------|    0       0
# 
# (x,y,z) 代表左岸的传教士 野人 船的状态(1代表在右岸 0代表在左岸)
# 则上述初始状态为(3,3,0) 
# 最终状态为(0,0,1)
# 

#当前操作的状态栈
state_stack = []
#所有可以进行的操作列表
boat_list = []

# 检测左岸状态和右岸状态是不是合法
def isRight(x,y):
    if x<0 or y<0 or x>3 or y>3:
        return False
    if x<y and x>0:
        return False
    if 3-x < 3-y and 3-x>0 :
        return False
    return True

# 将x,y,z状态下的 a个传教士和b个野人移走
def isRightBoot(x,y,a,b,flag):

    #船向左岸运送人    左岸变成x+a y+b flag变成1-flag
    if flag==1 and isRight(x+a,y+b):
        return True
    #船向右岸运人  左岸变成x-a y-b 1-flag
    if flag==0 and isRight(x-a,y-b):
        return True
    return False


#对每个状态找可行的 船运送结果
def findSln(x,y,flag):
    #状态不合法
    if  not isRight(x,y):
        return False
    #顺利结束
    if [x,y,flag] == [0,0,1]:
        return True
    #已经出现过的状态
    if [x,y,flag] in state_stack:
        return False
    state_stack.append([x,y,flag])
    available_boot = []
    #找到当前可用的所有操作
    for boot in boat_list:
        #船的状态一致
        if boot[2]==flag:
            if isRightBoot(x,y,boot[0],boot[1],boot[2]):
                available_boot.append(boot)
    
    #遍历每个可用操作
    for i in range(len(available_boot)):
        action = available_boot.pop()
        #做出尝试 失败后还原
        if flag:
            tmp_x = x + action[0]
            tmp_y = y + action[1]
        else:
            tmp_x = x - action[0]
            tmp_y = y - action[1]
        #船反向
        flag = 1-flag
        if findSln(tmp_x,tmp_y,flag):
            return True
        #失败后还原船状态
        else:
            flag = 1-flag
    state_stack.pop()
    return False   

#打印结果
def printResult():
    print("传道士\t野人|------------|传道士\t野人")
    for state in state_stack:
        if state[2]==1:
            print(state[0],"\t",state[1],"|----------船|",3-state[0],"\t",3-state[1])
        else:
            print(state[0],"\t",state[1],"|船----------|",3-state[0],"\t",3-state[1])

def main():   
    state_start = [3,3,0]
    state_stop= [0,0,1] 
    #得到船所有运送可能的集合
    
    for c in [0,1]:
        for a in [0,1,2]:
            for b in [0,1,2]:
                #船上只能有1 或者2 人                
                if a+b==1 or a+b ==2:
                    boat_list.append((a,b,c))
    
    #print("InitialState:",state_start)
    if not findSln(state_start[0],state_start[1],state_start[2]):
        print("No solution.")
    else:
        print("Get solution.")
        printResult()

if __name__=='__main__':
    main()