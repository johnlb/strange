# Possible CSS syntax uses
ex:
/#M1 {
    width:100%;
    border:3px
}

- M1 selects the device M1
- width:100% sets the width to fill the whole cell bounding box
- border: invokes a border around M1 (i.e. guard ring) of width 3(px?)

## Selectors
- /# selects id (ie. ref des) of a device
- . selects device (or net) class
- no modifier selects an element (anything with prefix R in ref des?)
This seems slightly confusing... maybe should make /# the element selector?


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


## 
