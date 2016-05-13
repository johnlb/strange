class geometryContainer():
	"""
	Holds a set of geometries and provides basic manipulations.

	Parameters
	----------
	_geometries : list of translatable gdspy geometry objects.
	"""

	@property
	def extent_left(self):
	    return self._extent_left

	@property
	def extent_right(self):
	    return self._extent_right

	@property
	def extent_top(self):
	    return self._extent_top
	
	@property
	def extent_bottom(self):
	    return self._extent_bottom
	

	def __init__(self, geometries, extents=None):
		self._geometries = geometries
		self._updateExtents(geometries)

		try:
			self._extent_top    = extents[0]
			self._extent_right  = extents[1]
			self._extent_bottom = extents[2]
			self._extent_left   = extents[3]
		except TypeError:
			# Figure it out your self...
# FINISH ME
			self._extent_top    = None
			self._extent_right  = None
			self._extent_bottom = None
			self._extent_left   = None

	def translate(self, delta):
		"""
		Moves all objects by delta := [dx, dy]

		Parameters
		----------
		delta : [dx, dy]
			List of two floats.
			dx: distance to move in x-direction
			dy: distance to move in y-direction

		Returns
		-------
		self : geometryContainer
		"""

		for geo in self._geometries:
			geo.translate(delta[0], delta[1])

		self._extent_left   += delta[0]
		self._extent_right  += delta[0]
		self._extent_top    += delta[1]
		self._extent_bottom += delta[1]

		return self

	def rotate(self, angle):
		"""
		TO DO
		"""

	def flip(self, axis):
		"""
		TO DO
		"""

	def printToCell(self, cell):
		"""
		Prints all geometries in this container to the gdspy cell given.

		Parameters
		----------
		cell : Cell
			A gdspy cell object

		Modifies
		--------
		cell

		Returns
		-------
		None.

		"""

		[cell.add(geo) for geo in self._geometries]
		return

	
	def _updateExtents(self, geometries):
		"""Updates the extents based on a new set of geometries"""
		