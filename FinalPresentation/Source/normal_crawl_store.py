'''
Script to read in all the Normal crawl data and store it as RDF
'''

import rdflib as rdf
from rdflib import URIRef, BNode, Literal, Graph
from rdflib.namespace import RDF, FOAF
import os

#Path to directory
path = r"C:/Users/Jdpre/Desktop/Big Data/Project/Normal Crawl/"

#Initialize the graph
g = Graph()
#g = g.parse("C:/Users/Jdpre/Desktop/Big Data/Project/normal_crawl.xml", format = "xml")

#Initialize the videos dictionary        
videos = {}

os.walk(path)

subdirs = [x[0] for x in os.walk(path)]

subdirs = [subdirs[i] for i in range(2, len(subdirs), 2)]

counter = 0

for subdir in subdirs:
    
    counter += 1
    print("\n", counter, "out of ", len(subdirs), ":\n")
    print("Number of videos: ", len(videos))
    
    for files in os.walk(subdir):
        
        for curr_file in files[2]:
            
            if curr_file != "log.txt":
                with open(subdir + "/" + curr_file) as file:
                    data = file.readlines()
                    
                    for i in range(len(data)):
                        if data[i].split("\t")[0] not in videos:
                            videos[data[i].split("\t")[0]] = BNode()
                            
print(len(videos))

counter = 0

for subdir in subdirs:
    counter += 1
    print("\n", counter, "out of ", len(subdirs), ":\n")
    print("Number of nodes: ", len(g))
    
#    if (counter % 20) == 0:
#        g.serialize("normal_crawl.xml", format = "xml")
    for files in os.walk(subdir):
        for curr_file in files[2]:
            print("Current file: ", curr_file)
            if curr_file != "log.txt":
                with open(subdir + "/" + curr_file) as file:
                    data = file.readlines()
                
                
                for i in range(len(data)):
                    curr_node = videos[data[i].split("\t")[0]]
                    vid_id = Literal(data[i].split("\t")[0])
                    
                    g.add((curr_node, FOAF.vidID, vid_id))
                    
                    if len(data[i].split("\t")) > 1:
                        uploader = Literal(data[i].split("\t")[1])
                        age = Literal(data[i].split("\t")[2])
                        category = Literal(data[i].split("\t")[3])
                        length = Literal(data[i].split("\t")[4])
                        views = Literal(data[i].split("\t")[5])
                        rate = Literal(data[i].split("\t")[6])
                        ratings = Literal(data[i].split("\t")[7])
                        comments = Literal(data[i].split("\t")[8])
                        
                        g.add((curr_node, FOAF.uploader, uploader))
                        g.add((curr_node, FOAF.age, age))
                        g.add((curr_node, FOAF.category, category))
                        g.add((curr_node, FOAF.length, length))
                        g.add((curr_node, FOAF.views, views))
                        g.add((curr_node, FOAF.rate, rate))
                        g.add((curr_node, FOAF.ratings, ratings))
                        g.add((curr_node, FOAF.comments, comments))
                    
                for i in range(len(data)):
                    related_vids = [data[i].split("\t")[j] for j in range(9, len(data[i].split("\t")))]
                    for j in range(len(related_vids)):
                        if related_vids[j] in videos:
                            g.add((curr_node, FOAF.isRelatedTo, videos[related_vids[j]]))



##Open current file
#with open(path + "0.txt") as file:
#    data = file.readlines()
#
##For each row in the file, add the video to the dictionary
#for i in range(len(data)):
#    if data[i].split("\t")[0] not in videos:
#        videos[data[i].split("\t")[0]] = BNode()
#
#
#for i in range(len(data)):
#    curr_node = videos[data[i].split("\t")[0]]
#    vid_id = Literal(data[i].split("\t")[0])
#    uploader = Literal(data[i].split("\t")[1])
#    age = Literal(data[i].split("\t")[2])
#    category = Literal(data[i].split("\t")[3])
#    length = Literal(data[i].split("\t")[4])
#    views = Literal(data[i].split("\t")[5])
#    rate = Literal(data[i].split("\t")[6])
#    ratings = Literal(data[i].split("\t")[7])
#    comments = Literal(data[i].split("\t")[8])
#    
#    g.add((curr_node, FOAF.vidID, vid_id))
#    g.add((curr_node, FOAF.uploader, uploader))
#    g.add((curr_node, FOAF.age, age))
#    g.add((curr_node, FOAF.category, category))
#    g.add((curr_node, FOAF.length, length))
#    g.add((curr_node, FOAF.views, views))
#    g.add((curr_node, FOAF.rate, rate))
#    g.add((curr_node, FOAF.ratings, ratings))
#    g.add((curr_node, FOAF.comments, comments))
#    
#for i in range(len(data)):
#    related_vids = [data[i].split("\t")[j] for j in range(9, len(data[i].split("\t")))]
#    for j in range(len(related_vids)):
#        if related_vids[j] in videos:
#            g.add((curr_node, FOAF.isRelatedTo, videos[related_vids[j]]))

print("Number of nodes: ", len(g))

g.serialize("normal_crawl.xml", format = "xml")









