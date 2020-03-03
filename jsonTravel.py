#random walk on OSM

import json
import random
import time

count=0
way_data = [];
nodeTravled=[];

# show the node info
def nodeInfo(id):
    node_file = open("../files/map.osm_node.json")
    for line in node_file:
        node = json.loads(line)
        if node["id"] == id:
            print(count, " | Now at node: " + node["id"] + " | (lat,lon): (" + node["lat"] + "," + node["lon"] + ")")

            if "tag" in node.keys():
                print("Node info: ", node["tag"])
    node_file.close()

def wayInfo(id):
    for way in way_data:
        if way["id"]==id:
            print(" Traveling through the way: "+way["id"])

            if "tag" in way.keys():
                print(" Way info: ",way["tag"])

#change ways to python dict
way_file = open("../files/map.osm_way.json")
for line in way_file:
    way = json.loads(line)
    way_data.append(way)
way_file.close()


startWay = way_data[random.randint(0,len(way_data)-1)]
currentNode = startWay["nd"][random.randint(0,len(startWay["nd"])-1)]["ref"]

nodeInfo(currentNode)
nodeTravled.append(currentNode)
count=count+1

while count<100:
    nextCand=[]
    end=0

    #find all next node we can go
    for way in way_data:
        flag = 0
        for node in way["nd"]:
            if node["ref"] == currentNode:
                flag=1
                break

        if flag==1:
            for node in way["nd"]:
                if node["ref"]!=currentNode and (node["ref"] not in nodeTravled):
                    nextCand.append((way["id"],node["ref"]))
                    end=1

    if end==0:
        print("End of the road !!!!!!")
        break

    #randomly choose a random node to move to
    pair = nextCand[random.randint(0,len(nextCand)-1)]
    wayInfo(pair[0])
    nodeInfo(pair[1])
    nodeTravled.append(pair[1])

    count=count+1
    currentNode=pair[1]








