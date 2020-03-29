# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 21:54:47 2019

@author: Nathan

Reads in all the normal crawl data into a single pandas dataframe
clean_data.py needs to be run on the data first so that it will read in correctly to pandas
"""

import pandas as pd
import os
import re
import time
import mysql.connector
import pymysql

start = time.time()
os.chdir('C:\\Users\\Jdpre\\Desktop\\Big Data\\Project\\Data') # This is the folder I have all the data in
master_normal = pd.DataFrame()
master_update = pd.DataFrame()
master_file_size = pd.DataFrame()
master_user = pd.DataFrame()

#"""
#'NormalCrawl' is the subfolder with all the data for the normal crawl,
#so .\Data\NormalCrawl, is where it's stored.
#If you want to read different data, obviously change this.
#"""

#Gets all normal crawl data
for root, dirs, files, in os.walk('NormalCrawl', topdown=True):
    for fname in files:
        if re.match('\d.txt', fname): # looks for all files that are "a number".txt
            print(os.path.join(root,fname))
            #this is only using the first 9 columns. If you want all, then get rid of this parameter
            temp_db = pd.read_csv(os.path.join(root,fname), usecols=[*range(9)], header=None, sep='\t', error_bad_lines=False)
            master_normal = pd.concat([master_normal, temp_db]) # this is the dataframe object you can reference

#Gets all the updated crawl data            
for root, dirs, files, in os.walk('UpdateCrawl', topdown=True):
    for fname in files:
        if re.match('update.txt', fname): # looks for all files that are "a number".txt
            print(os.path.join(root,fname))
            #this is only using the first 9 columns. If you want all, then get rid of this parameter
            temp_db = pd.read_csv(os.path.join(root,fname), usecols=[*range(5)], header=None, sep='\t', error_bad_lines=False)
            master_update = pd.concat([master_update, temp_db]) # this is the dataframe object you can reference

#Gets all file size and bitrate information data
for root, dirs, files, in os.walk('FileSize', topdown=True):
    for fname in files:
        if re.match('size.txt', fname): # looks for all files that are "a number".txt
            print(os.path.join(root,fname))
            #this is only using the first 9 columns. If you want all, then get rid of this parameter
            temp_db = pd.read_csv(os.path.join(root,fname), usecols=[*range(3)], header=None, sep='\t', error_bad_lines=False)
            master_file_size = pd.concat([master_file_size, temp_db]) # this is the dataframe object you can reference

#Gets all the user information
for root, dirs, files, in os.walk('Users', topdown=True):
    for fname in files:
        if re.match('user.txt', fname): # looks for all files that are "a number".txt
            print(os.path.join(root,fname))
            #this is only using the first 9 columns. If you want all, then get rid of this parameter
            temp_db = pd.read_csv(os.path.join(root,fname), usecols=[*range(3)], header=None, sep='\t', error_bad_lines=False)
            master_user = pd.concat([master_user, temp_db]) # this is the dataframe object you can reference

end = time.time()
print(round(end-start, 2))

'''
Once this is done you export master to csv, using the command: master.to_csv().
You may have to specify where you want to export it, and what name you want to give the file
'''

master_normal.to_csv("C:\\Users\\Jdpre\\Desktop\\Big Data\\Project\\Data\\NormalCrawl.csv")
master_update.to_csv("C:\\Users\\Jdpre\\Desktop\\Big Data\\Project\\Data\\UpdateCrawl.csv")
master_file_size.to_csv("C:\\Users\\Jdpre\\Desktop\\Big Data\\Project\\Data\\FileSize.csv")
master_user.to_csv("C:\\Users\\Jdpre\\Desktop\\Big Data\\Project\\Data\\Users.csv")

#Connect to MySQL
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="password"
)

#Create a cursor
mycursor = mydb.cursor(buffered = True)

#Create a new Database
mycursor.execute("CREATE DATABASE Youtube")

#Use newly created databse
mycursor.execute("Use Youtube")

#Create NormalCrawl table
mycursor.execute("""CREATE TABLE NormalCrawl (
        VideoID VARCHAR(255) NOT NULL,
        Uploader VARCHAR(255),
        Age DOUBLE,
        Category VARCHAR(255),
        Length DOUBLE,
        Views INT,
        Rate DOUBLE,
        Ratings INT,
        Comments INT,
        PRIMARY KEY (VideoID)
        );""")

#Create UpdateCrawl table
mycursor.execute("""CREATE TABLE UpdateCrawl (
        VideoID VARCHAR(255) NOT NULL,
        Views INT,
        Rate DOUBLE,
        Ratings INT,
        Comments INT,
        PRIMARY KEY (VideoID)
        );""")

#Create FileSize table
mycursor.execute("""CREATE TABLE FileSize (
        VideoID VARCHAR(255) NOT NULL,
        VideoLength INT,
        FileSize INT,
        PRIMARY KEY (VideoID)
        );""")

#Create Users table
mycursor.execute("""CREATE TABLE Users (
        Uploader VARCHAR(255) NOT NULL,
        Uploads INT,
        Watches INT,
        Friends INT,
        PRIMARY KEY (Uploader)
        );""")



def csv_to_mysql(load_sql, host, user, password):
    '''
    This function load a csv file to MySQL table according to
    the load_sql statement.
    '''
    con = pymysql.connect(host=host,
                            user=user,
                            password=password,
                            autocommit=True,
                            local_infile=1)
    print('Connected to DB: {}'.format(host))
    # Create cursor and execute Load SQL
    cursor = con.cursor()
    cursor.execute(load_sql)
    print('Succuessfully loaded the table from csv.')
    con.close()

#Load local files into MySQL
load_sql_normal = """LOAD DATA LOCAL INFILE 'C:/Users/Jdpre/Desktop/Big Data/Project/Data/NormalCrawl.csv' INTO TABLE Youtube.NormalCrawl FIELDS TERMINATED BY ',' ENCLOSED BY '"';"""
load_sql_update = """LOAD DATA LOCAL INFILE 'C:/Users/Jdpre/Desktop/Big Data/Project/Data/UpdateCrawl.csv' INTO TABLE Youtube.UpdateCrawl FIELDS TERMINATED BY ',' ENCLOSED BY '"';"""
load_sql_file_size = """LOAD DATA LOCAL INFILE 'C:/Users/Jdpre/Desktop/Big Data/Project/Data/FileSize.csv' INTO TABLE Youtube.FileSize FIELDS TERMINATED BY ',' ENCLOSED BY '"';"""
load_sql_users = """LOAD DATA LOCAL INFILE 'C:/Users/Jdpre/Desktop/Big Data/Project/Data/Users.csv' INTO TABLE Youtube.Users FIELDS TERMINATED BY ',' ENCLOSED BY '"';"""

#Login information
host = 'localhost'
user = 'root'
password = 'password'

csv_to_mysql(load_sql_normal, host, user, password)
csv_to_mysql(load_sql_update, host, user, password)
csv_to_mysql(load_sql_file_size, host, user, password)
csv_to_mysql(load_sql_users, host, user, password)

