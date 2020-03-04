#random walk on OSM 2.0
#memeory cost is very low; I/O operetions increases

import json
import random


count=0
nodeTravled=[];
way_route="../files/map.osm_way.json"
node_route="../files/map.osm_node.json"



# show the node info
def nodeInfo(id):
    node_file = open(node_route)
    for line in node_file:
        node = json.loads(line)
        if node["id"] == id:
            print(count, " | Now at node: " + node["id"] + " | (lat,lon): (" + node["lat"] + "," + node["lon"] + ")")

            if "tag" in node.keys():
                print("Node info: ", node["tag"])
    node_file.close()


def wayInfo(id):
    way_file = open(way_route)
    for line in way_file:
        way = json.loads(line)
        if way["id"] == id:
            print(" Traveling through the way: " + way["id"])

            if "tag" in way.keys():
                print(" Way info: ",way["tag"])
    way_file.close()


#random start, the first way need to be a highway instead of a building
high_way_list=[]

way_file=open(way_route)
for line in way_file:
   way = json.loads(line)
   if "tag" in way.keys():

       tag=way["tag"]

       if tag[0]['k']=="highway":
           high_way_list.append(way)
           if(len(high_way_list)>100):
               break


way_file.close()

#print("high_way_list: ",high_way_list)

startWay=high_way_list[random.randint(0,len(high_way_list)-1)]

currentNode=startWay["nd"][random.randint(0, len(startWay["nd"]) - 1)]["ref"]

nodeInfo(currentNode)
nodeTravled.append(currentNode)

count=count+1

while count<100:
    nextCand=[]
    end=0

    #find all next node we can go
    way_file = open(way_route)

    for line in way_file:
        way=json.loads(line)
        flag = 0
        for node in way["nd"]:
            if node["ref"] == currentNode:
                flag=1
                break

        if flag==1:
            for node in way["nd"]:
                if node["ref"]!=currentNode and (node["ref"] not in nodeTravled):
                    #Through which road to the next node
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

    way_file.close()








