from enum import IntFlag

import comtypes.gen._0002E157_0000_0000_C000_000000000046_0_5_3 as __wrapper_module__
from comtypes.gen._0002E157_0000_0000_C000_000000000046_0_5_3 import (
    ProjectTemplate, Window, _CodePanes, vbext_ct_ClassModule,
    vbextFileTypeForm, vbext_cv_FullModuleView, COMMETHOD, Component,
    _VBProject_Old, Library, _Components, _VBProjects, vbext_pk_Set,
    vbext_wt_CodeWindow, _AddIns, VBE, vbextFileTypeFrx,
    vbext_cv_ProcedureView, vbext_ct_StdModule, typelib_path,
    vbext_wt_Locals, vbext_ct_Document, vbext_wt_Browser,
    vbext_wt_Find, _dispCommandBarControlEvents, vbextFileTypeBinary,
    Addins, VBComponents, _VBProjectsEvents, vbextFileTypeModule,
    vbextFileTypeProject, _VBComponent, _Windows, VARIANT_BOOL,
    vbext_ws_Minimize, _VBProjects_Old, vbextFileTypeExe,
    _LinkedWindows, vbextFileTypeGroupProject,
    vbextFileTypeUserControl, Application, vbext_wt_PropertyWindow,
    vbextFileTypeDesigners, GUID, vbext_wt_LinkedWindowFrame,
    vbextFileTypePropertyPage, Components, _Windows_old, _References,
    vbext_vm_Design, AddIn, vbext_vm_Break, _CommandBarControlEvents,
    _dispReferences_Events, DISPMETHOD, CodeModule, vbext_pk_Get,
    CodePane, SelectedComponents, CommandBarEvents, vbext_vm_Run,
    _dispReferencesEvents, vbext_pp_none, dispid,
    vbextFileTypeDocObject, _CodePane, vbext_wt_FindReplace, Windows,
    CodePanes, vbext_wt_ToolWindow, vbext_pk_Proc,
    vbext_pt_HostProject, vbext_rk_TypeLib, Reference,
    _VBComponent_Old, _VBComponents, vbext_wt_Toolbox, VARIANT,
    _check_version, vbext_ct_MSForm, vbext_ws_Maximize, Property,
    VBProjects, vbext_wt_Designer, vbext_pk_Let, _VBComponents_Old,
    vbext_wt_ProjectWindow, vbext_wt_Watch, ReferencesEvents,
    _ReferencesEvents, vbext_ws_Normal, VBComponent, _Component,
    vbext_ct_ActiveXDesigner, _VBProject, _Properties,
    _VBComponentsEvents, vbext_pp_locked, _ProjectTemplate,
    _dispVBComponentsEvents, IUnknown, _lcid, Events, References,
    vbext_wt_Immediate, IDispatch, vbext_wt_MainWindow, VBProject,
    vbext_rk_Project, vbext_pt_StandAlone, HRESULT, BSTR,
    vbextFileTypeClass, LinkedWindows, _dispVBProjectsEvents,
    Properties, _CodeModule, CoClass, vbextFileTypeRes
)


class vbext_ProcKind(IntFlag):
    vbext_pk_Proc = 0
    vbext_pk_Let = 1
    vbext_pk_Set = 2
    vbext_pk_Get = 3


class vbext_ProjectType(IntFlag):
    vbext_pt_HostProject = 100
    vbext_pt_StandAlone = 101


class vbext_ComponentType(IntFlag):
    vbext_ct_StdModule = 1
    vbext_ct_ClassModule = 2
    vbext_ct_MSForm = 3
    vbext_ct_ActiveXDesigner = 11
    vbext_ct_Document = 100


class vbext_RefKind(IntFlag):
    vbext_rk_TypeLib = 0
    vbext_rk_Project = 1


class vbextFileTypes(IntFlag):
    vbextFileTypeForm = 0
    vbextFileTypeModule = 1
    vbextFileTypeClass = 2
    vbextFileTypeProject = 3
    vbextFileTypeExe = 4
    vbextFileTypeFrx = 5
    vbextFileTypeRes = 6
    vbextFileTypeUserControl = 7
    vbextFileTypePropertyPage = 8
    vbextFileTypeDocObject = 9
    vbextFileTypeBinary = 10
    vbextFileTypeGroupProject = 11
    vbextFileTypeDesigners = 12


class vbext_VBAMode(IntFlag):
    vbext_vm_Run = 0
    vbext_vm_Break = 1
    vbext_vm_Design = 2


