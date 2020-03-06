#random walk on OSM 4.0
#memeory cost is very low; I/O operetions increases
#now can go back to an earlier node. Random walking based on a tree sturcture.
#the tree has been saved; less space complexity

import json
import random


count=0
nodeTravled=[]
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
            print("Traveling through the way: " + way["id"])

            if "tag" in way.keys():
                print("Way info: ",way["tag"])
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
nodeTravled.append([0,startWay["id"],currentNode])

count=count+1

nextCand=[]

while count<10:

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
                if node["ref"]!=currentNode:
                    isIn=0
                    for tri in nextCand:
                        if(node["ref"]==tri[2]):
                            isIn=1
                    for tri in nodeTravled:
                        if(node["ref"]==tri[2]):
                            isIn=1
                    #Through which road to the next node
                    if isIn==0:
                        nextCand.append([currentNode,way["id"],node["ref"]])

    if len(nextCand)==0:
        print("End of the road !!!!!!")
        break

    #randomly choose a random node to move to
    tri = nextCand[random.randint(0,len(nextCand)-1)]

    print("From node: "+tri[0])
    wayInfo(tri[1])
    nodeInfo(tri[2])

    nextCand.remove(tri)
    nodeTravled.append(tri)

    count=count+1
    currentNode=tri[2]

    way_file.close()

#print(nodeTravled)








