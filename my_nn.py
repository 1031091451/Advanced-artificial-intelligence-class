import tensorflow as tf
import numpy as np
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"]='3'

#26个字母 数据集大小为26
data_size = 26
#训练轮数设为10000 可调
STEPS = 10000
#每个batch大小 可调  小于26
batch_size = 8

#输入 每个字母输入当成26维向量 如'a' -> [1,0...0]。输出同
x = tf.compat.v1.placeholder(tf.float32,shape=(None,26),name = 'x-input')
y_ = tf.compat.v1.placeholder(tf.float32,shape=(None,26),name = 'y-input')

#权重
w1 = tf.Variable(tf.random.normal([26,26],stddev=1,seed =1))
w2 = tf.Variable(tf.random.normal([26,26],stddev=1,seed =1))
w3 = tf.Variable(tf.random.normal([26,26],stddev=1,seed =1))


#偏置
bias1 = tf.Variable(tf.constant(0.1,shape=[26]))
bias2 = tf.Variable(tf.constant(0.1,shape=[26]))
bias3 = tf.Variable(tf.constant(0.1,shape=[26]))

#前向传播  三层，每层26维 
a1 = tf.nn.sigmoid(tf.matmul(x,w1)+bias1)
a2 = tf.nn.sigmoid(tf.matmul(a1,w2)+bias2)
y = tf.nn.sigmoid(tf.matmul(a2,w2)+bias3)



#损失函数(交叉熵)
cross_entropy = -tf.reduce_mean(y_ * tf.math.log(tf.clip_by_value(y,1e-10,1.0)) +(1-y_)*tf.math.log(tf.clip_by_value(1-y,1e-10,1.0)))

#优化  学习率0.001
train_step = tf.compat.v1.train.AdamOptimizer(0.001).minimize(cross_entropy)

#训练数据 26个字母的向量矩阵
X = []
for i in range(26):
    tmp = []
    for j in range(26):
        if j==i:
            tmp.append(1)
        else:
            tmp.append(0)
    X.append(tmp)

Y= []
for temp in X:
    tmp = list(temp)
    tmp[1:] = temp[:-1]
    tmp[0] = temp[-1]
    Y.append(tmp)

train_x = np.array(X)
train_y = np.array(Y)


with tf.compat.v1.Session() as sess:
    #初始化
    init_op = tf.compat.v1.global_variables_initializer()
    sess.run(init_op)
    
    #训练阶段
    print("Begin training.")
    for i in range(STEPS):
        start = (i*batch_size) % data_size
        end = min(start+batch_size,data_size)
        sess.run(train_step,feed_dict={x:train_x[start:end],y_:train_y[start:end]})
        if i % 1000 == 0:
            total_cross_entropy = sess.run(cross_entropy,feed_dict={x:train_x,y_:train_y})
            print("STEPS: %d/%d,cross entropy on all data: %g" % (i,STEPS,total_cross_entropy))
    print("Training finished.")

    #测试阶段
    letter_dict = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    flag = 1
    while flag:
        test_letter = input("Give a letter to predict(auto translated to lower case):").lower()
        while test_letter not in letter_dict:
            test_letter = input("Not a letter,try again:").lower()
        in_index = letter_dict.index(test_letter)
        test_x = []
        #创建输入字符的向量
        for i in range(26):
            if i == in_index:
                test_x.append(1)
            else:
                test_x.append(0)
        test_x = np.reshape(np.array(list(test_x)),newshape=(1,26))
        #得到预测结果  转为字符
        predict = sess.run(y,feed_dict={x:test_x})
        test_y = list(predict[0])
        ret = test_y.index(max(test_y))
        print("Predict Next letter:",letter_dict[ret])
        flag = int(input("Next one(0 to quit and 1 to continue):"))
    print("Exit.")