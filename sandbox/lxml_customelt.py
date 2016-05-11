# We can add fallback to ElementTree API if we want
# (if we only use compatible API elements)
#
# http://lxml.de/tutorial.html
from lxml import etree


## Make a custom element
class styleElt(etree.ElementBase):
	def getStyle():
		return None



## Do parsing
parser = etree.HTMLParser()
# parser = etree.XMLParser()
try: 
	tree = etree.parse("inputs/test.html", parser)
except etree.XMLSyntaxError, e:
	print(e.error_log)


## Elements are lists
head = tree.getroot()[0]
body = tree.getroot()[1]

