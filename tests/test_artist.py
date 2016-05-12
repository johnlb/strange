from context import strange
from strange.artist import artist

import numpy
import gdspy

import tinycss

from lxml import etree


## For testing only
from io import StringIO
import filecmp
import datetime
import monkeypatch
# import os


###################################################################################
# Useful Testing Devices
###################################################################################

def almost_equal(a,b,eps):
	"""Compare two lists, allowing for roundoff error."""
	# print([abs(x-y) for x,y in zip(a,b)])
	return all([abs(x-y)<eps for x,y in zip(a,b)])


class mock_datetime():
	"""A class to monkeypatch the datetime module"""
	def __init__(self):
		self.datetime = self._datetime()
	class _datetime():
		def __init__(self):
			pass
		def today(self):
			return datetime.datetime(2016,1,1,1,1,1,1)




###################################################################################
# Setup / Teardown
###################################################################################

def setup_function(function):
	function.thisArtist = artist(1e-6,5e-9)



###################################################################################
# Test Fixtures
###################################################################################


def test_combineParams():

	params = [
			{'a':'1', 'b':'1'},
			{'a':'2', 'c':'2'},
			{'a':'3', 'c':'3'}
		]

	result = {'a':'3', 'b':'1', 'c':'3'}

	assert( result == test_combineParams.thisArtist._combineParams(params) )



class baseTest():
	"""
	Inherited by all Test Classes.
	"""

	def setup(self):
		self.thisArtist = artist(1e-6,5e-9)
		self.parser = tinycss.make_parser()




class Test_parseValue(baseTest):


	def test_string_out(self):

		ss = self.parser.parse_stylesheet(	
				"""
				a { name:"value" }
				"""
			)
		value = ss.rules[0].declarations[0].value[0]
		assert( self.thisArtist._parseValue(value) == 'value' )



	def test_bool_out(self):

		ss = self.parser.parse_stylesheet(	
				"""
				a { name:true }
				"""
			)
		value = ss.rules[0].declarations[0].value[0]
		assert( self.thisArtist._parseValue(value) == True )



	def test_dimension_out(self):

		ss = self.parser.parse_stylesheet(	
				"""
				a { name:10nm }
				"""
			)
		value = ss.rules[0].declarations[0].value[0]
		assert( self.thisArtist._parseValue(value) == 0.01 )




class Test_parseProp(baseTest):


	def test_shorthand(self):

		ss = self.parser.parse_stylesheet(	
				"""
				a { margin:0px 1u 15nm 30nm }
				"""
			)
		value = ss.rules[0].declarations[0].value
		name  = ss.rules[0].declarations[0].name
		result = self.thisArtist._parseProp(name,value)

		expected = {
			'margin-top'	:0.,
			'margin-right'	:1.,
			'margin-bottom'	:0.015,
			'margin-left'	:0.030,
		}
		assert( almost_equal(result.values(), expected.values(), 1e-4) )




class Test_declaration2dict(baseTest):


	def test_shorthand(self):

		ss = self.parser.parse_stylesheet(	
				"""
				a { margin:1px 1u 15nm 30nm; padding-top:1u }
				"""
			)
		decl = ss.rules[0].declarations
		result = self.thisArtist._declaration2dict(decl)
		
		expected = {
			'margin-top'	:0.005,
			'margin-right'	:1.,
			'margin-bottom'	:0.015,
			'margin-left'	:0.030,
			'padding-top' 	:1.
		}
		result_list   = [result[x] for x in result.keys()]
		expected_list = [expected[x] for x in result.keys()]
		assert( almost_equal(result_list, expected_list, 1e-4) )





class Test_decl2str(baseTest):


	def test_shorthand_with_newline(self):

		ss = self.parser.parse_stylesheet(	
				"""
				a { 
					margin:1px 1u 15nm 30nm;
					padding-top:1u;
				}
				"""
			)
		decl = ss.rules[0].declarations
		result = self.thisArtist._decl2str(decl)
		
		expected = "margin:1px 1u 15nm 30nm; padding-top:1u; "

		assert( result == expected )



