'''
Script to perform all the queries.
'''

import mysql.connector
from neo4jrestclient.client import GraphDatabase
from neo4jrestclient.query import Q
import pandas as pd
import pymysql
import time
import matplotlib.pyplot as plt

#mydb = mysql.connector.connect(
#  host="localhost",
#  user="yourusername",
#  passwd="yourpassword"
#)
#
#print(mydb)

#Connect to Neo4j database
gbd = GraphDatabase("http://localhost:7474/db/data/")

'''
Page Rank ---------------------------------------------------------------------
'''

def page_rank(k):
    '''
    Function to run PageRank algorithm and returns pandas dataframe containing
    top k page rank scores
    '''
    
    #Query to retrieve PageRank results
    q = """CALL algo.pageRank.stream('Resource', 'ns0__isRelatedTo', {iterations:20, dampingFactor:0.85, graph:"huge"})
    YIELD nodeId, score
    
    RETURN algo.asNode(nodeId).ns0__vidID AS page,score
    ORDER BY score DESC
    LIMIT """ + str(2*k)
    
    #Run PageRank algorithm
    result = gbd.query(q = q)
    
    #Collect results in Pandas df
    df = pd.DataFrame(result[:])
    
    #Rename columns
    df = df.rename({0:"Video", 1:"PageRank"}, axis = 1)
    
    #Drop rows with VideoID of None
    df = df.dropna()
    
    #Reset the index
    df = df.reset_index()
    df = df.drop({"index"}, axis = 1)
    
    #Return top k queries
    return df.head(k)

start = time.time()
scores = page_rank(10)

print(scores)
end = time.time()

del scores

print("Query: ", end - start, "s", sep = "")

host = 'localhost'
user = 'root'
password = 'January12995!'

conn = pymysql.connect(host=host, 
                      user=user, 
                      password=password,
                      db = "Youtube",
                      autocommit=True)

'''
Top K -------------------------------------------------------------------------
'''

def top_k(k):
    
    # Create a cursor object

    cursor = conn.cursor()

    # SQL query string
    sqlQuery = "SELECT * from NormalCrawl LIMIT " + str(k) + ";"

    # Execute the sqlQuery
    cursor.execute(sqlQuery)

    #Fetch all the rows
    rows = cursor.fetchall()

    for row in rows:
        print(row)
        print(len(row))

#        print(row["id"])
#        print(row["firstname"])
#        print(row["lastname"])
#        print(row["courseid"])

#print(top_k(100))
        
'''
Degree Distribution -----------------------------------------------------------
'''
        
def degree_dist():
    '''
    Function to get the degree distribution
    '''
    
    #Query to retrieve PageRank results
    q = """MATCH (n:Resource) RETURN n.ns0__vidID AS VideoID, SIZE((n)-[:ns0__isRelatedTo]->()) AS OutDegree, size((n)<-[:ns0__isRelatedTo]-()) AS InDegree;"""
    
    #Run PageRank algorithm
    result = gbd.query(q = q)
    
    #Collect results in Pandas df
    df = pd.DataFrame(result[:])
    
    #Rename columns
    df = df.rename({0:"Video", 1:"In", 2:"Out"}, axis = 1)
    
    #Drop rows with VideoID of None
    df = df.dropna()
    
    #Reset the index
    df = df.reset_index()
    df = df.drop({"index"}, axis = 1)
    
    #Return top k queries
    return df
    

start = time.time()

degrees = degree_dist()

end = time.time()

degrees.head()

degrees = degrees[degrees.Out < 50]
degrees = degrees[degrees.In < 30]
        
degrees.hist(normed = True, bins = 40, figsize = (10, 5))
plt.savefig('C:\\Users\\Jdpre\\Desktop\\Big Data\\Project\\Degrees.png')

print("Minimum In-Degree: ", min(degrees.In))
print("Average In-Degree: ", sum(degrees.In) / degrees.shape[0])
print("Maximum In-Degree: ", max(degrees.In))

print("Minimum Out-Degree: ", min(degrees.Out))
print("Average Out-Degree: ", sum(degrees.Out) / degrees.shape[0])
print("Maximum Out-Degree: ", max(degrees.Out))

print("Query: ", end - start, "s", sep = "")


'''
Subgraph ----------------------------------------------------------------------
'''

start = time.time()

#Query
q = """MATCH (n) -- (m) WHERE n.ns0__uploader = m.ns0__uploader
RETURN n.ns0__uploader, n.ns0__vidID, m.ns0__vidID;"""

#Run PageRank algorithm
result = gbd.query(q = q)

#Collect results in Pandas df
df = pd.DataFrame(result[:])

end = time.time()

#Rename columns
df = df.rename({0:"Uploader", 1:"Video1", 2:"Video2"}, axis = 1)

#Drop rows with VideoID of None
df = df.dropna()

#Reset the index
df = df.reset_index()
df = df.drop({"index"}, axis = 1)

print(df)
print("Query: ", end - start, "s", sep = "")

del df




