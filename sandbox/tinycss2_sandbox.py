import tinycss2 as tinycss


# Create parser object. Can add extra features by overriding the class's methods...
with open('./inputs/test.css', 'r') as f:
	# Import test stylesheet
	rules, encoding = tinycss.parse_stylesheet_bytes( f.read(),
								skip_comments=True, skip_whitespace=True );

print(rules)
print(encoding)