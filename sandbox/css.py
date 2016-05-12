import tinycss
import cssselect


# Create parser object. Can add extra features by overriding the class's methods...
parser = tinycss.make_parser();


# Import test stylesheet
stylesheet = parser.parse_stylesheet_file("./inputs/test.css");


# Let's look at it
print(stylesheet.rules)
print(stylesheet.errors)


# Accessing a specific parsed statement (the first "rule" in rules)
rule = stylesheet.rules[1]
print(rule.selector[0].value) 				# one of the selectors,
															# there can be many

print(rule.declarations[0].value[0].type) 	# the declaration,
															# there can be many

print(rule.declarations[0].value[0].value)	# its assigned value,
															# (not sure when there'd
															#  be more than one?)


ssRules = stylesheet.rules

# Try dealing with complex selectors
rule = ssRules[1]
sel = cssselect.parse(rule.selector.as_css())
print(sel)
print(dir(sel[0].parsed_tree))