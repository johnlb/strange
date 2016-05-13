# TO DO

## Big-picture
1. <del>Get basic drawing (export/import) and visualization going.</del>
2. <del>Define and implement artist module (final renderer, before export) -- This means deciding how to do tech file integration </del>
3. <del>Define netlist format</del>
4. <del>Build netlist parser</del>
3. <del>Link netlist, stylesheet to artist module</del>
4. Build features


## high-priority gdspy features
1. <del>translation for basic geometries</del>
2. <del>copy method for geometries</del>
3. <del>translation for non-geomtry objects</del>
4. libraries


## artist
1. better lib structure
2. fix caps in parameters
3. objectify artist tasks

## libraries

### core
1. BJT process variant? or BiCMOS?
2. Should fully type-check arguments @ artist?
4. Make contactHelper
4. Make contactHelper capable of multiple columns?
5. Make contactHelper better at trimming overrunning contacts?



## little big things
1. better way of referencing files -- allow env variables in html?
2. better error reporting
    - css / html source filename
    - more coverage
3. proper placement of techfile?
    - shouldn't have to redefine for all heirarchy...
4. better library linking system.
    - how does the artist know to load the library?
5. automatic extents calculation


## netlist
1. Simulation netlist exporter -- hspice, spectre
2. Netlist importer -- hspice, spectre
2. JS-like DOM API
3. 
