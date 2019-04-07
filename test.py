#############################################
#  Created by Suntuo
#  2019-4-5 22:03
#  This code is a test of the basic component
#  of the model, which is used to get the 
#  image from localdisk, and use the model to
#  distinguish it.
#
#############################################
from PIL import Image
import flask
import tensorflow as tf
import matplotlib.pyplot as plt

app = flask.Flask(__name__)
model = None
sess = tf.InteractiveSession()


def image_prepare(image):
    # image = Image.open('C:/Users/suntuo/Desktop/mnistoutput/5.png')  # Abandoned

    image = image.resize((28, 28))
    # plt.imshow(image)  # plot the image
    # plt.show()
    image = image.convert('L')
    tv = list(image.getdata())
    tva = [(255-x) * 1.0 / 255.0 for x in tv]
    return tva


def weight_variable(shape):
    initial = tf.truncated_normal(shape,stddev = 0.1)
    return tf.Variable(initial)


def bias_variable(shape):
    initial = tf.constant(0.1,shape = shape)
    return tf.Variable(initial)


def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides = [1,1,1,1], padding = 'SAME')


def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1,2,2,1], strides=[1,2,2,1], padding='SAME')


# use the model
def model(result):
    x = tf.placeholder(tf.float32, [None, 784])
    y_ = tf.placeholder(tf.float32, [None, 10])

    W_conv1 = weight_variable([5, 5, 1, 32])
    b_conv1 = bias_variable([32])

    x_image = tf.reshape(x, [-1, 28, 28, 1])

    h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1)+b_conv1)
    h_pool1 = max_pool_2x2(h_conv1)

    W_conv2 = weight_variable([5, 5, 32, 64])
    b_conv2 = bias_variable([64])

    h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2)+b_conv2)
    h_pool2 = max_pool_2x2(h_conv2)

    W_fc1 = weight_variable([7 * 7 * 64, 1024])
    b_fc1 = bias_variable([1024])

    h_pool2_flat = tf.reshape(h_pool2, [-1, 7 * 7 * 64])
    h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1)+b_fc1)

    keep_prob = tf.placeholder("float")
    h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

    W_fc2 = weight_variable([1024, 10])
    b_fc2 = bias_variable([10])

    y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2)+b_fc2)

    cross_entropy = -tf.reduce_sum(y_ * tf.log(y_conv))
    train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
    correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

    saver = tf.train.Saver()

    sess.run(tf.global_variables_initializer())
    saver.restore(sess, "./SAVE/model.ckpt")  # use the model generated from grneratemodel.py

    prediction = tf.argmax(y_conv, 1)
    predint = prediction.eval(feed_dict={x:[result], keep_prob:1.0}, session=sess)
    return predint


image = Image.open('C:/Users/suntuo/Desktop/mnistoutput/5.png') #Testing without docker
result = image_prepare(image)
predint = model(result)
data = predint[0]
print('识别结果:')
print(data)

