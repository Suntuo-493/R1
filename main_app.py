
# from PIL import Image, # Testing without docker
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
import datetime
import flask
import tensorflow as tf
# import matplotlib.pyplot as plt

app = flask.Flask(__name__)
model = None
sess = tf.InteractiveSession()
KEYSPACE = "mykeyspace"


def send_to_cassandra(predictresult, image_info):
    information_value = ','.join(str(i) for i in image_info)
    cluster = Cluster(contact_points = ['127.0.0.1'], port = 9042)
    session = cluster.connect()
    mnist_result_value = predictresult
    image_num_value = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    date_value = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        session.execute("""
           CREATE KEYSPACE %s
           WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' }
           """ % KEYSPACE)
    except:
        pass
        # keyspace already exist
    session.set_keyspace(KEYSPACE)
    try:
        session.execute("""
            CREATE TABLE mnist_user_table (
                date text,
                mnist_result int,
                image_num text,
                PRIMARY KEY (image_num)
             )
             """)
    except:
        pass
        # table already exist
    try:
        session.execute("""
            CREATE TABLE image (
                information text,
                image_num text,
                PRIMARY KEY (image_num)
             )
             """)
    except:
        pass

    session.execute("""
    		INSERT INTO mnist_user_table (date, mnist_result, image_num) 
    		Values (%s,%s,%s)
    		""",
                    (date_value, mnist_result_value, image_num_value)
                    )
    session.execute("""
    		INSERT INTO image (information, image_num) 
    	        Values (%s,%s) 
    		""",
                    (information_value, image_num_value)
                    )



def image_prepare(image):
    # image = Image.open('C:/Users/suntuo/Desktop/mnistoutput/5.png')  # Testing without docker

    image = image.resize((28, 28))
    # plt.imshow(image)  # 显示需要识别的图片
    # plt.show()
    image = image.convert('L')
    tv = list(image.getdata())
    tva = [(255-x) * 1.0 / 255.0 for x in tv]
    return tva


def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)


def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)


def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')


def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')


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
    saver.restore(sess, "./SAVE/model.ckpt")  # 使用模型，参数和之前的代码保持一致

    prediction = tf.argmax(y_conv, 1)
    predint = prediction.eval(feed_dict={x:[result], keep_prob:1.0}, session=sess)
    return predint


@app.route("/predict", methods=["POST"])
def predict():
    # initialize the data dictionary that will be returned from the
    # view
    data = {"success": False}

    # ensure an image was properly uploaded to our endpoint
    if flask.request.method == "POST":
        if flask.request.files.get("image"):
            # read the image in PIL format
            image = flask.request.files["image"].read()

            # pre-process the image and prepare it for classification
            result = image_prepare(image)

            # classify the input image and then initialize the list
            # of predictions to return to the client
            predint = model(result)
            data = predint[0]
            send_to_cassandra(data, result)
            data["success"] = True

    # return the data dictionary as a Json response
    return flask.jsonify(data)


if __name__ == "__main__":

    app.run(port=7777)
