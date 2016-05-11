import AdvancedHTMLParser

document = AdvancedHTMLParser.AdvancedHTMLParser()

document.parseFile("inputs/test.html")


# We can use standard JS-style DOM interactions
print(document.getElementsByTagName("fet"))

# Not everything is the same, though.
# Ex: python doesn't use *.length -- need len(*)
print(len(document.getElementsByTagName("fet")))


M1 = document.getElementsByTagName("fet")[0]

# Attributes are dicts
print(M1.attributes)