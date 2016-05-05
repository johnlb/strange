"""Drawing functions for basic, process agnostic devices.

Process-specific features should be added on top of these devices.
"""

import gdspy
from . import stdStackup
import math


# def contactHelper( bbH, bbW, COsize=0.04, COspace=0.03, COoffsetY=0, COoffsetX=0 ) :
# 	"""
# 	Draws vertical column of contacts centered within an imaginary box
# 	of height bbH and width bbW.

# 	The origin of the result is at the upper left corner of the box.

# 	Returns: list of gdspy geometry objects, following the standard layer stackup.
# 	"""

# 	numCO 		= math.floor((bbH - COspace)/(COspace + COsize))
# 	COinsetY 	= (bbH - COsize - (numCO-1)*(COspace + COsize))/2.0 - COoffsetY;
# 	COposX 		= -(RXextLeft/2.0 + COsize/2.0 + COoffsetX)	# from top left of contact
	
# 	contacts = []
# 	for ii in range(numCO):
# 		thisY = -COinsetY - ii*(COsize+COspace)	
# 		contacts = contacts + [gdspy.Rectangle(	(COposX,thisY),
# 												(COposX+COsize,thisY-COsize),
# 												stdStackup.CO )]




def fet(	l, w,
			COsize=0.04, COspace=0.03, COoffsetY=0, COoffsetX=0,
			COexistsLeft=True, 	COexistsRight=True,
			POextTop=0.1, 		POextBot=0.1,
			RXextLeft=0.1, 		RXextRight=0.1
		) :

	"""
	Responsible for drawing a fundamental FET device.

	Meant to be process agnostic, this function returns only 
	active, poly, and contact geometries. Any process-specific
	requirements should be built on top of this geometry.

	Origin of returned geometries will be the top left intersection of the gate
	and the active area. This ensures geometries stay on-grid after being built.

	Returns: list of gdspy geometry objects, following the standard layer stackup.
	"""

	if l<=0:
		raise MinLengthError("Can't have negative legnth device.")
	if w<=0:
		raise MinwidthError("Can't have negative width device.")



	# Draw gate
	gate = gdspy.Rectangle((0,POextTop), (l,-(w+POextBot)), stdStackup.PO);

	# Draw RX
	active = gdspy.Rectangle((-RXextLeft,0), (l+RXextRight,-w), stdStackup.RX);

	# Draw CO
	numCO 		= math.floor((w - COspace)/(COspace + COsize))
	COinsetY 	= (w - COsize - (numCO-1)*(COspace + COsize))/2.0;
	COposXleft 	= -(RXextLeft/2.0 + COsize/2.0 + COoffsetX)	# from bot left of contact
	COposXright =   RXextRight/2.0 - COsize/2.0 + COoffsetX + l
	contactsLeft = []
	contactsRight = []
	for ii in range(numCO):
		thisY = -w + COinsetY + ii*(COsize+COspace)
		
		contactsLeft = contactsLeft + [gdspy.Rectangle(	(COposXleft,thisY),
														(COposXleft+COsize,thisY+COsize),
														stdStackup.CO )]
		contactsRight = contactsRight + [gdspy.Rectangle( (COposXright,thisY),
														 (COposXright+COsize,thisY+COsize),
														 stdStackup.CO )]

	return [gate, active] + contactsLeft + contactsRight



def res_poly ( l, w, POext=0.1, COsize=0.04, COspace=0.03 ) :
	"""
	Responsible for drawing a fundamental poly resistor.

	This function draws poly and contact layers for a poly resistor.

	Origin of returned geometries will be the top left corner of the resistor.

	Returns: list of gdspy geometry objects, following the standard layer stackup.
	"""

	# Draw PO
	poly = gdspy.Rectangle((-POext,0), (l+POext,-w), stdStackup.PO);

	# Draw CO
	numCO 		= math.floor((w - COspace)/(COspace + COsize))
	COinsetY 	= (w - COsize - (numCO-1)*(COspace + COsize))/2.0;
	COposXleft 	= -COsize	# from bot left of contact
	COposXright = l
	contactsLeft = []
	contactsRight = []
	for ii in range(numCO):
		thisY = -w + COinsetY + ii*(COsize+COspace)
		
		contactsLeft = contactsLeft + [gdspy.Rectangle(	(COposXleft,thisY),
														(COposXleft+COsize,thisY+COsize),
														stdStackup.CO )]
		contactsRight = contactsRight + [gdspy.Rectangle( (COposXright,thisY),
														 (COposXright+COsize,thisY+COsize),
														 stdStackup.CO )]

	return [poly] + contactsLeft + contactsRight