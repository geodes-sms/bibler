'''
BiBler - A software to manage references of scientific articles using BibTeX.
Copyright (C) 2018  Eugene Syriani

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

"""
Created on Jan 13, 2014
.. moduleauthor:: Eugene Syriani
.. moduleauthor:: Florin Oncica 

.. versionadded:: 1.0

This module represents the graphical user interface of BiBler.
It should be used as an API that a statechart controller can invoke.

@group Main GUI class: BiBlerGUI
@group Widgets: ActionCancelDialog, EditorTab, EntryEditor, EntryList, EntryPreviewer, EntryWidget, HTMLDialog, HTMLWindow, PreferencesDialog, SearchDialog
@sort: A*, B*, E*, H*, P*, S*
"""

import wx
import wx.lib.mixins.listctrl as wxLC
import wx.html as wxHTML
import webbrowser
from utils import settings, resourcemgr
from gui.app_interface import EntryListColumn
from app.entry_type import EntryType
from utils.settings import BibStyle
"""
from wx import Orientation, BORDER, DefaultSize, Border
from tkinter.constants import HORIZONTAL
from docutils.parsers.rst.directives import flag
from math import ceil
from colorama.ansi import Style
from docutils.nodes import title
from _operator import pos
from cProfile import label
from test.test_largefile import size
"""
prefs = settings.Preferences()
"""
Load the preferences.
"""
resMgr = resourcemgr.ResourceManager()
"""
Load the resource manager.
"""

class EntryWidget(object):
    """
    A widget to control entries.
    """
    def __init__(self, rows, cols, behavior=None):
        """
        @type rows: L{int}
        @param rows: The number of rows of the C{wx.FlexGridSizer} of the widget.
        @type cols: L{int}
        @param cols: The number of columns of the C{wx.FlexGridSizer} of the widget.
        @type behavior: L{controller.Controller}
        @param behavior: The statechart controller that defines the behavior of this widget.
        """
        self.behavior = behavior
        self.sizer = wx.FlexGridSizer(rows=rows, cols=cols, vgap=0, hgap=0)
    
    def clear(self):
        """
        Clear the content of the widget.
        """
        raise NotImplemented()
    
    def getSizer(self):
        """
        Get the sizer of the L{EntryEditor}.
        
        @rtype: C{wx.FlexGridSizer}
        @return: The sizer.
        """
        return self.sizer
    
    def getBehavior(self):
        """
        @rtype behavior: L{controller.Controller}
        @return: The statechart controller that defines the behavior of this widget.
        """
        return self.behavior

class EntryList(wx.ListCtrl, wxLC.ListCtrlAutoWidthMixin):
    """
    The list of entries.    
    It contains the 7 columns from L{gui.app_interface.EntryDict}: id, Paper, Type, Author, Title, Year, Key.
    @group Events: __on*
    @sort: __*, a*, d*, g*, G*, i*, r*, s*, u*
    
    """
    WARNING_COLOR = wx.Colour(255, 246, 232)
    ERROR_COLOR = wx.Colour(255, 127, 127)
    SUCCESS_COLOR = wx.Colour(255, 255, 255)
    
    def __init__(self, parent, behavior):
        """
        @type parent: C{wx.Window}
        @param parent: The parent window. Must be not C{None}.
        @type behavior: L{controller.Controller}
        @param behavior: The statechart controller that defines the behavior of this window.
        """
        wx.ListCtrl.__init__(self, parent, wx.NewId(),
                             style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.SUNKEN_BORDER
                                    | wx.LC_HRULES | wx.LC_VRULES | wx.EXPAND)
        wxLC.ListCtrlAutoWidthMixin.__init__(self)
        
        self.behavior = behavior
        
        self.InsertColumn(0, "#", width=53)
        self.InsertColumn(1, "Paper", width=20)
        self.InsertColumn(2, "Type", width=100)
        self.InsertColumn(3, "Author", width=200)
        self.InsertColumn(4, "Title", width=500)
        self.InsertColumn(5, "Year", width=50)
        self.InsertColumn(6, "Key", width=100)
        self.setResizeColumn(3)
        self.setResizeColumn(4)
        self.setResizeColumn(5)
        self.paperImageList = wx.ImageList(16, 16)
        bitmap = wx.Bitmap(resMgr.getPaperImagePath(), wx.BITMAP_TYPE_PNG)
        self.paperImageList.Add(bitmap)
        self.AssignImageList(self.paperImageList, wx.IMAGE_LIST_SMALL) 
        
        self.Bind(wx.EVT_LIST_ITEM_SELECTED,self.__onEntrySelected)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.__onEntryDeselected)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.__onEntryDoubleClicked)
        self.Bind(wx.EVT_LIST_COL_CLICK, self.__onColumnClicked)
        
    def __onEntrySelected(self, e):
        """
        Triggered when a row is clicked.
        @type e: C{wx.ListEvent}
        """
        self.behavior.entrySelected(self.getEntryId(e.GetIndex()))
        
    def __onEntryDeselected(self, e):
        """
        Triggered when another row entry is clicked in the list.
        @type e: C{wx.ListEvent}
        """
        flag = self.GetFocusedItem()
        self.behavior.entryDeselected(flag)
    
    def __onEntryDoubleClicked(self, e):
        """
        Triggered when a row is double-clicked.
        @type e: C{wx.ListEvent}
        """
        self.behavior.entryDoubleClicked(self.getEntryId(e.GetIndex()))
    
    def __onColumnClicked(self, e):
        """
        Triggered when the header of a column is clicked.
        @type e: C{wx.ListEvent}
        """
        col = e.GetColumn()
        if col == 0:
            self.behavior.colIdClicked()
        elif col == 1:
            self.behavior.colPaperClicked()
        elif col == 2:
            self.behavior.colTypeClicked()
        elif col == 3:
            self.behavior.colAuthorClicked()
        elif col == 4:
            self.behavior.colTitleClicked()
        elif col == 5:
            self.behavior.colYearClicked()
        elif col == 6:
            self.behavior.colKeyClicked()       
    
    def GetListCtrl(self):
        """
        Required by C{wx.lib.mixins.listctrl.ListCtrlAutoWidthMixin}.
        """
        return self
    
    def getEntryId(self, row):
        """
        Returns the id of the entry on this row.
        @type row: C{int}
        @param row: The index of a row.
        @rtype: C{int}
        @return: The id of the entry.
        """
        return int(self.GetItem(row, 0).GetText())
    
    def isEntrySelected(self):
        """
        Check if a row is selected.
        @rtype: L{bool}
        @return: C{True} if a row is selected. C{False} otherwise.
        """
        return self.GetSelectedItemCount() > 0
    
    def selectEntryRow(self, entryId):
        """
        Select the row corresponding to the entry I{id}.
        @type entryId: L{int}
        @param entryId: The I{id} of the entry.
        @raise Exception: If no entry was found.
        """
        index = self.FindItem(0, str(entryId))
        if index == wx.NOT_FOUND:
            raise Exception('Entry not found.')
        self.Select(index)
        self.EnsureVisible(index)
        return True
        
    def unselectEntryRow(self):
        """
        Ensure no row is selected.
        """
        self.Select(-1)
        return True
    
    def displayEntries(self, entryList):
        """
        Show the entry list, one row per entry.
        @type entryList: L{list} of L{EntryDict}
        @param entryList: The list of entries to show.
        """
        self.DeleteAllItems()
        for entry in entryList:
            self.addEntryRow(entry)
        return True
    
    def addEntryRow(self, entryDict):
        """
        Add a new row filled with the data for an entry.
        @type entryDict: L{EntryDict}
        @param entryDict: The dictionary representation of an entry.
        """
        row = self.Append(self.__entryDictToRowTuple(entryDict))
        self.SetItemColumnImage(row, 0, -1)
        self.showPDFIcon(row, entryDict[EntryListColumn.Paper])
        self.colorRow(row, (entryDict[EntryListColumn.Valid],entryDict[EntryListColumn.Message]))
        return True
    
    def updateSelectedEntryRow(self, entryDict):
        """
        Update the columns of a row with the data provided.
        @type entryDict: L{EntryDict}
        @param entryDict: The dictionary representation of an entry.
        @raise Exception: If no row was selected.
        """
        row = self.GetFirstSelected()
        if row < 0: raise Exception('No entry selected.')
        data = self.__entryDictToRowTuple(entryDict)
        for i in range(len(data)):
            self.SetItem(row, i, data[i])
        self.showPDFIcon(row, entryDict[EntryListColumn.Paper])
        self.colorRow(row, (entryDict[EntryListColumn.Valid],entryDict[EntryListColumn.Message]))
        return True
    
    def removeEntryRow(self, entryId):
        """
        Remove the row corresponding to the entry I{id}.
        @type entryId: L{int}
        @param entryId: The I{id} of the entry.
        @raise Exception: If no entry was found.
        """
        index = self.FindItem(0, str(entryId))
        if index == wx.NOT_FOUND:
            raise Exception('Entry not found.')
        self.DeleteItem(index)
        return True
    
    def showPDFIcon(self, row, data):
        """
        Display a PDF icon in the C{paper} column if C{data != ''}.
        @type row: L{int}
        @param row: The index of a row.
        @type data: L{str}
        @param data: The uri of the paper.
                        
        """
        if data != '':
            self.SetItemColumnImage(row, 1, 0)
            self.SetItem(row, 1, '')    # only display the icon, so remove text
        else:
            self.SetItemColumnImage(row, 1, -1)
        return True
    
    def colorRow(self, row, data):
        """
        Color the row in red if C{data} is L{False}.
        @type row: L{int}
        @param row: The index of a row.
        @type data: L{str}
        @param data: The uri of the paper.
                        
        """
        valid, msg = data
        if valid and msg:
            self.SetItemBackgroundColour(row, EntryList.WARNING_COLOR)
        elif not valid:
            self.SetItemBackgroundColour(row, EntryList.ERROR_COLOR)
        else:
            self.SetItemBackgroundColour(row, EntryList.SUCCESS_COLOR)
    
    def __entryDictToRowTuple(self, entryDict):
        """
        Converts an L{EntryDict} into a L{tuple}.
        The order of the data is the same as in L{EntryList}.
        In the case of multiple authors, the I{et al.} notation is used.
        @type entryDict: L{EntryDict}
        @param entryDict: The dictionary representation of an entry.
        @rtype: L{tuple}
        @return: The tuple representation of the C{entryDict}.
        """
        author = str(entryDict[EntryListColumn.Author])
        if 'and' in author:
            author = author.split(',')[0] + ' et al.'
        else:
            author = author.split(',')[0]
        return (str(entryDict[EntryListColumn.Id]), str(entryDict[EntryListColumn.Paper]), str(entryDict[EntryListColumn.Entrytype]),
               author, str(entryDict[EntryListColumn.Title]), str(entryDict[EntryListColumn.Year]), str(entryDict[EntryListColumn.Entrykey]))

class EditorTab(wx.Panel):
    """
    A tab in the L{EntryEditor}.
    """
    WARNING_COLOR = wx.Colour(255, 246, 232)
    ERROR_COLOR = wx.Colour(255, 127, 127)
    SUCCESS_COLOR = wx.Colour(255, 255, 255)
    NO_EDIT_FIELD_COLOR = wx.Colour(222, 226, 232)
    
    def __init__(self, parent):
        """
        @type parent: C{wx.Window}
        @param parent: The parent window. Must be not C{None}.
        """
        super(EditorTab, self).__init__(parent, wx.NewId())
        
class EditorFieldsTab(EditorTab):
    """
    Abstract class for tabs with editable fields in the L{EntryEditor}.
    """
    def __init__(self, parent, behavior):
        """
        @type parent: C{EditorTab}
        @param parent: The parent window. Must be not C{None}.
        @type behavior: L{controller.Controller}
        @param behavior: The statechart controller that defines the behavior of this widget.
        """
        super().__init__(parent)
        self.behavior = behavior
        self.LABEL_COLOR = wx.Colour((89, 125, 183))
        self.name = ""
        self.ItemsList = []
    
    def setFields(self, data):
        """
        Replace text in fields tabs with names and values from C{data}.
        
        :type data: L{dic}
        :param data: The dictionary of fields for the entry.
        """
        raise NotImplementedError()
        
    
    def onTextChangedInFieldEditor(self, e):
        """
        Triggered every time the text is change in a tab field.
        
        @type evt: C{wx.CommandEvent}
        @param evt: C{wx_TxtCtrl} triggered event
        @type field: L{str}
        @param field: The name of the field        
        """
        txtCtrl = e.GetEventObject()
        self.behavior.textChangedInFieldEditor(e.GetString(), txtCtrl.GetName().lower())
        
    def onTextChangedInBibtexEditor(self, e):
        """
        Triggered every time the text is changed in Bibtex editor.
        @type e: C{wx.CommandEvent}
        """
        self.behavior.textChangedInEditor(e.GetString())
        
    def getName(self):
        """
        @rtype: L{str}
        @return: The name of the tab
        """
        return self.name
    
    def resetItemsList(self):
        """
        Empty the fields in fields tab editor.
        """
        self.ItemsList = []

class RequiredFields(EditorFieldsTab):
    """
    Concrete class of the L{EditorFieldsTab}.
    """
    def __init__(self, parent, behavior):
        """
        @see: L{gui.EditorFieldsTab.__init__}.
        """
        super().__init__(parent, behavior)        
        self.name = "Required Fields"
        self.ItemsList = []
        
        self.FieldsSizer = wx.FlexGridSizer(2,gap=wx.Size(5,0))
        self.FieldsSizer.AddGrowableCol(1, 0)
        self.SetSizerAndFit(self.FieldsSizer, deleteOld=False)
        
    def setFields(self, data):
        """
        @see: L{gui.EditorFieldsTab.setFields}.
        """
        if len(self.ItemsList) == 0:
            for field in data:
                name = field.getName()
                self.fieldsEditorLabel = wx.StaticText(self, wx.NewId(), label=name.title())                
                self.fieldsEditorLabel.SetForegroundColour(self.LABEL_COLOR)
                self.fieldsEditor = wx.TextCtrl(self, wx.NewId(), 
                                    style=wx.TE_MULTILINE | wx.TE_BESTWRAP, size=(-1,60),
                                    name = name)
                
                self.ItemsList.append({'labelId' : self.fieldsEditorLabel.GetId(), 'fieldId' : self.fieldsEditor.GetId()})
                   
                self.fieldsEditor.SetFont(wx.Font(pointSize=11, family=wx.FONTFAMILY_MODERN,
                                        style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_NORMAL))
                self.fieldsEditor.WriteText(field.getValue())
                self.fieldsEditor.SetInsertionPoint(0)
                self.fieldsEditor.Bind(wx.EVT_TEXT, self.onTextChangedInFieldEditor)
                self.FieldsSizer.AddMany([(self.fieldsEditorLabel),(self.fieldsEditor, 1, wx.EXPAND)])
            self.Layout()
        else:
            newItems = []
            for field in data:
                newItems.append({'label':field.getName().title(), 'text':field.getValue()})
            if len(newItems) <= len(self.ItemsList):
                for itm in range(0,len(newItems)):
                    item = self.ItemsList[itm]
                    widgetLabelId = item['labelId']
                    widgetFieldId = item['fieldId']
                    newItem = newItems[itm]
                    newLabel = newItem['label']
                    newText = newItem['text']
                    self.FindWindow(widgetLabelId).SetLabel(newLabel)
                    self.FindWindow(widgetFieldId).SetName(newLabel)
                    self.FindWindow(widgetFieldId).ChangeValue(newText)
                    
                for itm in reversed(range(len(newItems), len(self.ItemsList),1)):
                    widgetToDel = self.ItemsList[itm]
                    labelToDel = widgetToDel['labelId']
                    fieldToDel = widgetToDel['fieldId']
                    self.FindWindow(labelToDel).Destroy()
                    self.FindWindow(fieldToDel).Destroy()                   
                    del self.ItemsList[itm]
            else:
                for itm in range(0,len(self.ItemsList)):
                    item = self.ItemsList[itm]
                    widgetLabelId = item['labelId']
                    widgetFieldId = item['fieldId']
                    newItem = newItems[itm]
                    newLabel = newItem['label']
                    newText = newItem['text']
                    self.FindWindow(widgetLabelId).SetLabel(newLabel)
                    self.FindWindow(widgetFieldId).SetName(newLabel)
                    self.FindWindow(widgetFieldId).ChangeValue(newText)
                    
                for itm in range(len(self.ItemsList), len(newItems)):
                    newItem = newItems[itm]
                    newLabel = newItem['label']
                    newText = newItem['text']
                    self.fieldsEditorLabel = wx.StaticText(self, wx.NewId(), label=newLabel)                
                    self.fieldsEditorLabel.SetForegroundColour(self.LABEL_COLOR)
                    self.fieldsEditor = wx.TextCtrl(self, wx.NewId(), 
                                        style=wx.TE_MULTILINE | wx.TE_BESTWRAP, size=(-1,60),
                                        name = newLabel)
                
                    self.ItemsList.append({'labelId' : self.fieldsEditorLabel.GetId(), 'fieldId' : self.fieldsEditor.GetId()})
                       
                    self.fieldsEditor.SetFont(wx.Font(pointSize=11, family=wx.FONTFAMILY_MODERN,
                                            style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_NORMAL))
                    self.fieldsEditor.WriteText(newText)
                    self.fieldsEditor.SetInsertionPoint(0)
                    self.fieldsEditor.Bind(wx.EVT_TEXT, self.onTextChangedInFieldEditor)
                    self.FieldsSizer.AddMany([(self.fieldsEditorLabel),(self.fieldsEditor, 1, wx.EXPAND)])
                self.Layout()
        return True
    
class OptionalFileds(EditorFieldsTab):
    """
    Concrete class of the L{EditorFieldsTab}.
    """
    def __init__(self, parent, behavior):
        """
        @see: L{gui.EditorFieldsTab.__init__}.
        """
        super().__init__(parent, behavior)        
        self.name = "Optional Fields"
        
        self.FieldsSizer = wx.FlexGridSizer(4,gap=wx.Size(10,0))
        self.FieldsSizer.AddGrowableCol(1, 0)
        self.FieldsSizer.AddGrowableCol(3, 0)
        self.SetSizerAndFit(self.FieldsSizer, deleteOld=False)
        
    def setFields(self, data):
        """
        @see: L{gui.EditorFieldsTab.setFields}.
        """
        if len(self.ItemsList) == 0:
            for field in data:
                name = field.getName()
                self.fieldsEditorLabel = wx.StaticText(self, wx.NewId(), style=wx.ALIGN_RIGHT, label=name.title())
                self.fieldsEditorLabel.SetForegroundColour(self.LABEL_COLOR)
                self.fieldsEditor = wx.TextCtrl(self, wx.NewId(), 
                                    style=wx.TE_MULTILINE | wx.TE_BESTWRAP, size=(-1,42),
                                    name = name)
                
                self.ItemsList.append({'labelId' : self.fieldsEditorLabel.GetId(), 'fieldId' : self.fieldsEditor.GetId()})
                                
                self.fieldsEditor.SetFont(wx.Font(pointSize=11, family=wx.FONTFAMILY_MODERN,
                                        style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_NORMAL))
                self.fieldsEditor.WriteText(field.getValue())
                self.fieldsEditor.SetInsertionPoint(0)
                self.fieldsEditor.Bind(wx.EVT_TEXT, self.onTextChangedInFieldEditor)                
                self.FieldsSizer.AddMany([(self.fieldsEditorLabel),(self.fieldsEditor, 1, wx.EXPAND)])                        
            self.Layout()
        else:
            newItems = []
            for field in data:
                newItems.append({'label':field.getName().title(), 'text':field.getValue()})
            if len(newItems) <= len(self.ItemsList):
                for itm in range(0,len(newItems)):
                    item = self.ItemsList[itm]
                    widgetLabelId = item['labelId']
                    widgetFieldId = item['fieldId']
                    newItem = newItems[itm]
                    newLabel = newItem['label']
                    newText = newItem['text']
                    self.FindWindow(widgetLabelId).SetLabel(newLabel)
                    self.FindWindow(widgetFieldId).SetName(newLabel)
                    self.FindWindow(widgetFieldId).ChangeValue(newText)
                    
                for itm in reversed(range(len(newItems), len(self.ItemsList),1)):
                    widgetToDel = self.ItemsList[itm]
                    labelToDel = widgetToDel['labelId']
                    fieldToDel = widgetToDel['fieldId']
                    self.FindWindow(labelToDel).Destroy()
                    self.FindWindow(fieldToDel).Destroy()                   
                    del self.ItemsList[itm]
            else:
                for itm in range(0,len(self.ItemsList)):
                    item = self.ItemsList[itm]
                    widgetLabelId = item['labelId']
                    widgetFieldId = item['fieldId']
                    newItem = newItems[itm]
                    newLabel = newItem['label']
                    newText = newItem['text']
                    self.FindWindow(widgetLabelId).SetLabel(newLabel)
                    self.FindWindow(widgetFieldId).ChangeValue(newText)
                    
                for itm in range(len(self.ItemsList), len(newItems)):
                    newItem = newItems[itm]
                    newLabel = newItem['label']
                    newText = newItem['text']
                    self.fieldsEditorLabel = wx.StaticText(self, wx.NewId(), style=wx.ALIGN_RIGHT, label=newLabel)
                    self.fieldsEditorLabel.SetForegroundColour(self.LABEL_COLOR)
                    self.fieldsEditor = wx.TextCtrl(self, wx.NewId(), 
                                        style=wx.TE_MULTILINE | wx.TE_BESTWRAP, size=(-1,40),
                                        name = newLabel)
                    
                    self.ItemsList.append({'labelId' : self.fieldsEditorLabel.GetId(), 'fieldId' : self.fieldsEditor.GetId()})
                                     
                    self.fieldsEditor.SetFont(wx.Font(pointSize=11, family=wx.FONTFAMILY_MODERN,
                                            style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_NORMAL))
                    self.fieldsEditor.WriteText(field.getValue())
                    self.fieldsEditor.SetInsertionPoint(0)
                    self.fieldsEditor.Bind(wx.EVT_TEXT, self.onTextChangedInFieldEditor)                
                    self.FieldsSizer.AddMany([(self.fieldsEditorLabel),(self.fieldsEditor, 1, wx.EXPAND)])
                self.Layout()
        return True
    
class AdditionalFields(EditorFieldsTab):
    """
    Concrete class of the L{EditorFieldsTab}.
    """
    def __init__(self, parent, behavior):
        """
        @see: L{gui.EditorFieldsTab.__init__}.
        """
        super().__init__(parent, behavior)        
        self.name = "Additional Fields"
        
        self.FieldsSizer = wx.FlexGridSizer(2,gap=wx.Size(5,0))
        self.FieldsSizer.AddGrowableCol(1, 0)
        self.SetSizerAndFit(self.FieldsSizer, deleteOld=False)
        
    def setFields(self, data):
        """
        @see: L{gui.EditorFieldsTab.setFields}.
        """
        if len(self.ItemsList) == 0:
            for field in data:
                name = field.getName()
                self.fieldsEditorLabel = wx.StaticText(self, wx.NewId(), label=name.title())
                self.fieldsEditorLabel.SetForegroundColour(self.LABEL_COLOR)
                self.fieldsEditor = wx.TextCtrl(self, wx.NewId(), 
                                        style=wx.TE_MULTILINE | wx.TE_BESTWRAP, size=(-1,60),
                                        name = name)
                
                self.ItemsList.append({'labelId' : self.fieldsEditorLabel.GetId(), 'fieldId' : self.fieldsEditor.GetId()})
                                    
                self.fieldsEditor.SetFont(wx.Font(pointSize=11, family=wx.FONTFAMILY_MODERN,
                                        style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_NORMAL))
                self.fieldsEditor.WriteText(field.getValue())
                self.fieldsEditor.SetInsertionPoint(0)
                self.fieldsEditor.Bind(wx.EVT_TEXT, self.onTextChangedInFieldEditor)
                self.FieldsSizer.AddMany([(self.fieldsEditorLabel),(self.fieldsEditor, 1, wx.EXPAND)])            
            self.Layout()
        else:
            newItems = []
            for field in data:
                newItems.append({'label':field.getName().title(), 'text':field.getValue()})
            if len(newItems) <= len(self.ItemsList):
                for itm in range(0,len(newItems)):
                    item = self.ItemsList[itm]
                    widgetLabelId = item['labelId']
                    widgetFieldId = item['fieldId']
                    newItem = newItems[itm]
                    newLabel = newItem['label']
                    newText = newItem['text']
                    self.FindWindow(widgetLabelId).SetLabel(newLabel)
                    self.FindWindow(widgetFieldId).SetName(newLabel)
                    self.FindWindow(widgetFieldId).ChangeValue(newText)

        return True
    
class BibtexTab(EditorFieldsTab):
    """
    Concrete class of the L{EditorFieldsTab}.
    """
    def __init__(self, parent, behavior):
        """
        @see: L{gui.EditorFieldsTab.__init__}.
        """
        super().__init__(parent, behavior)        
        self.name = "BibTeX {}"
        
        self.FieldsSizer = wx.FlexGridSizer(rows=1, cols=1, vgap=0, hgap=0)
        self.FieldsSizer.AddGrowableCol(0, 1)
        self.FieldsSizer.AddGrowableRow(0, 1)
        
        self.fieldsEditor = wx.TextCtrl(self, wx.NewId(),
                            style=wx.TE_MULTILINE | wx.TE_BESTWRAP | wx.HSCROLL)
        self.fieldsEditor.SetFont(wx.Font(pointSize=11, family=wx.FONTFAMILY_MODERN,
                                style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_NORMAL))
        self.fieldsEditor.Bind(wx.EVT_TEXT, self.onTextChangedInBibtexEditor)
        self.FieldsSizer.Add(self.fieldsEditor, 1, wx.EXPAND)
        
        self.SetSizerAndFit(self.FieldsSizer, deleteOld=False)
        
    def setFields(self, data):
        """
        @see: L{gui.EditorFieldsTab.setFields}.
        """
        self.fieldsEditor.Clear() 
        self.fieldsEditor.WriteText(data)
        return True
        
    def ClearTab(self):
        """
        Delete text in editor
        """
        self.fieldsEditor.Clear()
        return True
        
    def WriteData(self, data):
        """
        Replace old text with new text from data in editor
        
        @param data: The new text
        @type data: L{str}
        """
        self.fieldsEditor.Clear()
        self.fieldsEditor.WriteText(data)
        self.fieldsEditor.SetInsertionPoint(0)  # set cursor at the beginning of the text
        
    def GetFieldValue(self):
        """
        Get the BiBtex string in the editor
        
        @rtype: L{str}
        @return: The BibTex string
        """
        return self.fieldsEditor.GetValue()
    
    def SelectAll(self):
        self.fieldsEditor.SelectAll()
        
class EntryEditor(EntryWidget):
    """
    The editor of a reference.
    @group Events: __on*
    @sort: __*, c*, d*, e*, s*
    """
    def __init__(self, parent, behavior):
        """
        @type parent: C{wx.Window}
        @param parent: The parent window. Must be not C{None}.
        @type behavior: L{controller.Controller}
        @param behavior: The statechart controller that defines the behavior
        """
        super(EntryEditor, self).__init__(3, 1, behavior)
        self.title = wx.StaticText(parent, wx.NewId(), 'Edit fields')
        self.tabs = wx.Notebook(parent, style=wx.NB_TOP)
        
        self.requiredFields = RequiredFields(self.tabs, behavior)
        self.tabs.InsertPage(0, self.requiredFields, self.requiredFields.getName(), True)
        
        self.optionalFields = OptionalFileds(self.tabs, behavior)
        self.tabs.InsertPage(1, self.optionalFields, self.optionalFields.getName(), True)
        
        self.additionalFields = AdditionalFields(self.tabs, behavior)
        self.tabs.InsertPage(2, self.additionalFields, self.additionalFields.getName(), True)
        
        self.bibtexTab = BibtexTab(self.tabs, behavior)        
        self.tabs.InsertPage(3, self.bibtexTab, self.bibtexTab.getName(), True)
        
        self.updateButton = wx.Button(parent, wx.NewId(), 'Update')
        self.updateButton.Disable()
        self.updateButton.Bind(wx.EVT_BUTTON, self.__onUpdateButtonClick)
        
        updateButtonSizer = wx.BoxSizer(wx.HORIZONTAL)
        updateButtonSizer.Add((0, 0), 1, wx.EXPAND)
        updateButtonSizer.Add(self.updateButton)
        
        self.sizer.AddGrowableCol(0, 1)
        self.sizer.AddGrowableRow(1, 1)
        self.sizer.Add(self.title)
        self.sizer.Add(self.tabs, 1, wx.EXPAND)
        self.sizer.Add(updateButtonSizer, 1, wx.EXPAND)
    
    def getBibtexTab(self):
        """
        @rtype: L{EditorFieldsTab}
        @return: The required fields of the selected entry
        """
        return self.bibtexTab
       
    def getRequiredFields(self):
        """
        @rtype: L{EditorFieldsTab}
        @return: The required fields of the selected entry
        """
        return self.requiredFields
    
    def getOptionalFields(self):
        """
        @rtype: L{EditorFieldsTab}
        @return: The optional fields of the selected entry
        """
        return self.optionalFields
    
    def getAdditionalFields(self):
        """
        @rtype: L{EditorFieldsTab}
        @return: The additional fields of the selected entry
        """
        return self.additionalFields
        
    def __onUpdateButtonClick(self, e):
        """
        Triggered when the Update button is clicked.
        @type e: C{wx.CommandEvent}
        """
        self.behavior.updateButtonClicked(self.bibtexTab.GetFieldValue())
    
    def enableUpdateButton(self):
        """
        Enable the Update button.
        """
        self.updateButton.Enable(True)
        return True
    
    def disableUpdateButton(self):
        """
        Disable the Update button.
        """
        self.updateButton.Enable(False)
        return True
    
    def clear(self, flag):
        """
        Remove all the text from the editor and the panels from tab fields.
        @param entrySelected: The entry previous selected
        @type L{int}: The id
        """
        if flag >= 0:
            self.bibtexTab.ClearTab()
            
            self.requiredFields.DestroyChildren()
            self.getRequiredFields().resetItemsList()
            
            self.optionalFields.DestroyChildren()
            self.getOptionalFields().resetItemsList()
            
            self.additionalFields.DestroyChildren()
            self.getAdditionalFields().resetItemsList()
            
        else:
            self.bibtexTab.ClearTab()
        return True
    
    def clearBibtexEditor(self):
        """
        Remove the text from the bibtex editor.
        """
        self.bibtexTab.ClearTab()
        return True
    
    def setBibtex(self, data):
        """
        Replace text in the BibTeX editor with C{data}.
        @type data: L{str}
        @param data: The text to write.
        """       
        self.bibtexTab.WriteData(data)        
        return True

class EntryPreviewer(EntryWidget):
    """
    The editor of a reference.
    """
    def __init__(self, parent):
        """
        @type parent: C{wx.Window}
        @param parent: The parent window. Must be not C{None}.
        """
        super(EntryPreviewer, self).__init__(2, 1, behavior=None)
        self.title = wx.StaticText(parent, wx.NewId(), 'Preview reference')
        self.htmlPreviewer = wxHTML.HtmlWindow(parent, style=wxHTML.HW_SCROLLBAR_NEVER)
        
        self.sizer = wx.FlexGridSizer(rows=2, cols=1, vgap=0, hgap=0)
        self.sizer.AddGrowableCol(0, 1)
        self.sizer.AddGrowableRow(1, 1)
        self.sizer.Add(self.title)
        self.sizer.Add(self.htmlPreviewer, 1, wx.EXPAND)
    
    def clear(self):
        """
        Remove all content.
        """
        self.htmlPreviewer.SetPage('')
        return True
    
    def display(self, content):
        """
        Display the content.
        @type content: L{str}
        @param content: The HTML text to display.
        """
        self.htmlPreviewer.SetPage(content)
        return True

class HTMLDialog(wx.Dialog):
    """
    A dialog displaying HTML content.
    """
    def __init__(self, parent, title, source, size=(420, 200)):
        """
        @type parent: C{wx.Window}
        @param parent: The parent window.
        @type title: C{str}
        @param title: The title of the dialog.
        @type source: C{str}
        @param source: The path to the source of the HTML.
        @type size: C{tuple}
        @param size: The width and height of the dialog.
        """
        super(HTMLDialog, self).__init__(parent, wx.NewId(), title,
                           style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.TAB_TRAVERSAL)
        # wx.THICK_FRAME | style is not recognized
        hwin = wxHTML.HtmlWindow(self, wx.NewId(), size=size)
        hwin.LoadPage(source)
        irep = hwin.GetInternalRepresentation()
        hwin.SetSize((irep.GetWidth() + 25, irep.GetHeight() + 10))
        self.SetClientSize(hwin.GetSize())
        self.CentreOnParent(wx.BOTH)
        self.SetFocus()

class HTMLWindow(wx.Frame):
    """
    A window displaying HTML content.
    """
    def __init__(self, parent, title, source):
        """
        @type parent: C{wx.Window}
        @param parent: The parent window.
        @type title: C{str}
        @param title: The title of the dialog.
        @type source: C{str}
        @param source: The path to the source of the HTML.
        """
        super(HTMLWindow, self).__init__(parent, wx.NewId(), title=title)
        
        self.content = wxHTML.HtmlWindow(self, wx.NewId())
        self.content.LoadPage(source)
        self.Bind(wxHTML.EVT_HTML_LINK_CLICKED, self.__onLink)
    
    def __onLink(self, link):
        href = link.GetLinkInfo().GetHref()
        if href.startswith('http') or href.startswith('mailto'):
            self.GetParent().openURL(href)
        elif href == 'docs':
            self.GetParent().openURL(resMgr.docsHTMLPath)
        
    

class ActionCancelDialog(wx.Dialog):
    """
    A generic dialog with one customizable action button and one cancel button.
    The L{performAction} method can be overridden to customize the action of the action button.
    @group Events: __on*
    @sort: __*, g*, p*, s*
    """
    def __init__(self, parent, title, actionButtonLabel='OK'):
        """
        @type parent: C{wx.Window}
        @param parent: The parent window.
        """
        super(ActionCancelDialog, self).__init__(parent, wx.NewId(), title=title,
                           style=wx.DEFAULT_DIALOG_STYLE | wx.STAY_ON_TOP)
        self.panel = wx.Panel(self, wx.NewId())
        self.actionButton = wx.Button(self.panel, id=wx.ID_APPLY, label=actionButtonLabel)
        self.actionButton.Bind(wx.EVT_BUTTON, self.__onActionButtonClicked)
        self.cancelButton = wx.Button(self.panel, id=wx.ID_CANCEL, label="Cancel")
        self.cancelButton.Bind(wx.EVT_BUTTON, self.__onCancelClicked)
        self.SetEscapeId(wx.ID_CANCEL)
        self.__isSizerSet = False
    
    def setSizer(self, sizer):
        """
        Set the sizer that goes on top of the buttons.
        @type sizer: C{wx.Sizer}
        @param sizer: The sizer
        """
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        bottomSizer = wx.BoxSizer(wx.HORIZONTAL)
        bottomSizer.Add(self.actionButton, 0, wx.ALL, 5)
        bottomSizer.Add(self.cancelButton, 0, wx.ALL, 5)
        mainSizer.Add(sizer, 0, wx.EXPAND)
        mainSizer.Add(bottomSizer, 0, wx.EXPAND)
        self.panel.SetSizerAndFit(mainSizer)
        self.SetClientSize(self.panel.GetSize())
        self.__isSizerSet = True
    
    def ShowModal(self):
        """
        @raise Exception: If L{setSizer} was not called before.
        """
        if self.__isSizerSet:
            return wx.Dialog.ShowModal(self)
        else:
            raise Exception('setSizer must be called before ShowModal')
    
    def getPanel(self):
        """
        @return: The main panel of the dialog.
        @rtype: C{wx.Panel}
        """
        return self.panel
    
    def __onActionButtonClicked(self, e):
        """
        Triggered when the action button is clicked.
        @type e: C{wx.CommandEvent}
        """
        self.performAction(e)
        self.EndModal(wx.ID_OK)
    
    def __onCancelClicked(self, e):
        """
        Triggered when Cancel is clicked.
        @type e: C{wx.CommandEvent}
        """
        self.EndModal(wx.ID_CANCEL)
    
    def performAction(self, e):
        """
        Abstract method that performs the action.
        """
        pass
        
class PreferencesDialog(ActionCancelDialog):
    """
    The Preferences dialog.
    It allows to change the preferences of the tool.
    @group Events: __on*
    @sort: __*
    """
    def __init__(self, parent):
        """
        @type parent: C{wx.Window}
        @param parent: The parent window.
        """
        super(PreferencesDialog, self).__init__(parent, title="Preferences")
        
        styleLabel = wx.StaticText(self.panel, wx.NewId(), 'Bibliography style:')
        self.styleCombo = wx.ComboBox(self.panel, wx.NewId(), choices=BibStyle.getAllStyles(), style=wx.CB_READONLY)
        self.styleCombo.SetValue(prefs.bibStyle)
        
        validationLabel = wx.StaticText(self.panel, wx.NewId(), 'Allow invalid entries:')
        self.validation = wx.CheckBox(self.panel, style=wx.CB_SIMPLE)
        self.validation.SetValue(prefs.allowInvalidEntries)
        
        stdFieldsLabel = wx.StaticText(self.panel, wx.NewId(), 'Allow non-standard fields:')
        self.stdFields = wx.CheckBox(self.panel, style=wx.CB_SIMPLE)
        self.stdFields.SetValue(prefs.allowNonStandardFields)
        
        keyGenLabel = wx.StaticText(self.panel, wx.NewId(), 'Override key generation:')
        self.keyGen = wx.CheckBox(self.panel, style=wx.CB_SIMPLE)
        self.keyGen.SetValue(prefs.overrideKeyGeneration)
        
        stdSearchLabel = wx.StaticText(self.panel, wx.NewId(), 'Search query as regular expression:')
        self.stdSearch = wx.CheckBox(self.panel, style=wx.CB_SIMPLE)
        self.stdSearch.SetValue(prefs.searchRegex)

        sizer = wx.BoxSizer(wx.VERTICAL)
        styleSizer = wx.BoxSizer(wx.HORIZONTAL)
        styleSizer.Add(styleLabel, 0, wx.ALL, 5)
        styleSizer.Add(self.styleCombo, 0, wx.ALL, 5)
        validateSizer = wx.BoxSizer(wx.HORIZONTAL)
        validateSizer.Add(validationLabel, 0, wx.ALL, 5)
        validateSizer.Add(self.validation, 0, wx.ALL, 5)
        stdFieldsSizer = wx.BoxSizer(wx.HORIZONTAL)
        stdFieldsSizer.Add(stdFieldsLabel, 0, wx.ALL, 5)
        stdFieldsSizer.Add(self.stdFields, 0, wx.ALL, 5)
        keyGenSizer = wx.BoxSizer(wx.HORIZONTAL)
        keyGenSizer.Add(keyGenLabel, 0, wx.ALL, 5)
        keyGenSizer.Add(self.keyGen, 0, wx.ALL, 5)
        stdSearchSizer = wx.BoxSizer(wx.HORIZONTAL)
        stdSearchSizer.Add(stdSearchLabel, 0, wx.ALL, 5)
        stdSearchSizer.Add(self.stdSearch, 0, wx.ALL, 5)
        sizer.Add(styleSizer, 0, wx.ALL)
        sizer.Add(validateSizer, 0, wx.ALL)
        sizer.Add(stdFieldsSizer, 0, wx.ALL)
        sizer.Add(keyGenSizer, 0, wx.ALL)
        sizer.Add(stdSearchSizer, 0, wx.ALL)
        self.setSizer(sizer)
    
    def performAction(self, e):
        """
        Triggered when OK is clicked.
        Stores the preferences in L{prefs}
        @type e: C{wx.CommandEvent}
        """
        selection = self.styleCombo.GetSelection()
        if selection != wx.NOT_FOUND:
            prefs.bibStyle = BibStyle.getAllStyles()[selection]
        prefs.allowInvalidEntries = self.validation.GetValue()
        prefs.allowNonStandardFields = self.stdFields.GetValue()
        prefs.overrideKeyGeneration = self.keyGen.GetValue()
        prefs.searchRegex = self.stdSearch.GetValue()

class SearchDialog(ActionCancelDialog):
    """
    The Search dialog.
    It allows to search for a query in the list of entries.
    @group Events: __on*
    @sort: __*, g*
    """
    def __init__(self, parent):
        """
        @type parent: C{wx.Window}
        @param parent: The parent window.
        """
        super(SearchDialog, self).__init__(parent, title="Search", actionButtonLabel="Filter")
        
        searchLabel = wx.StaticText(self.panel, wx.NewId(), 'Query:')
        self.query = wx.TextCtrl(self.panel, wx.NewId(), size=(200, -1))
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(searchLabel, 0, wx.ALL, 5)
        sizer.Add(self.query, 0, wx.ALL, 5)
        self.setSizer(sizer)
        self.query.SetFocus()

    def getSearchQuery(self):
        """
        Get the query entered.
        """
        return self.query.GetValue()

class AddNewEntry(wx.Dialog):
    """
    The add new entry dialog.
    It allows to create a new entrie of a specified type or an empty entry.
    """
    def __init__(self, parent):
        super(AddNewEntry,self).__init__(parent, id=wx.NewId(), title = "Select entry type", pos=(100,300), size=(300,300))
        self.initUI()
        
    def initUI(self):
        self.entry=""
        entryTypes = EntryType.getAllEntryTypes()
        
        dialogSizer = wx.BoxSizer(wx.VERTICAL)
        
        self.RadioBoxes = wx.RadioBox(self, id=wx.NewId(), label='BiBteX', size=(280,-1), choices = entryTypes, majorDimension=8, style=wx.RA_SPECIFY_ROWS)
        
        self.ctrlPanel = wx.Panel(self)
        self.panelSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.createButton = wx.Button(self.ctrlPanel, label='Create')        
        self.createButton.Bind(wx.EVT_BUTTON, self.onCreateClicked)        
        self.cancelButton = wx.Button(self.ctrlPanel, label='Cancel')
        self.cancelButton.Bind(wx.EVT_BUTTON, self.onCancelClicked)
        self.panelSizer.Add(self.createButton, 0, wx.ALIGN_LEFT)
        self.panelSizer.AddSpacer(100)
        self.panelSizer.Add(self.cancelButton, 0, wx.ALIGN_RIGHT)
        self.ctrlPanel.SetSizerAndFit(self.panelSizer, deleteOld=True)
        
        dialogSizer.Add(self.RadioBoxes, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        #dialogSizer.AddSpacer(15)
        dialogSizer.Add(self.ctrlPanel, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        self.SetSizer(dialogSizer, deleteOld=True)
        
        self.Centre()
    def onCreateClicked(self, e):
        self.entry = self.RadioBoxes.GetStringSelection()
        self.Destroy()
        
    def onCancelClicked(self, e):
        self.Close() 
        
    def getEntryType(self):
        """
        Get the entry type to add
        
        @rtype: L{str}
        @return: The type of entry to add
        """
        return self.entry
        
class BiBlerGUI(wx.Frame):
    """
    Main window of the application.
    @group Events: __on*
    @sort: __*, a*, c*, d*, e*, h*, i*, o*, p*, r*, s*, u*
    """
    def __init__(self, behavior, maximize=False):
        """
        @type behavior: controller.Controller
        @param behavior: The statechart controller that defines the behavior of this window
        """
        super(BiBlerGUI, self).__init__(None, wx.NewId())        
        # The statechart behavior
        self.behavior = behavior
        # The icon and title of the window
        self.SetTitle("BiBler - the simple bibliography management tool")
        self.SetIcon(wx.Icon(resMgr.getIconPath(), wx.BITMAP_TYPE_ICO))
        # A status bar at the bottom of the window
        self.statusBar = self.CreateStatusBar()
        self.statusBar.SetFieldsCount(2)
        self.SetStatusWidths([-1, 70])
        self.updateStatusBarTotal(0)
        # A panel to hold all the controls
        panel = wx.Panel(self, wx.NewId())
        # In case the 'X' is clicked
        self.Bind(wx.EVT_CLOSE, self.__onExit)
        
        #####################
        # Create the menu bar
        #####################
        fileMenu = wx.Menu()
        menuOpen = fileMenu.Append(wx.ID_OPEN, "&Open\tCtrl+O"," Open a BibTeX file")
        menuSave = fileMenu.Append(wx.ID_SAVE,"&Save\tCtrl+S"," Save the database")
        menuSaveAs = fileMenu.Append(wx.ID_SAVEAS,"Save as"," Save the database to a BibTeX file")
        fileMenu.AppendSeparator()
        menuImport = fileMenu.Append(wx.NewId(), "&Import from file\tCtrl+I"," Import database from a file")
        menuExport = fileMenu.Append(wx.NewId(),"&Export to file\tCtrl+E"," Export database to a file")
        fileMenu.AppendSeparator()
        menuExit = fileMenu.Append(wx.ID_EXIT,"E&xit\tAlt+F4"," Terminate the program")
        
        editMenu = wx.Menu()
        menuUndo = editMenu.Append(wx.ID_UNDO, "&Undo"," Undo the last action, to undo the text the editor use Ctrl+Z")
        menuSelectAll = editMenu.Append(wx.ID_SELECTALL, 'Select all text\tCtrl+A', 'Select the entire text in the editor')
        menuUndo.Enable(False)
        editMenu.AppendSeparator()
        menuSearch = editMenu.Append(wx.ID_FIND, "&Filter\tCtrl+F"," Search and filter the list with entries matching a query")
        menuClearFilter = editMenu.Append(wx.ID_CLEAR, "Clear filter\tCtrl+Shift+F"," Clear the search results and display the complete list")
        menuClearFilter.Enable(False)
        editMenu.AppendSeparator()
        menuPreferences = editMenu.Append(wx.ID_PREFERENCES,"&Preferences\tCtrl+P"," Manage settings and preferences")
        
        referenceMenu = wx.Menu()
        menuAdd = referenceMenu.Append(wx.ID_ADD,"&Add new\tIns"," Add a reference")
        menuDelete = referenceMenu.Append(wx.ID_DELETE,"&Delete\tDel"," Remove a reference")
        menuDelete.Enable(False)
        menuDuplicate = referenceMenu.Append(wx.ID_DUPLICATE, "&Duplicate\tCtrl+D"," Duplicate the selected reference")
        menuDuplicate.Enable(False)
        referenceMenu.AppendSeparator()
        menuGenKeys = referenceMenu.Append(wx.ID_MORE, "&Generate all keys"," Generate a key for all entries")
        menuValidate = referenceMenu.Append(wx.ID_INFO, "&Validate all"," Validate all entries")
        
        helpMenu = wx.Menu()
        menuManual = helpMenu.Append(wx.ID_HELP,"User &manual"," The user manual")
        helpMenu.AppendSeparator()
        menuAbout = helpMenu.Append(wx.ID_ABOUT, "About &BiBler"," Information about this program")

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu,"&File")
        menuBar.Append(editMenu,"&Edit")
        menuBar.Append(referenceMenu,"&Reference")
        menuBar.Append(helpMenu,"&Help")
        self.SetMenuBar(menuBar)
        
        self.Bind(wx.EVT_MENU, self.__onOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.__onSave, menuSave)
        self.Bind(wx.EVT_MENU, self.__onSaveAs, menuSaveAs)
        self.Bind(wx.EVT_MENU, self.__onImport, menuImport)
        self.Bind(wx.EVT_MENU, self.__onExport, menuExport)
        self.Bind(wx.EVT_MENU, self.__onExit, menuExit)
        self.Bind(wx.EVT_MENU, self.__onUndo, menuUndo)
        self.Bind(wx.EVT_MENU, self.__onSearch, menuSearch)
        self.Bind(wx.EVT_MENU, self.__onClearFilter, menuClearFilter)
        self.Bind(wx.EVT_MENU, self.__onPreferences, menuPreferences)
        self.Bind(wx.EVT_MENU, self.__onSelectAll, menuSelectAll)
        self.Bind(wx.EVT_MENU, self.__onAdd, menuAdd)
        self.Bind(wx.EVT_MENU, self.__onDelete, menuDelete)
        self.Bind(wx.EVT_MENU, self.__onDuplicate, menuDuplicate)
        self.Bind(wx.EVT_MENU, self.__onGenKeys, menuGenKeys)
        self.Bind(wx.EVT_MENU, self.__onValidate, menuValidate)
        self.Bind(wx.EVT_MENU, self.__onManual, menuManual)
        self.Bind(wx.EVT_MENU, self.__onAbout, menuAbout)
        
        #####################
        # Create the widgets
        #####################
        self.entryList = EntryList(panel, self.behavior)
        self.editor = EntryEditor(panel, self.behavior)
        self.previewer = EntryPreviewer(panel)    
                
        #####################
        # Layout the controls
        #####################
        mainSizer = wx.FlexGridSizer(rows=3, cols=1, vgap=5, hgap=5)
        mainSizer.AddGrowableCol(0, 1)
        mainSizer.AddGrowableRow(0, 5)
        mainSizer.AddGrowableRow(2, 9)
        bottomSizer = wx.FlexGridSizer(rows=1, cols=5, vgap=5, hgap=5)
        bottomSizer.AddGrowableCol(1, 2)
        bottomSizer.AddGrowableCol(3, 1)
        bottomSizer.AddGrowableRow(0, 1)
        bottomSizer.AddSpacer(5)
        bottomSizer.Add(self.editor.getSizer(), 1, wx.EXPAND)
        bottomSizer.AddSpacer(5)
        bottomSizer.Add(self.previewer.getSizer(), 1, wx.EXPAND)
        bottomSizer.AddSpacer(5)
        mainSizer.Add(self.entryList, 1, wx.EXPAND)
        mainSizer.AddSpacer(5)
        mainSizer.Add(bottomSizer, 1, wx.EXPAND)
        panel.SetSizerAndFit(mainSizer)
        mainSizer.Fit(self)
        
        if maximize:
            self.Maximize()
        
    def __onOpen(self, e):
        """
        Triggered when File>Open is clicked.
        @type e: C{wx.CommandEvent}
        """
        self.behavior.openClicked()
        
    def __onSave(self, e):
        """
        Triggered when File>Save is clicked.
        @type e: C{wx.CommandEvent}
        """
        self.behavior.saveClicked(settings.ExportFormat.BIBTEX)
        
    def __onSaveAs(self, e):
        """
        Triggered when File>Save As is clicked.
        @type e: C{wx.CommandEvent}
        """
        self.behavior.saveAsClicked()
        
    def __onImport(self, e):
        """
        Triggered when File>Import is clicked.
        @type e: C{wx.CommandEvent}
        """
        self.behavior.importClicked()
        
    def __onExport(self, e):
        """
        Triggered when File>Export is clicked.
        @type e: C{wx.CommandEvent}
        """
        self.behavior.exportClicked()

    def __onExit(self, e):
        """
        Triggered when File>Exit or the 'X' at the top right of the window is clicked.
        @type e: C{wx.CommandEvent}
        """
        self.behavior.exitClicked()
    
    def __onUndo(self, e):
        """
        Triggered when Edit>Undo is clicked.
        @type e: C{wx.CommandEvent}
        """
        self.behavior.undoClicked()
        
    def __onSearch(self, e):
        """
        Triggered when Edit>Search is clicked.
        @type e: C{wx.CommandEvent}
        """
        self.behavior.searchClicked()
    
    def __onClearFilter(self, e):
        """
        Triggered when Edit>Clear Filter is clicked.
        @type e: C{wx.CommandEvent}
        """
        self.behavior.clearFilterClicked()
        
    def __onPreferences(self, e):
        """
        Triggered when Edit>Preferences is clicked.
        @type e: C{wx.CommandEvent}
        """
        self.behavior.preferencesClicked()
    
    def __onSelectAll(self, e):
        self.editor.getBibtexTab().SelectAll()
        
    def __onAdd(self, e):
        """
        Triggered when Reference>Add is clicked.
        @type e: C{wx.CommandEvent}
        """
        self.behavior.addClicked()
        
    def __onDelete(self, e):
        """
        Triggered when Reference>Delete is clicked.
        @type e: C{wx.CommandEvent}
        """
        self.behavior.deleteClicked()
        
    def __onDuplicate(self, e):
        """
        Triggered when Reference>Duplicate is clicked.
        @type e: C{wx.CommandEvent}
        """
        self.behavior.duplicateClicked()
        
    def __onGenKeys(self, e):
        """
        Triggered when Reference>Generate all keys is clicked.
        @type e: C{wx.CommandEvent}
        """
        self.behavior.genKeysClicked()
        
    def __onValidate(self, e):
        """
        Triggered when Reference>Validate is clicked.
        @type e: C{wx.CommandEvent}
        """
        self.behavior.validateAllClicked()
        
    def __onManual(self, e):
        """
        Triggered when Help>User Manual is clicked.
        @type e: C{wx.CommandEvent}
        """
        self.behavior.manualClicked()
        
    def __onAbout(self, e):
        """
        Triggered when Help>About BiBler is clicked.
        @type e: C{wx.CommandEvent}
        """
        self.behavior.aboutClicked()
    
    def start(self):
        """
        Launch the window.
        """
        self.Show(True)
    
    def exit(self):
        """
        Close the window.
        """
        self.Destroy()
    
    def hasUnsavedModifications(self):
        """
        Check of there is a C{*} at the end of the title in the title bar. 
        """
        return self.GetTitle()[-1] == '*'
    
    def setDirtyTitle(self):
        """
        Place a C{*} at the end of the title in the title bar. 
        """
        title = self.GetTitle()
        if title[-1] != '*':
            self.SetTitle(title + '*')
        return True
    
    def unsetDirtyTitle(self):
        """
        Remove the C{*} from the title in the title bar. 
        """
        title = self.GetTitle()
        if title[-1] == '*':
            self.SetTitle(title[:-1])
        return True
    
    def displayEntries(self, entryList):
        """
        Show the entries in the entry list.
        @type entryList: L{list} of L{EntryDict}
        @param entryList: The list of entries to show.
        """
        return self.entryList.displayEntries(entryList)
    
    def updateSelectedEntryRow(self, entryDict):
        """
        @see: L{EntryList.updateSelectedEntryRow}.
        """
        self.statusBar.SetStatusText(entryDict[EntryListColumn.Message])
        return self.entryList.updateSelectedEntryRow(entryDict)
    
    def addNewEntryRow(self, entryDict):
        """
        @see: L{EntryList.addEntryRow}.
        """
        return self.entryList.addEntryRow(entryDict)
    
    def selectEntryRow(self, entryId):
        """
        @see: L{EntryList.selectEntryRow}.
        """
        return self.entryList.selectEntryRow(entryId)
    
    def isEntrySelected(self):
        """
        @see: L{EntryList.isEntrySelected}.
        """
        return self.entryList.isEntrySelected()
    
    def removeEntryRow(self, entryId):
        """
        @see: L{EntryList.removeEntryRow}.
        """
        return self.entryList.removeEntryRow(entryId)
    
    def unselectEntryRow(self):
        """
        @see: L{EntryList.unselectEntryRow}
        """
        return self.entryList.unselectEntryRow()
    
    def clearList(self):
        """
        Delete all rows of the entry list.
        """
        self.entryList.DeleteAllItems()
        return True
    
    def displayBibTexInEditor(self, data):
        """
        @see: L{EntryEditor.setBibtex}.
        """
        return self.editor.getBibtexTab().setFields(data)
    
    def displayRequiredFields(self, data):
        """
        @see: L{EntryEditorTabs.setRequiredFields}.
        """
        return self.editor.getRequiredFields().setFields(data)
    
    def displayOptionalFields(self, data):
        """
        @see: L{EntryEditorTabs.setOptionalields}.
        """
        return self.editor.getOptionalFields().setFields(data)
    
    def displayAdditionalFields(self, data):
        """
        @see: L{EntryEditorTabs.setAdditionalFields}.
        """
        return self.editor.getAdditionalFields().setFields(data)
    
    def clearEditor(self, flag):
        """
        @see: L{EntryEditor.clear}.
        """
        return self.editor.clear(flag)
    
    def clearBibtexEditor(self):
        """
        @see: L{EntryEditor.clearBibtexEditor}.
        """
        return self.editor.clearBibtexEditor()
    
    def clearPreviewer(self):
        """
        @see: L{EntryPreviewer.clear}.
        """
        return self.previewer.clear()
    
    def previewEntry(self, content):
        """
        @see: L{EntryPreviewer.display}.
        """
        return self.previewer.display(content)
    
    def updateStatusBar(self, msg):
        """
        Display a message in the left status bar.
        @type msg: L{str}
        @param msg: The message to display.
        """
        self.statusBar.SetStatusText(msg)
        return True
    
    def clearStatusBar(self):
        """
        Remove any message from the left status bar.
        """
        self.statusBar.SetStatusText('')
        return True
    
    def updateStatusBarTotal(self, total):
        """
        Display the total number of entries in the right status bar.
        @type total: L{int}
        @param total: The total number of entries.
        """
        self.SetStatusText(' Total: %s' % total, 1)
        return True
    
    def enableClearFilter(self):
        """
        Enable the Clear Filter menu.
        """
        self.GetMenuBar().FindItemById(wx.ID_CLEAR).Enable(True)
        return True
    
    def disableClearFilter(self):
        """
        Disable the Clear Filter menu.
        """
        self.GetMenuBar().FindItemById(wx.ID_CLEAR).Enable(False)
        return True
    
    def enableDelete(self):
        """
        Enable the Delete menu.
        """
        self.GetMenuBar().FindItemById(wx.ID_DELETE).Enable(True) #wx.wx.ID_DELETE
        return True
    
    def disableDelete(self):
        """
        Disable the Delete menu.
        """
        self.GetMenuBar().FindItemById(wx.ID_DELETE).Enable(False)#wx.wx.ID_DELETE
        return True
    
    def enableDuplicate(self):
        """
        Enable the Duplicate menu.
        """
        self.GetMenuBar().FindItemById(wx.ID_DUPLICATE).Enable(True) #wx.wx.ID_DUPLICATE
        return True
    
    def disableDuplicate(self):
        """
        Disable the Duplicate menu.
        """
        self.GetMenuBar().FindItemById(wx.ID_DUPLICATE).Enable(False) #wx.wx.ID_DUPLICATE
        return True
    
    def enableUndo(self):
        """
        Enable the Undo menu.
        """
        self.GetMenuBar().FindItemById(wx.ID_UNDO).Enable(True) #wx.wx.ID_UNDO
        return True
    
    def disableUndo(self):
        """
        Disable the Undo menu.
        """
        self.GetMenuBar().FindItemById(wx.ID_UNDO).Enable(False) #(wx.wx.ID_UNDO
        return True
    
    def enableUpdateButton(self):
        """
        Enable the Update button.
        """
        return self.editor.enableUpdateButton()
    
    def disableUpdateButton(self):
        """
        Disable the Update button.
        """
        return self.editor.disableUpdateButton()
    
    def popupOpenDialog(self):
        """
        Open a dialog to select a BibTeX file to open.
        The title of the window will reflect the path to the file.
        """
        dlg = wx.FileDialog(self, message="Open a bibliography file",
                            wildcard="BibTeX (*.bib)|*.bib|EndNote file (*.bib)|*.bib",
                            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            _format = None
            flt = dlg.GetFilterIndex()
            if flt == 0:
                _format = settings.ImportFormat.BIBTEX
            elif flt == 1:
                _format = settings.ImportFormat.ENDNOTE
            self.behavior.openFileSelected(dlg.GetPath(), _format)
        else:
            self.behavior.cancelClicked()
        dlg.Destroy()
    
    def popupSaveDialog(self):
        """
        Open a dialog to select a BibTeX file to save to.
        The title of the window will reflect the path to the file.
        """
        dlg = wx.FileDialog(self, message="Save the bibliography to a file",
                            wildcard="BibTeX (*.bib)|*.bib",
                            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.behavior.saveFileSelected(path, settings.ExportFormat.BIBTEX)
            self.SetTitle('BiBler - ' + path)
            prefs.defaultDir = path
        else:
            self.behavior.cancelClicked()
        dlg.Destroy()
    
    def popupImportDialog(self):
        """
        Open a dialog to select a CSV file to import from.
        """
        dlg = wx.FileDialog(self, message="Import a bibliography file",
                            wildcard="BibTeX (*.bib)|*.bib|Comma-Separated Values (*.csv)|*.csv|EndNote file (*.bib)|*.bib",
                            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            _format = None
            flt = dlg.GetFilterIndex()
            if flt == 0:
                _format = settings.ImportFormat.BIBTEX
            elif flt == 1:
                _format = settings.ImportFormat.CSV
            elif flt == 2:
                _format = settings.ImportFormat.ENDNOTE
            self.behavior.importFileSelected(dlg.GetPath(), _format)
        else:
            self.behavior.cancelClicked()
        dlg.Destroy()
    
    def popupExportDialog(self):
        """
        Open a dialog to select an HTML or CSV file to export to.
        """
        dlg = wx.FileDialog(self, message="Export to a file",
                            wildcard="Web page (*.html)|*.html|Comma-Separated Values (*.csv)|*.csv|MySQL (*.sql)|*.sql",
                            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            _format = None
            flt = dlg.GetFilterIndex()
            if flt == 0:
                _format = settings.ExportFormat.HTML
            elif flt == 1:
                _format = settings.ExportFormat.CSV
            elif flt == 2:
                _format = settings.ExportFormat.SQL
            wx.BeginBusyCursor()
            busy = wx.BusyInfo("Please wait a few seconds while exporting all entries...")
            wx.Yield()  # not sure if we need this
            self.behavior.exportFileSelected(dlg.GetPath(), _format)
            del busy
            wx.EndBusyCursor()
        else:
            self.behavior.cancelClicked()
        dlg.Destroy()
    
    def popupPreferencesDialog(self):
        """
        Open the preferences dialog.
        @see: L{PreferencesDialog}.
        """
        dlg = PreferencesDialog(self)
        if dlg.ShowModal() == wx.ID_OK:
            self.behavior.preferencesChanged()
        else:
            self.behavior.cancelClicked()
        dlg.Destroy()
    
    def popupSearchDialog(self):
        """
        Open the search dialog.
        @see: L{SearchDialog}.
        """
        dlg = SearchDialog(self)
        if dlg.ShowModal() == wx.ID_OK:
            # Searching is very slow so make sure to inform the user
            wx.BeginBusyCursor()
            busy = wx.BusyInfo("Please wait a few seconds while searching through the whole database...")
            wx.Yield()  # not sure if we need this
            self.behavior.filterClicked(dlg.getSearchQuery())
            del busy
            wx.EndBusyCursor()
        else:
            self.behavior.cancelClicked()
        dlg.Destroy()
        
    def popupAddNewEntryDialog(self):
        """
        Open add new entry dialog.
        @see: L{AddNewEntry}.
        """
        dlg = AddNewEntry(self)
        dlg.ShowModal()
        entry = dlg.getEntryType()
        if entry != "":
            self.behavior.entryTypeSelected(entry)
        else:
            self.behavior.cancelClicked()
        
    
    def popupAboutDialog(self):
        """
        Open the about box.
        @see: L{HTMLDialog}.
        The content of this dialog is contained in L{utils.resourcemgr.ResourceManager.getAboutHTML}
        """
        dlg = HTMLDialog(self, "About BiBler", resMgr.getAboutHTML())
        dlg.ShowModal()
        dlg.Destroy()
        return True
    
    def popupUserManualWindow(self):
        """
        Open the user manual.
        The content of this window is contained in L{utils.resourcemgr.ResourceManager.getUserManualHTML}.
        @see: L{HTMLWindow}.
        """
        win = HTMLWindow(self, "User Manual", resMgr.getUserManualHTML())
        return win.Show(True)
    
    def popupConfirmExitDialog(self):
        """
        Prompt to confirm closing the window.
        """
        dlg = wx.MessageDialog(self, "Do you really want to exit?", "Confirm Exit",
                               wx.OK | wx.CANCEL | wx.ICON_QUESTION)
        if dlg.ShowModal() == wx.ID_OK:
            dlg.Destroy()
            self.behavior.exit()
        else:
            self.behavior.cancelClicked()
    
    def popupPendingChangesOnExitDialog(self):
        """
        Prompt to ask if current bibliography must be saved before exiting.
        """
        dlg = wx.MessageDialog(self, "Do you want to save changes before exiting?", "Pending Changes",
                               wx.YES_NO | wx.ICON_QUESTION)
        if dlg.ShowModal() == wx.ID_YES:
            dlg.Destroy()
            self.behavior.saveClicked(settings.ExportFormat.BIBTEX)
        else:
            self.behavior.forceExitClicked()
    
    def popupValidationResultMessage(self, invalid):
        """
        Display the validation result.
        """
        if invalid > 0:
            msg = 'There are %i invalid entries highlighted in red.' % invalid
            dlg = wx.MessageDialog(self, msg, "Vaidation Result", wx.OK | wx.ICON_WARNING)
        else:
            msg = 'All entries are valid.'
            dlg = wx.MessageDialog(self, msg, "Vaidation Result", wx.OK | wx.ICON_EXCLAMATION)
        dlg.ShowModal()
        dlg.Destroy()
    
    def popupErrorMessage(self, msg):
        """
        Display an error message.
        """
        dlg = wx.MessageDialog(self, msg, "Error", wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()
    
    def openURL(self, url):
        """
        Open a URL in a web browser. Note that local files can be open to.
        """
        wx.BeginBusyCursor()
        url_opened = webbrowser.open(url, new=2)
        wx.EndBusyCursor()
        return url_opened