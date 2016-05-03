import tinycss


# Create parser object. Can add extra features by overriding the class's methods...
parser = tinycss.make_parser();


# Import test stylesheet
stylesheet = parser.parse_stylesheet_file("./test.css");


# Let's look at it
print(stylesheet.rules)
print(stylesheet.errors)


# Accessing a specific parsed statement (the first "rule" in rules)
print(stylesheet.rules[0].selector[0].value) 				# one of the selectors,
															# there can be many

print(stylesheet.rules[0].declarations[0].value[0].type) 	# the declaration,
															# there can be many

print(stylesheet.rules[0].declarations[0].value[0].value)	# its assigned value,
															# (not sure when there'd
															#  be more than one?)