class vbext_ProjectProtection(IntFlag):
    vbext_pp_none = 0
    vbext_pp_locked = 1


class vbext_WindowState(IntFlag):
    vbext_ws_Normal = 0
    vbext_ws_Minimize = 1
    vbext_ws_Maximize = 2


class vbext_WindowType(IntFlag):
    vbext_wt_CodeWindow = 0
    vbext_wt_Designer = 1
    vbext_wt_Browser = 2
    vbext_wt_Watch = 3
    vbext_wt_Locals = 4
    vbext_wt_Immediate = 5
    vbext_wt_ProjectWindow = 6
    vbext_wt_PropertyWindow = 7
    vbext_wt_Find = 8
    vbext_wt_FindReplace = 9
    vbext_wt_Toolbox = 10
    vbext_wt_LinkedWindowFrame = 11
    vbext_wt_MainWindow = 12
    vbext_wt_ToolWindow = 15


class vbext_CodePaneview(IntFlag):
    vbext_cv_ProcedureView = 0
    vbext_cv_FullModuleView = 1


__all__ = [
    'ProjectTemplate', 'Window', 'vbext_cv_FullModuleView',
    'Component', 'Library', 'vbext_WindowType', '_Components',
    'vbext_pk_Set', 'vbext_wt_CodeWindow', '_AddIns', 'VBE',
    'typelib_path', 'vbext_wt_Locals', 'vbext_ct_Document',
    'vbext_ComponentType', 'vbext_ProjectProtection', 'Addins',
    '_VBProjectsEvents', '_VBComponent', '_VBProjects_Old',
    '_References', 'vbext_vm_Break', '_CommandBarControlEvents',
    'CodePane', 'SelectedComponents', 'CommandBarEvents',
    '_dispReferencesEvents', '_CodePane', 'vbext_VBAMode', 'Windows',
    'vbext_wt_ToolWindow', 'vbext_ct_MSForm', 'vbext_ws_Maximize',
    'Property', 'vbext_wt_Designer', 'vbext_pk_Let',
    'vbext_wt_ProjectWindow', 'ReferencesEvents', 'vbext_ws_Normal',
    'VBComponent', 'vbext_ct_ActiveXDesigner', '_VBProject',
    '_ProjectTemplate', '_dispVBComponentsEvents',
    'vbext_CodePaneview', 'Events', 'VBProject',
    'vbext_pt_StandAlone', 'vbextFileTypes', 'vbextFileTypeClass',
    'LinkedWindows', '_dispVBProjectsEvents', 'vbext_ProcKind',
    '_CodePanes', 'vbext_ct_ClassModule', 'vbextFileTypeForm',
    '_VBProject_Old', '_VBProjects', 'vbextFileTypeFrx',
    'vbext_cv_ProcedureView', 'vbext_ct_StdModule',
    'vbext_wt_Browser', 'vbext_wt_Find',
    '_dispCommandBarControlEvents', 'vbextFileTypeBinary',
    'VBComponents', 'vbextFileTypeModule', 'vbextFileTypeProject',
    '_Windows', 'vbext_ws_Minimize', 'vbextFileTypeExe',
    '_LinkedWindows', 'vbextFileTypeGroupProject',
    'vbextFileTypeUserControl', 'Application', 'vbext_WindowState',
    'vbext_wt_PropertyWindow', 'vbextFileTypeDesigners',
    'vbext_wt_LinkedWindowFrame', 'vbextFileTypePropertyPage',
    'Components', '_Windows_old', 'vbext_vm_Design', 'AddIn',
    '_dispReferences_Events', 'CodeModule', 'vbext_pk_Get',
    'vbext_vm_Run', 'vbext_pp_none', 'vbextFileTypeDocObject',
    'vbext_wt_FindReplace', 'CodePanes', 'vbext_pk_Proc',
    'vbext_pt_HostProject', 'vbext_rk_TypeLib', 'Reference',
    'vbext_ProjectType', '_VBComponent_Old', '_VBComponents',
    'vbext_wt_Toolbox', 'VBProjects', '_VBComponents_Old',
    'vbext_wt_Watch', '_ReferencesEvents', '_Component',
    '_Properties', '_VBComponentsEvents', 'vbext_pp_locked',
    'References', 'vbext_wt_Immediate', 'vbext_wt_MainWindow',
    'vbext_rk_Project', 'Properties', '_CodeModule', 'vbext_RefKind',
    'vbextFileTypeRes'
]