class Test_parseStylesheet(baseTest):

	def test_simple_selectors(self):

		parser = etree.HTMLParser()
		htmlDoc = etree.parse( StringIO(
				u"""
				<!DOCTYPE netlist>
				<html>
				<head></head>
				<body></body>
				</html>
				"""), parser)
		htmlBody = htmlDoc.getroot()[1]

		result = self.thisArtist._parseStylesheet(
					'./tests/inputs/_parseStylesheet-simple_selectors.css',
					htmlBody
				)
		
		expected = [
			{'a': {'tag':	1}},
			{'a': {'id':	2}},
			{'a': {'class':	3}}
		]
		assert( result == expected )



class Test_parseStylesheets(baseTest):

	def test_simple_selectors(self):

		ssNames = ['./tests/inputs/_parseStylesheet-simple_selectors.css']

		parser = etree.HTMLParser()
		htmlDoc = etree.parse( StringIO(
			u"""
			<!DOCTYPE netlist>
			<html>
			<head>	
			<link rel="stylesheet" href="./tests/inputs/_parseStylesheet-simple_selectors.css">
			</head>
			<body></body>
			</html>
			"""), parser)
		htmlBody = htmlDoc.getroot()[1]

		result = self.thisArtist._parseStylesheets(ssNames, htmlBody)
		
		expected = [
			{'a': {'tag':	1}},
			{'a': {'id':	2}},
			{'a': {'class':	3}}
		]
		assert( result == expected )


class Test_parseTechFile(baseTest):

	def test_basic(self):

		techfileName =	'./tests/inputs/_parseTechFile-test_basic.css'
		result = self.thisArtist._parseTechFile(techfileName)

		expected = [
			{ 
				'fet': {'cosize':0.04},
				'res_poly': {'padding-bottom':0.11}
			},

			{	
				## result is an unbound method.
				## AFAIK, this is best I can do...
				'fet': result[1]['fet'],
				'res_poly': result[1]['res_poly']
			} 
		]

		# print(result[1])
		assert(expected == result)





class Test_core(baseTest):

	def setup_method(self,method):

		# Need to force the sys time to be consistent
		# b/c gds_print prints time-stamp into file.
		thisDatetime = mock_datetime()
		gdspy.datetime = thisDatetime




	def test_fet(self):

		# test fet
		fet_cell = gdspy.Cell('fet')
		fetGEO = self.thisArtist.core.fet(0.040, 0.440)

		fetGEO.printToCell(fet_cell)

		# print in a special way that doesn't add timestamp
		ptr = gdspy.GdsPrint('./tests/outputs/core_fet-test_basic.gds',
							unit=1.0e-6, precision=5.0e-9)
		ptr.write_cell(fet_cell)
		ptr.close()

		print(filecmp.cmp(
					'./tests/outputs/core_fet-test_basic.gds',
					'./tests/outputs/core_fet-test_basic-truth.gds'
				))
		assert( filecmp.cmp(
					'./tests/outputs/core_fet-test_basic.gds',
					'./tests/outputs/core_fet-test_basic-truth.gds'
				) )


	def test_res_poly(self):

		# test fet
		res_poly_cell = gdspy.Cell('res_poly')
		fetGEO = self.thisArtist.core.res_poly(2, 1)
		fetGEO.printToCell(res_poly_cell)

		# print in a special way that doesn't add timestamp
		ptr = gdspy.GdsPrint('./tests/outputs/core_res_poly-test_basic.gds',
							unit=1.0e-6, precision=5.0e-9)
		ptr.write_cell(res_poly_cell)
		ptr.close()

		assert( filecmp.cmp(
					'./tests/outputs/core_res_poly-test_basic.gds',
					'./tests/outputs/core_res_poly-test_basic-truth.gds'
				) )

