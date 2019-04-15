Deploy mnist application in docker
====

About the model
------
This model is python application with Concolutional Neural Networks.<br>
After training for 20000 times. It will has about 99.5% accuracy.<br>
The Model will be saved in a file folder called Save.<br>

About the docker
------
In this project the application will be deployed in the docker container.<br>
<br>
First, put requirements,Dockerfile and app.py in the same filefolder.<br>
And use the following command:
```Bash
sudo docker build -t mnist-app:latest .
```
<br>
Second,run the Docker container
We can run our docker container for testing
```Bash
sudo docker run -d -p 9042:9042 mnist-app
```
<br>
Check the container by```bash
sudo docker ps -a
```

this is a program that can recognize the handwritten numbers.
use curl -X post -F @image=image_name.png "http://127.0.0.1:5000/predict" to submit the image
then you can get number as a result
the uploaded image, the time will be record in the cassandra
