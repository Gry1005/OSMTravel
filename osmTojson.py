# -*- coding: utf-8 -*-
import json
from lxml import etree
import xmltodict

def iter_element(file_parsed, file_length, node_write,way_write,relation_write):
    current_line = 0
    try:
        for event, element in file_parsed:
            current_line += 1
            print(current_line/float(file_length))
            elem_data = etree.tostring(element)
            elem_dict = xmltodict.parse(elem_data, attr_prefix="", cdata_key="")
            if (element.tag == "node"):
                elem_jsonStr = json.dumps(elem_dict["node"])
                node_write.write(elem_jsonStr + "\n")
            if (element.tag == "way"):
                elem_jsonStr = json.dumps(elem_dict["way"])
                way_write.write(elem_jsonStr + "\n")
            if (element.tag == "relation"):
                elem_jsonStr = json.dumps(elem_dict["relation"])
                relation_write.write(elem_jsonStr + "\n")

            # 每次读取之后进行一次清空
            element.clear()
            while element.getprevious() is not None:
                del element.getparent()[0]
    except:
        pass

if __name__ == '__main__':
    osmfile = r'../files/map.osm'

    file_length = -1
    for file_length, line in enumerate(open(osmfile, encoding='UTF-8')):
        pass
    file_length += 1
    print("length of the file:\t" + str(file_length))

    file_node = open(osmfile+"_node.json","w+")
    file_way = open(osmfile + "_way.json", "w+")
    file_relation = open(osmfile + "_relation.json", "w+")

    file_parsed = etree.iterparse(osmfile, tag=["node","way","relation"])
    iter_element(file_parsed, file_length, file_node,file_way,file_relation)

    file_node.close()
    file_way.close()
    file_relation.close()

