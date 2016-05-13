# import artist
from context import strange
from strange.artist import artist
from strange.artist import core

import numpy
import gdspy




core = core()

# test fet
fet_cell = gdspy.Cell('fet')
fetGEO = core.fet(0.040, 0.440)

# try copying the gate -- tests translation as well.
# fetGEO += [ gdspy.copy(fetGEO[0],"+x",2) ]
# for ii in fetGEO:
# 	fet_cell.add(ii)
fetGEO.printToCell(fet_cell)


# test res_poly
res_poly_cell = gdspy.Cell('res_poly')
fetGEO = core.res_poly(2, 1)
# for ii in fetGEO:
# 	res_poly_cell.add(ii)
fetGEO.printToCell(res_poly_cell)


# Output GDS
gdspy.gds_print('./outputs/visualTest_core.gds', unit=1.0e-6, precision=5.0e-9)


# Look at the results
gdspy.LayoutViewer()