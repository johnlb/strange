class geometryContainer():
	"""
	Holds a set of geometries and provides basic manipulations.

	Parameters
	----------
	_geometries : list of translatable gdspy geometry objects.
	"""

	def __init__(self, geometries):
		self._geometries = geometries

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

		for geo in self._geometries:
			cell.add(geo)

		return