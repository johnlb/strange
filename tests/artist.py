import sys
sys.path.insert(0, '../strange/')

import gdspy
# import artist
# from artist.core import fet
from artist import core as artist



# test fet
fet_cell = gdspy.Cell('fet')
fetGEO = artist.fet(0.040, 0.440)

# try copying the gate -- tests translation as well.
fetGEO += [ gdspy.copy(fetGEO[0],"+x",2) ]
for ii in fetGEO:
	fet_cell.add(ii)


# test res_poly
res_poly_cell = gdspy.Cell('res_poly')
fetGEO = artist.res_poly(2, 1)
for ii in fetGEO:
	res_poly_cell.add(ii)



# Output GDS
gdspy.gds_print('./outputs/artist_test.gds', unit=1.0e-6, precision=5.0e-9)


# Look at the results
gdspy.LayoutViewer()