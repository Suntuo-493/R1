###################################################
#  Created by Suntuo
#  2019-4-7 04:31
#  This code is a test of a basic component of 
#  the project, which is used to upload information
#  to the cassandra database.
#  Both of them are in the docker.
#  The cassandra is in http://172.17.0.2
#  port:9042
#  use the --link name_of_container:name_of_link
##################################################
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
import datetime
import numpy as np
KEYSPACE = "mykeyspace"
predictresult = 4
image_arr = [2, 7, 3, 5, 1, 3, 1, 1, 1, 2, 3, 4, 4, 5, 3, 4, 4, 4, 3, 1, 2, 3]
image_info= ','.join(str(i) for i in image_arr)

#connnect to the cassandra
cluster = Cluster(contact_points=['127.0.0.1'],port=9042)
session = cluster.connect()
mnist_result_value = predictresult
image_num_value = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
date_value = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
information_value = image_info
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

