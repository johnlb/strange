from context import strange

import numpy
import gdspy


from lxml import etree



## Do parsing
parser = etree.HTMLParser()
try: 
	document = etree.parse("./inputs/artist-test_css.html", parser)
except etree.XMLSyntaxError, e:
	print(e.error_log)


artist = strange.artist(1e-6, 1e-9)
cells = artist.drawGDS(document)


# Output GDS
gdspy.gds_print('./outputs/visualTest_artist.gds', unit=1.0e-6, precision=5.0e-9)


# Look at the results
gdspy.LayoutViewer(cells=cells)