Deploy mnist application in docker
====
Creation of the model
------
this is a program that can recognize the handwritten numbers.
use curl -X post -F @image=image_name.png "http://127.0.0.1:5000/predict" to submit the image
then you can get number as a result
the uploaded image, the time will be record in the cassandra
