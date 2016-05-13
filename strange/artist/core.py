"""
Drawing functions for basic, process agnostic devices.

Process-specific features should be added on top of these devices.
"""

import gdspy
import math

from . import stdStackup
from containers import geometryContainer

# def contactHelper( bbH, bbW, COsize=0.04, COspace=0.03, COoffsetY=0, COoffsetX=0 ) :
# 	"""
# 	Draws vertical column of contacts centered within an imaginary box
# 	of height bbH and width bbW.

# 	The origin of the result is at the upper left corner of the box.

# 	Returns: list of gdspy geometry objects, following the standard layer stackup.
# 	"""

# 	numCO 		= math.floor((bbH - COspace)/(COspace + COsize))
# 	COinsetY 	= (bbH - COsize - (numCO-1)*(COspace + COsize))/2.0 - COoffsetY;
# 	COposX 		= -(rxextleft/2.0 + COsize/2.0 + COoffsetX)	# from top left of contact
	
# 	contacts = []
# 	for ii in range(numCO):
# 		thisY = -COinsetY - ii*(COsize+COspace)	
# 		contacts = contacts + [gdspy.Rectangle(	(COposX,thisY),
# 												(COposX+COsize,thisY-COsize),
# 												stdStackup.CO )]


class core():

	def fet(	self, 
				l, w,
				COsize=0.04, COspace=0.03, COoffsetY=0, COoffsetX=0,
				COexistsLeft=True, 	COexistsRight=True,
				POextTop=0.1, 		POextBot=0.1,
				rxextleft=0.1, 		rxextright=0.1,
				**kwargs
			) :

		"""
		Responsible for drawing a fundamental FET device.

		Meant to be process agnostic, this function returns only 
		active, poly, and contact geometries. Any process-specific
		requirements should be built on top of this geometry.

		Origin of returned geometries will be the top left intersection of the gate
		and the active area. This ensures geometries stay on-grid after being built.

		**kwargs is ignored. It is included to allow for passing of a style dictionary
		with more entries than those required by this function.

		Returns: geometryContainer
			A geometryContainer with all gdspy geometries for this device.
		"""

		if l<=0:
			raise Exception("FATAL: Can't have negative legnth device.")
		if w<=0:
			raise Exception("FATAL: Can't have negative width device.")


		# Draw gate
		gate = gdspy.Rectangle((0,POextTop), (l,-(w+POextBot)), stdStackup.PO);

		# Draw RX
		active = gdspy.Rectangle((-rxextleft,0), (l+rxextright,-w), stdStackup.RX);

		# Draw CO
		numCO 		= int( math.floor((w - COspace)/(COspace + COsize)) )
		COinsetY 	= (w - COsize - (numCO-1)*(COspace + COsize))/2.0;
		COposXleft 	= -(rxextleft/2.0 + COsize/2.0 + COoffsetX)	# from bot left of contact
		COposXright =   rxextright/2.0 - COsize/2.0 + COoffsetX + l
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

		# Build Container
		geometeries = [gate, active] + contactsLeft + contactsRight
		extents = (+POextTop, l+rxextright, w+POextBot, -rxextleft)
		return geometryContainer(geometeries, extents)



	def res_poly ( self, l, w, POext=0.1, COsize=0.04, COspace=0.03, **kwargs ) :
		"""
		Responsible for drawing a fundamental poly resistor.

		This function draws poly and contact layers for a poly resistor. The length
		of the resistor is measured from the inside edges of the contacts.

		Origin of returned geometries will be the top left corner of the resistor
		boundary (inside edge of left contacts)

		**kwargs is ignored. It is included to allow for passing of a style dictionary
		with more entries than those required by this function.

		Returns: geometryContainer
			A geometryContainer with all gdspy geometries for this device.
		"""

		# Draw PO
		poly = gdspy.Rectangle((-POext,0), (l+POext,-w), stdStackup.PO);

		# Draw CO
		numCO 		= int( math.floor((w - COspace)/(COspace + COsize)) )
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

		# Build Container
		geometeries = [poly] + contactsLeft + contactsRight
		extents = (0., l+POext, w, -POext)
		return geometryContainer(geometeries, extents)
