#!/usr/bin/python
# Let's play with gds import/export...

from gdsii.library import Library
from gdsii.elements import *

from print_gds import *

OUT('Reading file "IFneuron.gds"...')
with open('IFneuron.gds', 'rb') as stream:
    lib = Library.load(stream)
OUT('Done.')
OUT('')

print_gds_library(lib)

