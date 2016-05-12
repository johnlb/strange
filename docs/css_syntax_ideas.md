# Possible CSS syntax uses - Layout
ex:  
\#M1 {  
    width:100%;  
    border:3em  
}

- M1 selects the device M1
- width:100% sets the width to fill the whole cell bounding box
- border: invokes a border around M1 (i.e. guard ring) of width 3x min width of a guard ring


Note: Currently compiling 1:1 mapping (as best I can) between standard CSS and circuit layout equivalent. We can think about what to change from there.

## px notation?
So, one thing you can do in css is define things in pixels.
- Probably, 1px = 1 grid space (i.e. 0.005 um for most kits)
- *Preferrably*, the % notation would be used unless absolutely necessary. % would define a dimension relative to its minimum value. Probably should have both though.

## em notation
em is a unit that usually means "relative to font-size of the element"

We could repurpose this as "relative to the min. dimension of the property"


## @ rules
- @import is like an include statement for CSS
- Maybe setting parameters of the cell itself are @ rules? (ie setting bounding box is @bbox or something?)


## Selectors
- \# selects id (ie. ref des) of a device
- . selects device (or net) class
- no modifier selects an element (anything with prefix R in ref des?)

This seems slightly confusing... maybe should make \# the element selector?


## Borders
- Auto-generate guard ring around whatever it is applied to with specified thickness
- What is 1px? Do we have to redefine units?


## Padding / Margin (Box Model)
- Padding = distance to guard ring
- Margin = distance to nearest object (including well spacing?)
- Margin:auto put empty space on either side of device


## Height / Width
- Used to invoke dummies (i.e. 100% width means center device in bbox and fill rest with dummies)
- What defines outer dimensions of cell?
    + user-defined
    + dynamic (based on size of other objects in cell)


## Display
- display:none could be for app-specific feature sets? (i.e. change feature set implemented for a given product w/o changing core design)
    + display:none regenerates layout without element
    + visibility:hidden removes elements without moving anything else
- block level / inline elements, same as in html


## Position
- This is how we allow fixed positioning as well as relative positioning
- position:static is default
- position:relative moves *realtive to normal position*
- position:fixed forces placement of a block *relative to cell bounding box*
- position:absolute forces placement *relative to another block*

Maybe we can swap absolute with relative? It makes not a lot of sense in this context.


## Float
- This is how to typically position blocks under position:static (probably the most process-agnostic way?)
- float:right
- float:left
- clear forces left/right side of a floating block to be empty


## Combinators
- Not sure there's a use for these yet. There's really not much use for the concept of child and sibling blocks as in html (unless you're talking about descending heirarchy, which could be cool but definitely not a thing to implement now)


## Pseudo-classes (etc.)
- Some pseudo-classes could be useful (ie :not(selector) to select everything but a certain thing), but it is pretty low on the priority list.


## Attribute Selectors
- select elements with a certain attribute
- useful, but low on priority list


## CSS3 Transforms
- Will have to implement this inside tinycss (shouldn't be hard)
- Definitley important to control rotations, etc. of devices if you want (autoplacer needs this ability anyway)









# Possible Uses - Schematic

Schematic could have the exact same structure maybe? Use CSS to describe layout of schematic. This is where all the text and coloring attributes come in, but how do you describe line routing?
