from core import core
from containers import geometryContainer


import ast

import numpy
import gdspy
import tinycss

from lxml import etree
import cssselect



class artist():
	"""
	This is the object responsible for drawing a layout from a parsed html document.

	Ex:
	---
	artist = strange.artist()
	artist.drawGDS(htmlDoc)
	"""

	def __init__(self, units, precision):
		self.unitsSI = {
			'Y': 1e24,	# yotta
			'Z': 1e21,	# zetta
			'E': 1e18,	# exa
			'P': 1e15,	# peta
			'T': 1e12,	# tera
			'G': 1e9,	# giga
			'M': 1e6,	# mega
			'K': 1e3,	# kilo
			'c': 1e-2, 	# centi
			'm': 1e-3,	# milli
			'u': 1e-6,	# micro
			'n': 1e-9,	# nano
			'p': 1e-12,	# pico
			'f': 1e-15,	# femto
			'a': 1e-18,	# atto
			'z': 1e-21,	# zepto
			'y': 1e-24	# yocto
		}

		self.units = units
		self.precision = precision

		self.core = core()


	def drawGDS(self, htmlDoc):
		"""
		Draw me a layout, in GDS form.

		Parameters:
		-----------

		htmlDoc : etree.ElementTree
			The parsed html document to draw.

		Returns:
		--------
		out : gdspy.Cell
			A cell or list of gds cells containing the final layout.
		"""

		## HTML document
		htmlHead = htmlDoc.getroot()[0]
		htmlBody = htmlDoc.getroot()[1]

		## CSS parser
		cssparser = tinycss.make_parser()





		#### 1. Parse Techfile ####
		# NOTE: if multiple techfiles given, only 1st one is processed.
		techElt = htmlHead.cssselect('tech')
		if len(techElt) != 1:
			raise("FATAL: Exactly 1 techfile must be specified in the document's header.")
			return
		if 'file' not in techElt[0].attrib:
			raise("FATAL: No 'file' attribute of <tech> element given.")
			return

		techFileName = techElt[0].attrib['file']
		[defaultAttribs, deviceMap] = self._parseTechFile(techFileName)



		#### 2. Cascade & Parse Stylesheets ####
		# NOTE: stylesheets included in body are ignored
		ssElements = htmlHead.cssselect('link, [rel="stylesheet"], [href]')
		ssFileNames = [x.attrib['href'] for x in ssElements]
		styleMap = self._parseStylesheets(ssFileNames, htmlBody)


		#### 3. Build Geometries via Tree Traversal ####
		## geo : a mixed list of geometry objects and geometry containers.
		## location : the starting location of next object to print.
		geo = []
		location = [0, 0]
	## MAKE THIS A PROPER TRAVERSAL ##
		for elt in htmlBody:
			thisAttrib = elt.attrib
	
			## Collect any simple CSS styles
			## that apply to this element.
			try:
				thisTagStyle = styleMap[0][elt.tag]
			except:
				thisTagStyle = {}
			try:
				thisIdStyle = styleMap[1][thisAttrib['id']]
			except:
				thisIdStyle = {}
			try:
				thisClassStyle = styleMap[2][thisAttrib['class']]
			except:
				thisClassStyle = {}

			## Parse inline style
			inlineCSS = ''
			if 'style' in thisAttrib:
				inlineCSS = thisAttrib['style']
			thisStyle = cssparser.parse_stylesheet('this {' + inlineCSS + '}')
			thisStyle = self._declaration2dict(thisStyle.rules[0].declarations)


			# Combine everything in priority order into one set of
			# final parameters to draw with.
			combinedParams = self._combineParams([ defaultAttribs[elt.tag],
												   thisAttrib,
												   thisTagStyle,
												   thisClassStyle,
												   thisIdStyle,
												   thisStyle ])
			
			## account for left spacing
			location += [ combinedParams['padding-left'] +
						  combinedParams['margin-left']  +
						  combinedParams['border-width'] ,
						  0 ]

	## Make core into Class ##
			## Print geometries
			if elt.tag in self.deviceMap:
				thisDevice = self.deviceMap[elt.tag](**combinedParams)
				thisDevice.translate(location)
				geo += thisDevice


			# Increment location
			# TO DO: add <br> feature
			location += [ combinedParams['padding-right'] +
						  combinedParams['margin-right']  +
						  combinedParams['border-width'] ,
						  0 ]



	def _parseTechFile(self, fileName):
		"""
		Reads in a css techfile and builds necessary device map & default styles.

		Parameters
		----------
		fileName : string
			location of techfile

		Returns
		-------
		out : [defaultAttribs, deviceMap]
			List of two dictionaries. First describing default attributes,
			second linking tag names to the function meant to build them.
		"""

		cssparser = tinycss.make_parser()
		stylesheet = cssparser.parse_stylesheet_file(fileName)

		## Never modifying globals, just using to link text names to objects
		globs = globals()

		deviceMap = {}
		defaultAttribs = {}

		for rule in stylesheet.rules:
			# skip at rules
			if rule.at_keyword != None:
				continue



			# Grab the tag and declarations
			thisTag  = rule.selector[0]
			thisDecl = self._declaration2dict(rule.declarations)

			# In the declarations, we require a 'libname' and 'devname'
			try:
				thisLib = thisDecl['libname']
				thisDev = thisDecl['devname']
			except:
				raise Exception( "FATAL: techfile is malformed at line "
								 + str(rule.line) )

			# Use these properties to map the tag to a builder function
			deviceMap[thisTag.value] = getattr(globs[thisLib],thisDev)
			thisDecl.pop('libname')
			thisDecl.pop('devname')


			# Deal with the other declarations
			defaultAttribs[thisTag.value] = thisDecl

		return [defaultAttribs, deviceMap]




	def _parseStylesheets(self, ssFileNames, htmlBody):
		"""
		Reads in all stylesheets included in ssFileNames and parses them,
		in the order they appear (lowest index -> highest index)

		Parameters
		----------
		ssFileNames : [ strings ]
			List of file names.
		htmlBody : lxml.etree.Element
			Root element of the body.

		Modifies
		--------
		htmlBody
			Some of the more complex selectors can't be stored as a simple lookup,
			so these values are added to the inline "style" attribute of the
			appropriate tags.

		Returns
		-------
		out : [ dictionary ] * 3
			List of three dictionaries: [tagLookup idLookup classLookup]
			Each is a lookup table for its respective selector type and
			is of the form:
				{ 'name' : {dictionary} }, 	where the linked dictionaries
											contain that selector's parsed
											declarations.
		"""

		params = [self._parseStylesheet(fileName, htmlBody) for fileName in ssFileNames]

		tagParams = []
		idParams  = []
		classParams = []
		for p in params:
			tagParams 	+= [p[0]]
			idParams 	+= [p[1]]
			classParams += [p[2]]

		return [ self._combineParams(tagParams), 
				 self._combineParams(idParams),
				 self._combineParams(classParams) ]


	def _parseStylesheet(self, fileName, htmlBody):
		"""
		Reads in a stylesheet and parses it.

		Parameters
		----------
		ssFileNames : string
			File name to parse.
		htmlBody : lxml.etree.Element
			Root element of the body.

		Modifies
		--------
		htmlBody
			Some of the more complex selectors can't be stored as a simple lookup,
			so these values are added to the inline "style" attribute of the
			appropriate tags.

		Returns
		-------
		out : [ dictionary ] * 3
			List of three dictionaries: [tagLookup idLookup classLookup]
			Each is a lookup table for its respective selector type and
			is of the form:
				{ 'name' : {dictionary} }, 	where the linked dictionaries
											contain that selector's parsed
											declarations.
		"""

		cssparser = tinycss.make_parser()
		stylesheet = cssparser.parse_stylesheet_file(fileName)

		out = [{}, {}, {}]

		for rule in stylesheet.rules:
			# Skip at keywords
			if rule.at_keyword != None:
				continue

			thisDecl = self._declaration2dict(rule.declarations)

			## Decode selector types
			parsedSelectors = cssselect.parse(rule.selector.as_css())
			for i, thisSel in enumerate(parsedSelectors):
				
				## Do the easy selectors as a dictionary
				if sum(thisSel.specificity()) < 2:
					if hasattr(thisSel.parsed_tree, 'id'):
						# We have a single ID selector
						out[1][thisSel.parsed_tree.id] = thisDecl
						continue
					elif hasattr(thisSel.parsed_tree, 'class_name'):
						# We have a single CLASS selector
						out[2][thisSel.parsed_tree.class_name] = thisDecl
						continue
					elif hasattr(thisSel.parsed_tree, 'element'):
						# We have a single TAG selector
						out[0][thisSel.parsed_tree.element] = thisDecl
						continue


				## Do the hard selectors as in-line style
				for elt in htmlBody.cssselect(thisSel):
					declStr = self._decl2str(rule.declarations)
					try:
						elt.attrib['style'] += "; " + declStr
					except:
						elt.attrib['style'] = declStr

		return out


	def _decl2str(self, declarations):
		"""
		Converts a list of declarations to a single string.

		Parameters
		----------
		declarations : list
			list of tinycss declarations

		Returns
		-------
		out : string
		"""
		out = ''
		for thisDecl in declarations:
			valueStr = ''.join([x.as_css() for x in thisDecl.value])
			out += thisDecl.name + ':' + valueStr + '; '

		return out


	def _declaration2dict(self, declarations):
		"""
		Converts a list of declarations (from a tinycss object) into a dictionary

		Parameters
		----------
		declarations : list
			list of tinycss declarations

		Returns
		-------
		out : dictionary
			dictionary of the form "property:value," with all values parsed into
			base gds units.
		"""

		out = {}
		for decl in declarations:
			thisProp  = self._parseProp(decl.name, decl.value)

			# Deal with shorthand properties
			for name in thisProp.keys():
				out[name] = thisProp[name]

		return out



	def _parseProp(self, name, value):
		"""
		Checks for shorthand names and splits them up into their base names,
		then parses the values appropriately into a dictionary.

		Parameters
		----------
		name : string
			the name.
		value : [  ]
			# of values assigned to the name

		Returns
		-------
		out : dictionary
			Dictionary of name:value pairs.
		"""

		simple_prefixes = {
			'margin',
			'padding'
		}



		## Strip whitepace space tokens and parse any possible values
		parsedVals = []
		for x in value:
			if x.type != 'S':
				parsedVals += [self._parseValue(x)]
		valueLen = len(parsedVals)


		if name in simple_prefixes:
			if valueLen == 1:
				return { 
					name+'-top' 	:	parsedVals[0],
					name+'-right'	:	parsedVals[0],
					name+'-bottom' 	: 	parsedVals[0],
					name+'-left' 	: 	parsedVals[0]
				}
			elif valueLen == 4:
				return { 
					name+'-top' 	:	parsedVals[0],
					name+'-right'	:	parsedVals[1],
					name+'-bottom' 	: 	parsedVals[2],
					name+'-left' 	: 	parsedVals[3]
				}
			else:
				raise Exception(
					"""Incorrect # of values supplied to a shorthand CSS expression.
					Only 1-value and 4-value syntaxes are supported.
					(On line """ + str(value[0].line) + 
					", column "  + str(value[0].column) + ")"
					)


		elif name == 'border':
			suffixes = ['-width', '-style']
			names = [''.join(x) for x in zip(['border']*valueLen, suffixes)]
			return {x:y for x,y in zip(names,parsedVals)}


		else:
			if valueLen != 1:
				raise Exception(
					"""Incorrect # of values supplied to a CSS expression.
					(On line """ + str(value[0].line) +
					", column "  + str(value[0].column) + ")"
					)
			return {name:parsedVals[0]}




	def _parseValue(self, value):
		"""
		Converts tinycss Token into appropriate Pythonic value

		Parameters
		----------
		value : tinycss Token
			value being assigned to a property

		Returns
		-------
		out : string | boolean | float (depending on Token's value)
			Appropriate Pythonic datatype, with unit conversion.
			Percentages are returned as strings of the form: "90%"
			(since this function cannot know about the value's default)
		"""

		if value.type == 'DIMENSION':
			if value.unit == 'px':
				return value.value * (self.precision/self.units)
			else:
				return value.value * self.unitsSI[value.unit[0]]/self.units



		elif value.type == 'INTEGER' or value.type == 'NUMBER':
			return value.value



		elif value.type == 'PERCENTAGE':
			return str(value.value) + '%'



		elif value.type == 'STRING':
			if value.value.lower() == 'true':
				return True
			elif value.value.lower() == 'false':
				return False
			else:
				return value.value



		elif value.type == 'IDENT':
			if value.value.lower() == 'true':
				return True
			elif value.value.lower() == 'false':
				return False
			else:
				return value.value



		else:
			raise Exception("Illegal value (" + str(value.value) + 
							") in css at line " + str(value.line) +
				  			", column " + str(value.column) )





	def _combineParams(self, paramsList):
		"""
		This implements the "cascading" part of "Cascading Style Sheets".
		It combines each set of parameters in paramsList in order from lowest
		index to highest.

		This way, the last parameter set in the list will override any common 
		values it might have with other parameter sets.

		Parameters
		----------
		paramsList : [ dictionaries ]
			list of dictionaries to be combined.

		Returns
		-------
		out : dictionary
			single, combined dictionary.
		"""

		out = {}
		for pset in paramsList:
			for key in pset.keys():
				out[key] = pset[key]

		return out



	def _sanitizeDistance(self, dist):
		return int(dist*self.units/self.precision)*self.precision/self.units



	def _sanitizeDistanceDict(self, distDict):
		for x in distDict.iterkeys():
			try:
				distDict[x] = self._sanitizeDistance(distDict[x])
			except:
				continue

		return distDict
