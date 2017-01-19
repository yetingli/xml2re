#!/usr/bin/python
# -*- coding: UTF-8 -*-
import xml.dom.minidom
import re
import xml.etree.ElementTree as ET
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )


def fixed_writexml(self, writer, indent="", addindent="", newl=""):
    writer.write(indent + "<" + self.tagName)
    attrs = self._get_attributes()
    a_names = attrs.keys()
    a_names.sort()

    for a_name in a_names:
        writer.write(" %s=\"" % a_name)
        xml.dom.minidom._write_data(writer, attrs[a_name].value)
        writer.write("\"")
    if self.childNodes:
        if len(self.childNodes) == 1 \
                and self.childNodes[0].nodeType == xml.dom.minidom.Node.TEXT_NODE:
            writer.write(">")
            self.childNodes[0].writexml(writer, "", "", "")
            writer.write("</%s>%s" % (self.tagName, newl))
            return
        writer.write(">%s" % (newl))
        for node in self.childNodes:
            if node.nodeType is not xml.dom.minidom.Node.TEXT_NODE:
                node.writexml(writer, indent + addindent, addindent, newl)
        writer.write("%s</%s>%s" % (indent, self.tagName, newl))
    else:
        writer.write("/>%s" % (newl))

xml.dom.minidom.Element.writexml = fixed_writexml
class XML:
    #init
    def __init__(self,file_path):
        self.file = file_path
        self.dom = xml.dom.minidom.parse(self.file)  # open xml file
        self.root = self.dom.documentElement  # get xml document object
        self.xmlstring =  ''
        self.rootstring = ''
        self.leafList = []
        self.dict={}
        self.result = ''
        self.get_root()
        self.getXMLStr()

    #create dom
    def create_dom(self):
        self.dom = xml.dom.minidom.parseString(self.xml)
        self.root = self.dom.documentElement  # get xml document object

    #get xml string
    def getXMLStr(self):
        self.xmlstring = self.root.toprettyxml()
        return self.root.toprettyxml()

    #delete unless information
    def delete_useless_inf(self):
        strs = self.getXMLStr()
        strList = strs.split('\n')
        newList = []
        for li in strList:
            nums = re.findall(r'>.*?<', li)
            if len(nums) > 0:
                rs = re.subn(nums[0][1:-1], '', li)
                li = rs[0]
            lis = li.split(' ')
            if len(lis) > 1:
                li = lis[0] + '>'
            #print li
        newList.append(li)

    # rename with inter
    def rename_tags(self):
        leaves = list(set(self.leafList))
        self.dict = {}
        i = 1
        for leaf in leaves:
            if leaf not in self.dict.keys():
                self.dict[leaf] = str(i)
                i += 1
        return self.dict

    #get root string
    def get_root(self):
        strs = self.getXMLStr()
        rt = ET.fromstring(strs)
        self.rootstring = rt.tag

    #get re from xml
    def get_re(self,ETroot,parent):
        if len(ETroot)==0:
            return str(self.dict[parent+'.'+ETroot.tag])
        elif len(ETroot)==1:
            parent += '.' + ETroot.tag
            temp = self.get_re(ETroot[0],parent)
            return '('+temp +')'
        else:
            sum = '('
            for child in ETroot:
                temp = self.get_re(child,parent+'.' + ETroot.tag)
                sum +=temp +','
            sum = sum[:-1]
            sum +=')'
            return sum

    #get leaves
    def traversal_nodes(self,ETroot,level,parent):
        if len(ETroot)==0:
            self.leafList.append(parent+'.'+ETroot.tag)
        elif len(ETroot)==1:
            level +=1
            parent +='.'+ETroot.tag
            self.traversal_nodes(ETroot[0],level,parent)
        else:
            for child in ETroot:
                self.traversal_nodes(child,level+1,parent+'.' + ETroot.tag)
if __name__=="__main__":
    xml_file = r'imsmanifest.xml'
    xmls = XML(xml_file)
    #print xmls.getXMLStr()
    #print xmls.xmlstring
    #print xmls.rootstring
    strs = xmls.getXMLStr()
    ETroot = ET.fromstring(strs)
    xmls.traversal_nodes(ETroot,1,'')
    #print xmls.leafList
    print xmls.rename_tags()
    regex = xmls.get_re(ETroot,'')
    print regex









