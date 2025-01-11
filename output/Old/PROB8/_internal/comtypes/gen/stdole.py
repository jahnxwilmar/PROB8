from enum import IntFlag

import comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0 as __wrapper_module__
from comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0 import (
    IFontEventsDisp, OLE_HANDLE, COMMETHOD, OLE_YSIZE_CONTAINER, Gray,
    Library, OLE_XPOS_CONTAINER, OLE_XSIZE_CONTAINER, Default,
    typelib_path, EXCEPINFO, VgaColor, OLE_COLOR, VARIANT_BOOL,
    DISPPROPERTY, FONTSTRIKETHROUGH, OLE_YPOS_PIXELS, DISPPARAMS,
    Picture, OLE_OPTEXCLUSIVE, IFont, GUID, Color, OLE_CANCELBOOL,
    StdFont, Monochrome, DISPMETHOD, FONTUNDERSCORE, StdPicture,
    OLE_YSIZE_HIMETRIC, FontEvents, Unchecked, dispid, IPicture,
    IPictureDisp, OLE_ENABLEDEFAULTBOOL, OLE_XSIZE_HIMETRIC,
    OLE_XPOS_PIXELS, _check_version, OLE_YPOS_CONTAINER, Checked,
    FONTITALIC, FONTNAME, OLE_XSIZE_PIXELS, OLE_YPOS_HIMETRIC,
    IUnknown, _lcid, FONTBOLD, FONTSIZE, OLE_XPOS_HIMETRIC,
    IEnumVARIANT, IDispatch, IFontDisp, Font, BSTR, HRESULT, CoClass,
    OLE_YSIZE_PIXELS
)


class OLE_TRISTATE(IntFlag):
    Unchecked = 0
    Checked = 1
    Gray = 2


class LoadPictureConstants(IntFlag):
    Default = 0
    Monochrome = 1
    VgaColor = 2
    Color = 4


__all__ = [
    'IFontEventsDisp', 'OLE_YSIZE_HIMETRIC', 'OLE_HANDLE',
    'FontEvents', 'Unchecked', 'LoadPictureConstants',
    'OLE_YSIZE_CONTAINER', 'Gray', 'IPicture', 'Library',
    'OLE_ENABLEDEFAULTBOOL', 'IPictureDisp', 'OLE_XPOS_CONTAINER',
    'OLE_XSIZE_HIMETRIC', 'OLE_XPOS_PIXELS', 'OLE_XSIZE_CONTAINER',
    'Default', 'OLE_YPOS_CONTAINER', 'typelib_path', 'Checked',
    'OLE_TRISTATE', 'FONTITALIC', 'VgaColor', 'FONTNAME', 'OLE_COLOR',
    'OLE_YPOS_PIXELS', 'OLE_XSIZE_PIXELS', 'Picture',
    'OLE_YPOS_HIMETRIC', 'FONTBOLD', 'FONTSIZE', 'OLE_OPTEXCLUSIVE',
    'IFont', 'OLE_XPOS_HIMETRIC', 'Color', 'OLE_CANCELBOOL',
    'IFontDisp', 'Font', 'Monochrome', 'StdFont', 'FONTSTRIKETHROUGH',
    'FONTUNDERSCORE', 'StdPicture', 'OLE_YSIZE_PIXELS'
]

