# We can add fallback to ElementTree API if we want
# (if we only use compatible API elements)
#
# http://lxml.de/tutorial.html
from lxml import etree



## Do parsing
parser = etree.HTMLParser()
# parser = etree.XMLParser()
try: 
	tree = etree.parse("inputs/test.html", parser)
except etree.XMLSyntaxError, e:
	print(e.error_log)


## Elements are lists
head = tree.getroot()[0]
print(head)
body = tree.getroot()[1]
print(body)

M1 = body[1]
print(M1)

## Elements contain text
print(body[0].text)

## Attributes are dicts
print(M1.tag)
print(M1.attrib)


## Using <io> tag to define interconnect
print(M1[0].tag)
print(M1[0].attrib)