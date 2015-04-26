from xml.dom import minidom

xml_path = '/Users/young/LVM.xml'

xmldoc = minidom.parse(xml_path)
itemlist = xmldoc.getElementsByTagName('item')
print(len(itemlist))
print(itemlist[0].attributes['name'].value)
for s in itemlist:
    print(s.attributes['name'].value)