#!/usr/bin/python

import sys

from gdsii.library import Library
from gdsii.elements import *

INDENT = 0
def OUT(s):
    sys.stdout.write('%s%s\n' % (' ' * INDENT, s));
def INC_INDENT():
    global INDENT
    INDENT = INDENT + 3
def DEC_INDENT():
    global INDENT
    INDENT = max(INDENT - 3, 0)

def print_gds_element_elflags(element):
    if element.elflags:
        OUT('elflags      : %s' % '{0:016b}'.format(element.elflags))

def print_gds_element_plex(element):
    if element.plex:
        OUT('plex         : %d' % element.plex)

def print_gds_element_layer(element):
    OUT('layer        : %d' % element.layer)

def print_gds_element_data_type(element):
    OUT('data_type    : %d' % element.data_type)

def print_gds_element_path_type(element):
    if element.path_type:
        OUT('path_type    : %d' % element.path_type)

def print_gds_element_width(element):
    if element.width:
        OUT('width        : %d' % element.width)

def print_gds_element_bgn_extn(element):
    if element.bgn_extn:
        OUT('bgn_extn     : %d' % element.bgn_extn)

def print_gds_element_end_extn(element):
    if element.end_extn:
        OUT('end_extn     : %d' % element.end_extn)

def print_gds_element_xy(element):
    OUT('%d xy points:' % len(element.xy))
    INC_INDENT()
    for xy in element.xy:
        OUT(str(xy))
    DEC_INDENT()

def print_gds_element_struct_name(element):
    OUT('struct_name   : %s' % element.struct_name)

def print_gds_element_strans(element):
    if element.strans:
        OUT('strans       : %s' % '{0:016b}'.format(element.strans))

def print_gds_element_man(element):
    if element.mag:
        OUT('mag          : %g' % element.mag)

def print_gds_element_angle(element):
    if element.angle:
        OUT('angle        : %f' % element.angle)

def print_gds_element_cols(element):
    OUT('cols         : %d' % element.cols)

def print_gds_element_rows(element):
    OUT('rows         : %d' % element.rows)

def print_gds_element_text_type(element):
    OUT('text_type    : %d' % element.text_type)

def print_gds_element_presentation(element):
    if element.presentation:
        OUT('presentation : %s' % '{0:016b}'.format(element.presentation))

def print_gds_element_string(element):
    OUT('string       : "%s"' % element.string)

def print_gds_element_node_type(element):
    OUT('node_type    : %d' % element.node_type)

def print_gds_element_box_type(element):
    OUT('box_type     : %d' % element.box_type)

def print_gds_element_properties(element):
    if element.properties:
        OUT('%d properties:' % len(element.properties))
        INC_INDENT()
        for prop in element.properties:
            OUT(str(prop))
        DEC_INDENT()

def print_gds_element(element):
    OUT('element type "%s"' % type(element).__name__.upper())
    INC_INDENT()
    print_gds_element_elflags(element)
    if not isinstance(element, SRef):
        print_gds_element_plex(element)
    if isinstance(element, (ARef, Boundary)):
        print_gds_element_layer(element)
        print_gds_element_data_type(element)
    if isinstance(element, Box):
        print_gds_element_layer(element)
        print_gds_element_box_type(element)
    if isinstance(element, Node):
        print_gds_element_layer(element)
        print_gds_element_node_type(element)
    if isinstance(element, Path):
        print_gds_element_layer(element)
        print_gds_element_data_type(element)
        print_gds_element_path_type(element)
        print_gds_element_width(element)
        print_gds_element_bgn_extn(element)
        print_gds_element_end_extn(element)
    if isinstance(element, SRef):
        print_gds_element_struct_name(element)
        print_gds_element_strans(element)
    if isinstance(element, Text):
        print_gds_element_layer(element)
        print_gds_element_text_type(element)
        print_gds_element_presentation(element)
        print_gds_element_path_type(element)
        print_gds_element_width(element)
        print_gds_element_strans(element)
        print_gds_element_string(element)
    print_gds_element_xy(element)
    print_gds_element_properties(element)
    DEC_INDENT()

def print_gds_structure(structure):
    OUT('structure "%s" details:' % structure.name)
    INC_INDENT()
    OUT('mod_time : %s' % str(structure.mod_time))
    OUT('acc_time : %s' % str(structure.acc_time))
    if structure.strclass:
        OUT('strclass : %d' % structure.strclass)
    OUT('%d elements:' % len(structure))
    INC_INDENT()
    for element in structure:
        print_gds_element(element)
    DEC_INDENT()
    DEC_INDENT()

def print_gds_library(lib):
    OUT('library "%s" details:' % lib.name)
    INC_INDENT()
    OUT('version       : %d' % lib.version)
    OUT('physical_unit : %g' % lib.physical_unit)
    OUT('logical_unit  : %g' % lib.logical_unit)
    OUT('mod_time      : %s' % str(lib.mod_time))
    OUT('acc_time      : %s' % str(lib.acc_time))
    if lib.libdirsize:
        OUT('libdirsize    : %d' % lib.libdirsize)
    if lib.srfname:
        OUT('srfname       : %s' % lib.srfname)
    if lib.acls:
        OUT('%d acls:' % len(lib.acls))
        INC_INDENT()
        for acl in lib.acls:
            OUT('   %s' % str(acl))
        DEC_INDENT()
    if lib.reflibs:
        OUT('reflibs       : %s' % lib.reflibs)
    if lib.attrtable:
        OUT('attrtable     : %s' % lib.attrtable)
    if lib.generations:
        OUT('generations   : %d' % lib.generations)
    if lib.format:
        OUT('format        : %d' % lib.format)
    if lib.masks:
        OUT('%d masks:' % len(lib.masks))
        INC_INDENT()
        for mask in lib.masks:
            OUT('   %s' % mask)
        DEC_INDENT()
    OUT('%d structures:' % len(lib))
    INC_INDENT()
    for structure in lib:
        print_gds_structure(structure)
    DEC_INDENT()
    DEC_INDENT()
