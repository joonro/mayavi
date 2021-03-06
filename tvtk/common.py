"""Common functions and classes that do not require any external
dependencies (apart from the standard library of course).

"""
# Author: Prabhu Ramachandran <prabhu_r@users.sf.net>
# Copyright (c) 2005-2007, Enthought, Inc.
# License: BSD Style.

import string
import re

######################################################################
# Utility functions.
######################################################################

def get_tvtk_name(vtk_name):
    """Converts a VTK class name to a TVTK class name.

    This function additionally converts any leading digits into a
    suitable string.

    For example:

      >>> get_tvtk_name('vtk3DSImporter')
      'ThreeDSImporter'
      >>> get_tvtk_name('vtkXMLDataReader')
      'XMLDataReader'

    """
    if vtk_name[:3] == 'vtk':
        name = vtk_name[3:]
        dig2name = {'1':'One', '2':'Two', '3':'Three', '4':'Four',
                    '5':'Five', '6': 'Six', '7':'Seven', '8':'Eight',
                    '9': 'Nine', '0':'Zero'}

        if name[0] in string.digits:
            return dig2name[name[0]] + name[1:]
        else:
            return name
    else:
        return vtk_name



class _Camel2Enthought:
    """Simple functor class to convert names from CamelCase to
    Enthought compatible names.

    For example::
      >>> camel2enthought = _Camel2Enthought()
      >>> camel2enthought('XMLActor2DToSGML')
      'xml_actor2d_to_sgml'

    """

    def __init__(self):
        self.patn = re.compile(r'([A-Z0-9]+)([a-z0-9]*)')
        self.nd_patn = re.compile(r'(\D[123])_D')
    def __call__(self, name):
        ret = self.patn.sub(self._repl, name)
        ret = self.nd_patn.sub(r'\1d', ret)
        if ret[0] == '_':
            ret = ret[1:]
        return ret.lower()
    def _repl(self, m):
        g1 = m.group(1)
        g2 = m.group(2)
        if len(g1) > 1:
            if g2:
                return '_' + g1[:-1] + '_' + g1[-1] + g2
            else:
                return '_' + g1
        else:
            return '_' + g1 + g2

# Instantiate a converter.
camel2enthought = _Camel2Enthought()
