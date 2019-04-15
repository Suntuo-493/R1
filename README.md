Deploy mnist application in docker
====

Create the model
------
This model is python application with Concolutional Neural Networks.<br>
After training for 20000 times. It will has about 99.5% accuracy.<br>
The Model will be saved in a file folder called Save.<br>

Set the docker
------
In this project the application will be deployed in the docker container.<br>
<br>
First, put requirements,Dockerfile and app.py in the same filefolder.<br>
And use the following command:<br>
```Bash
sudo docker build -t mnist-app:latest .
```
<br>
Second,run the Docker container<br>
We can run our docker container for testing<br>

```Bash
sudo docker run -d -p 9042:9042 mnist-app
```
<br>
Finally,Check the container by:<br>

```bash
sudo docker ps -a
```
<br>

```bash
[suntuo@suntuo-493 ~]$ sudo docker ps -a
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS                    PORTS                    NAMES
d82f65802166        mnist-app           "python app.py"     About an hour ago   Up About an hour          0.0.0.0:9042->9042/tcp   apple_tree
```
<br>

Set the Cassandra
----
Pull the cassandra image from the docker server.<br>
For example, we can pull cassandra version 3.11.2<br>

```Bash
sudo docker pull cassandra:3.11.2
```
<br>
And then, deploy activitate cassandra container from the image.<br>

```Bash
sudo docker run -d --name "some-cassandra" -d -e cassandra:3.11.2
```
<br>

Link the container
-----
Use the link function to create one-way link from application to Database.<br>

```Bash
sudo docker run -d -p --name some-cassandra --link some-cassandra:linkname mnist_app:latest /bin/bash
```
<br>
And then we enter the mnist container, use ping command to check the connection. We can found they connection successfully.<br>
However, in Cassandra container, it will be failed. Because the link is one-way.<br>

Upload the graph
------
From a terminal, load the  filefolder with the graph willing to recognize.<br>
Use the following to submit the graph.<br>

```Bash
use curl -X post -F @image=image_name.png "http://127.0.0.1:5000/predict
```
And we will get the result of recongnization.<br>
And in the cassandra container <br>
```bash
```cqlsh: use mykeyspace;
```cqlsh:mykeyspace> SELECT * FROM image_num;

image_num      | date                | mnist_result
---------------+---------------------+--------------
20190410130802 | 2019-04-10 13:08:02 |            4
20190410132058 | 2019-04-10 13:20:58 |            6
20190415140809 | 2019-04-15 14:08:09 |            3
```
Then we can find the data of this testing<br>
