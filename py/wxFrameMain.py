#-----------------------------------------------------------------------------
#Boa:Frame:wxMainFrame

#-----------------------------------------------------------------------------
# Name:        wxFrameMain.py
# Product:     ClamWin Free Antivirus
#
# Author:      alch [alch at users dot sourceforge dot net]
#
# Created:     2004/19/03
# Copyright:   Copyright alch (c) 2004
# Licence:
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

import sys, os, time
import wx
#import MsgBox, Utils, wxDialogUtils, version

def create(parent, config):
    return wxMainFrame(parent, config)

# All wx constants now need to be prefixed with 'wx.'
[wxID_WXMAINFRAME, wxID_WXMAINFRAMEBUTTONCLOSE, wxID_WXMAINFRAMEBUTTONSCAN,
 wxID_WXMAINFRAMEDIRCTRLSCAN, wxID_WXMAINFRAMEPANELFRAME,
 wxID_WXMAINFRAMESTATIC1, wxID_WXMAINFRAMESTATUSBAR, wxID_WXMAINFRAMETOOLBAR, wxID_WXMAINFRAMETOOLBARTOOLS_SCANMEM
] = [wx.NewIdRef() for _init_ctrls in range(9)]

[wxID_WXMAINFRAMETOOLBARTOOLS_INETUPDATE, wxID_WXMAINFRAMETOOLBARTOOLS_PREFS,
 wxID_WXMAINFRAMETOOLBARTOOLS_SCAN,
] = [wx.NewIdRef() for _init_coll_toolBar_Tools in range(3)]

[wxID_WXMAINFRAMEREPORTSDATABASE, wxID_WXMAINFRAMEREPORTSSCAN,
] = [wx.NewIdRef() for _init_coll_Reports_Items in range(2)]

[wxID_WXMAINFRAMETOOLSDBUPDATE, wxID_WXMAINFRAMETOOLSPREFERENCES,
 wxID_WXMAINFRAMETOOLSREPORTS,
] = [wx.NewIdRef() for _init_coll_Tools_Items in range(3)]

[wxID_WXMAINFRAMEHELPABOUT, wxID_WXMAINFRAMEHELPFAQ, wxID_WXMAINFRAMEHELPUPDATE, wxID_WXMAINFRAMEHELPWEBSITE, wxID_WXMAINFRAMEHELPHELP, wxID_WXMAINFRAMEHELPSUPPORT,
] = [wx.NewIdRef() for _init_coll_Help_Items in range(6)]

[wxID_WXMAINFRAMEFILEITEMS0, wxID_WXMAINFRAMEFILESCAN, wxID_WXMAINFRAMEFILESCANMEM
] = [wx.NewIdRef() for _init_coll_File_Items in range(3)]

class wxMainFrame(wx.Frame):
    def _init_coll_flexGridSizerPanel_Items(self, parent):
        # generated method, don't edit
        parent.Add(8, 8, border=0, flag=0)
        parent.Add(self.static1, 0, border=5,
              flag=wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.ALIGN_LEFT)
        parent.Add(self.dirCtrlScan, 0, border=10,
              flag=wx.LEFT | wx.RIGHT | wx.GROW)

    def _init_coll_flexGridSizerPanel_Growables(self, parent):
        # generated method, don't edit

        parent.AddGrowableRow(2)
        parent.AddGrowableCol(0)

    def _init_coll_gridSizerFrame_Items(self, parent):
        # generated method, don't edit
        parent.Add(self.panelFrame, 0, border=0, flag=wx.GROW)

    def _init_coll_gridSizerButtons_Items(self, parent):
        # generated method, don't edit
        parent.Add(self.buttonScan, 0, border=10,
              flag=wx.ALIGN_RIGHT | wx.ALL)
        parent.Add(self.buttonClose, 0, border=10,
              flag=wx.ALIGN_LEFT | wx.ALL)

    def _init_coll_Tools_Items(self, parent):
        # generated method, don't edit

        parent.Append(id=wxID_WXMAINFRAMETOOLSPREFERENCES, item='&Preferences',
              helpString='Displays the configuration window',
              kind=wx.ITEM_NORMAL)
        parent.Append(id=wxID_WXMAINFRAMETOOLSDBUPDATE,
              item='Download &Virus Database Update',
              helpString='Downloads latest virus database from the Internet',
              kind=wx.ITEM_NORMAL)
        parent.Append(id=wxID_WXMAINFRAMETOOLSREPORTS, item='&Display Reports',
              subMenu=self.Reports,
              helpString='Displays ClamWin Log Files')
        self.Bind(wx.EVT_MENU, self.OnToolsPreferences, id=wxID_WXMAINFRAMETOOLSPREFERENCES)
        self.Bind(wx.EVT_MENU, self.OnToolsUpdate, id=wxID_WXMAINFRAMETOOLSDBUPDATE)

    def _init_coll_menuBar_Menus(self, parent):
        # generated method, don't edit

        parent.Append(menu=self.File, title='&File')
        parent.Append(menu=self.Tools, title='&Tools')
        parent.Append(menu=self.Help, title='&Help')

    def _init_coll_Help_Items(self, parent):
        # generated method, don't edit

        parent.Append(id=wxID_WXMAINFRAMEHELPHELP, item='&Help', helpString='Displays ClamWin Free Antivirus Manual', kind=wx.ITEM_NORMAL)
        parent.Append(id=wxID_WXMAINFRAMEHELPSUPPORT, item='&Technical Support', helpString='Opens Support Forum in the Web Browser', kind=wx.ITEM_NORMAL)
        parent.Append(id=wxID_WXMAINFRAMEHELPUPDATE, item='&Check Latest Version', helpString='Checks for the Latest Version', kind=wx.ITEM_NORMAL)
        parent.Append(id=wxID_WXMAINFRAMEHELPWEBSITE, item='ClamWin &Website', helpString='Opens ClamWin Free Antivirus Website', kind=wx.ITEM_NORMAL)

        parent.Append(id=wxID_WXMAINFRAMEHELPFAQ, item='&FAQ', helpString='Opens Frequently Asked Questions Page in the Web Browser', kind=wx.ITEM_NORMAL)

        parent.AppendSeparator()
        parent.Append(id=wxID_WXMAINFRAMEHELPABOUT, item='&About', helpString='Displays the About Box', kind=wx.ITEM_NORMAL)
        self.Bind(wx.EVT_MENU, self.OnHelpAbout, id=wxID_WXMAINFRAMEHELPABOUT)
        self.Bind(wx.EVT_MENU, self.OnHelpHelp, id=wxID_WXMAINFRAMEHELPHELP)
        self.Bind(wx.EVT_MENU, self.OnHelpSupport, id=wxID_WXMAINFRAMEHELPSUPPORT)
        self.Bind(wx.EVT_MENU, self.OnHelpUpdate, id=wxID_WXMAINFRAMEHELPUPDATE)
        self.Bind(wx.EVT_MENU, self.OnHelpWebsite, id=wxID_WXMAINFRAMEHELPWEBSITE)
        self.Bind(wx.EVT_MENU, self.OnHelpFAQ, id=wxID_WXMAINFRAMEHELPFAQ)

    def _init_coll_Reports_Items(self, parent):
        # generated method, don't edit

        parent.Append(id=wxID_WXMAINFRAMEREPORTSDATABASE,
              item='&Virus Database Update Report',
              helpString='Displays Virus Database Update Log FIle',
              kind=wx.ITEM_NORMAL)
        parent.Append(id=wxID_WXMAINFRAMEREPORTSSCAN, item='&Scan Report',
              helpString='Displays Virus Scan Log File',
              kind=wx.ITEM_NORMAL)
        self.Bind(wx.EVT_MENU, self.OnViewUpdateLog, id=wxID_WXMAINFRAMEREPORTSDATABASE)
        self.Bind(wx.EVT_MENU, self.OnViewScanLog, id=wxID_WXMAINFRAMEREPORTSSCAN)

    def _init_coll_File_Items(self, parent):
        # generated method, don't edit

        parent.Append(id=wxID_WXMAINFRAMEFILESCAN, item='&Scan Files', helpString='Scans Selected Files or Folders for Computer Viruses', kind=wx.ITEM_NORMAL)
        parent.Append(id=wxID_WXMAINFRAMEFILESCANMEM, item='Scan &Memory', helpString='Scans Programs in Computer Memory for Viruses', kind=wx.ITEM_NORMAL)

        parent.AppendSeparator()
        parent.Append(id=wxID_WXMAINFRAMEFILEITEMS0, item='E&xit', helpString='Exits the application', kind=wx.ITEM_NORMAL)
        self.Bind(wx.EVT_MENU, self.OnScanButton, id=wxID_WXMAINFRAMEFILESCAN)
        self.Bind(wx.EVT_MENU, self.OnScanMemButton, id=wxID_WXMAINFRAMEFILESCANMEM)
        self.Bind(wx.EVT_MENU, self.OnFileExit, id=wxID_WXMAINFRAMEFILEITEMS0)

    def _init_coll_toolBar_Tools(self, parent):
        # generated method, don't edit

        parent.AddTool(wxID_WXMAINFRAMETOOLBARTOOLS_PREFS,
                       'Preferences',
                       wx.Bitmap('img/Control.png', wx.BITMAP_TYPE_PNG),
                       wx.NullBitmap, # bmpDisabled
                       wx.ITEM_NORMAL, # kind
                       'Displays Preferences Window', # longHelp
                       'Displays Preferences Window') # shortHelp

        parent.AddTool(wxID_WXMAINFRAMETOOLBARTOOLS_INETUPDATE,
                       'Update',
                       wx.Bitmap('img/World.png', wx.BITMAP_TYPE_PNG),
                       wx.NullBitmap, # bmpDisabled
                       wx.ITEM_NORMAL, # kind
                       'Updates virus databases over the Internet', # longHelp
                       'Starts Internet Update') # shortHelp

        parent.AddSeparator()

        parent.AddTool(wxID_WXMAINFRAMETOOLBARTOOLS_SCANMEM,
                       'Scan Computer Memory',
                       wx.Bitmap('img/ScanMem.png', wx.BITMAP_TYPE_PNG),
                       wx.NullBitmap, # bmpDisabled
                       wx.ITEM_NORMAL, # kind
                       'Scans Programs Loaded in Computer Memory for Computer Viruses', # longHelp
                       'Scans Computer Memory for Viruses') # shortHelp

        parent.AddTool(wxID_WXMAINFRAMETOOLBARTOOLS_SCAN,
                       'Scan Selected Files',
                       wx.Bitmap('img/Scan.png', wx.BITMAP_TYPE_PNG),
                       wx.NullBitmap, # bmpDisabled
                       wx.ITEM_NORMAL, # kind
                       'Scans Selected Files or Folders for Computer Viruses', # longHelp
                       'Scans Selected Files For Viruses') # shortHelp

        self.Bind(wx.EVT_TOOL, self.OnToolsUpdate, id=wxID_WXMAINFRAMETOOLBARTOOLS_INETUPDATE)
        self.Bind(wx.EVT_TOOL, self.OnToolsPreferences, id=wxID_WXMAINFRAMETOOLBARTOOLS_PREFS)
        self.Bind(wx.EVT_TOOL, self.OnScanButton, id=wxID_WXMAINFRAMETOOLBARTOOLS_SCAN)
        self.Bind(wx.EVT_TOOL, self.OnScanMemButton, id=wxID_WXMAINFRAMETOOLBARTOOLS_SCANMEM)

        parent.Realize()

    def _init_sizers(self):
        # generated method, don't edit
        self.gridSizerFrame = wx.GridSizer(cols=1, hgap=0, rows=1, vgap=0)

        self.flexGridSizerPanel = wx.FlexGridSizer(cols=1, hgap=0, rows=4,
              vgap=0)

        self.gridSizerButtons = wx.GridSizer(cols=2, hgap=0, rows=1, vgap=0)

        self._init_coll_gridSizerFrame_Items(self.gridSizerFrame)
        self._init_coll_flexGridSizerPanel_Items(self.flexGridSizerPanel)
        self._init_coll_flexGridSizerPanel_Growables(self.flexGridSizerPanel)
        self._init_coll_gridSizerButtons_Items(self.gridSizerButtons)

        self.SetSizer(self.gridSizerFrame)
        self.panelFrame.SetSizer(self.flexGridSizerPanel)

    def _init_utils(self):
        # generated method, don't edit
        self.menuBar = wx.MenuBar()

        self.File = wx.Menu(title='')

        self.Tools = wx.Menu(title='')

        self.Help = wx.Menu(title='')

        self.Reports = wx.Menu(title='')

        self._init_coll_menuBar_Menus(self.menuBar)
        self._init_coll_File_Items(self.File)
        self._init_coll_Tools_Items(self.Tools)
        self._init_coll_Help_Items(self.Help)
        self._init_coll_Reports_Items(self.Reports)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_WXMAINFRAME, name='wxMainFrame',
              parent=prnt, pos=wx.Point(250, 143), size=wx.Size(568, 430),
              style=wx.DEFAULT_FRAME_STYLE, title='ClamWin Free Antivirus')
        self._init_utils()
        self.SetClientSize(wx.Size(560, 403))
        self.SetMenuBar(self.menuBar)
        self.SetHelpText('ClamWin Free Antivirus')
        self.Center(wx.BOTH)

        self.toolBar = wx.ToolBar(id=wxID_WXMAINFRAMETOOLBAR, name='toolBar',
              parent=self, pos=wx.Point(0, 0), size=wx.Size(560, 41),
              style=wx.TB_FLAT | wx.TB_HORIZONTAL | wx.NO_BORDER)
        self.toolBar.SetToolTip('')
        self.toolBar.SetToolBitmapSize(wx.Size(32, 32))
        self.SetToolBar(self.toolBar)

        self.statusBar = wx.StatusBar(id=wxID_WXMAINFRAMESTATUSBAR,
              name='statusBar', parent=self, style=0)
        self.statusBar.SetSize(wx.Size(537, 20))
        self.statusBar.SetPosition(wx.Point(0, 218))
        self.statusBar.SetToolTip('Status Bar')
        self.SetStatusBar(self.statusBar)

        self.panelFrame = wx.Panel(id=wxID_WXMAINFRAMEPANELFRAME,
              name='panelFrame', parent=self, pos=wx.Point(0, 0),
              size=wx.Size(560, 403), style=wx.TAB_TRAVERSAL)

        self.static1 = wx.StaticText(id=wxID_WXMAINFRAMESTATIC1,
              label='Select a folder or a file to scan\n(Hold Shift key to select multiple files or folders)', name='static1',
              parent=self.panelFrame, pos=wx.Point(5, 8), size=wx.Size(435, 32),
              style=0)

        self.dirCtrlScan = wx.GenericDirCtrl(defaultFilter=0, dir='.', filter='',
              id=wxID_WXMAINFRAMEDIRCTRLSCAN, name='dirCtrlScan',
              parent=self.panelFrame, pos=wx.Point(10, 27), size=wx.Size(540,
              376),
              style=wx.DIRCTRL_SELECT_FIRST | wx.SUNKEN_BORDER | wx.DIRCTRL_3D_INTERNAL)

        self.buttonScan = wx.Button(id=wxID_WXMAINFRAMEBUTTONSCAN, label='&Scan',
              name='buttonScan', parent=self.panelFrame, pos=wx.Point(-85, 10),
              size=wx.Size(75, 23), style=0)
        self.buttonScan.SetDefault()
        self.Bind(wx.EVT_BUTTON, self.OnScanButton, id=wxID_WXMAINFRAMEBUTTONSCAN)

        self.buttonClose = wx.Button(id=wxID_WXMAINFRAMEBUTTONCLOSE,
              label='&Close', name='buttonClose', parent=self.panelFrame,
              pos=wx.Point(10, 10), size=wx.Size(75, 23), style=0)
        self.Bind(wx.EVT_BUTTON, self.OnButtonClose, id=wxID_WXMAINFRAMEBUTTONCLOSE)

        self._init_coll_toolBar_Tools(self.toolBar)

        ##self._init_sizers()

    def __init__(self, parent, config):
        self._config = None
        self._config = config

        self._init_ctrls(parent)

        # select second in the directory tree (usually c:)
        try:
            treeCtrl = self.dirCtrlScan.GetTreeCtrl()
            itemid, cookie = treeCtrl.GetFirstChild(treeCtrl.GetRootItem())
            # Check if there is a next child before trying to get it
            # The original code tries to get the second child by calling GetNextChild on the root item,
            # which is incorrect. GetNextChild takes an item as the first argument, not a root.
            # Assuming the intent was to select the second *child* of the root, or perhaps the second *top-level* item.
            # If the original intent was to select the *second top-level item*,
            # the logic needs to be revised to get the children of the root and iterate.
            # For now, I'll keep the original intent as close as possible to fix the immediate error,
            # which is likely in how GetNextChild was called with 'cookie'.
            # A more robust way to get the second top-level item would be:
            # children = []
            # item, cookie = treeCtrl.GetFirstChild(treeCtrl.GetRootItem())
            # while item.IsOk():
            #     children.append(item)
            #     item, cookie = treeCtrl.GetNextChild(treeCtrl.GetRootItem(), cookie) # This line is also problematic with cookie
            # if len(children) > 1:
            #     itemid = children[1] # Select the second item in the list
            #     cookie = None # Reset cookie as it's not needed for this method
            #
            # Given the original structure, the issue is that GetNextChild expects the *parent item* and a cookie.
            # It's likely trying to get the *next sibling* of the *first child* if 'itemid' was the first child.
            # However, the code passes the root item again.
            # Let's simplify by directly getting the next sibling of the first found item, if that was the intent.
            # If the intent was to find the second direct child of the root:
            if itemid.IsOk():
                next_itemid, next_cookie = treeCtrl.GetNextSibling(itemid)
                if next_itemid.IsOk():
                    itemid = next_itemid
            # select it
            treeCtrl.SetFocus()
            treeCtrl.UnselectAll()
            if itemid.IsOk(): # Ensure itemid is valid before selecting
                treeCtrl.SelectItem(itemid)
        except Exception as e:
            print(f"Error in directory tree selection: {e}")
            pass

        # we need to set controls heights to 0 and reinit sizers
        # to overcome boa sizers bug
        self.dirCtrlScan.SetSize((-1, 0))
        self.panelFrame.SetSize((-1, 0))
        self._init_sizers()
        self.flexGridSizerPanel.Add(self.gridSizerButtons, flag = wx.GROW)

        # set window icons
        icons = wx.IconBundle()
        # Changed AddIconFromFile to AddIcon(wx.Icon(...))
        icons.AddIcon(wx.Icon('img/FrameIcon.ico', wx.BITMAP_TYPE_ICO))
        self.SetIcons(icons)

        if not sys.platform.startswith('win'):
            self.Help.Remove(wxID_WXMAINFRAMEHELPHELP)

        self._UpdateState()


    def OnFileExit(self, event):
        self.Close()

    def OnToolsPreferences(self, event):
        wxDialogUtils.wxConfigure(self, self._config)
        self._UpdateState()

    def OnHelpAbout(self, event):
        wxDialogUtils.wxAbout(self, self._config)

    def _IsConfigured(self):
        if self._config.Get('ClamAV', 'ClamScan') == '' or \
           self._config.Get('ClamAV', 'FreshClam') == '' or \
           self._config.Get('ClamAV', 'Database') == '' :
            return False
        else:
            return True


    def _UpdateState(self):
        try:
            # disable Run Command button if the configuration is invalid
            # or no item is selected in the tree
            configured = self._IsConfigured()
            if not configured:
                if wx.ID_YES == MsgBox.MessageBox(None, 'ClamWin Free Antivirus', 'ClamWin Free Antivirus is not configured. Would you like to configure it now?', wx.YES_NO | wx.ICON_QUESTION):
                    wxDialogUtils.wxConfigure(None, self._config)
                    configured = self._IsConfigured()

            hasdb = Utils.CheckDatabase(self._config)
            if configured and not hasdb:
                if wx.ID_YES == MsgBox.MessageBox(None, 'ClamWin Free Antivirus', 'You have not yet downloaded Virus Definitions Database. Would you like to download it now?', wx.YES_NO | wx.ICON_QUESTION):
                    wxDialogUtils.wxUpdateVirDB(self, self._config)
                    hasdb = Utils.CheckDatabase(self._config)


            self.buttonScan.Enable(configured and hasdb)
            self.toolBar.EnableTool(wxID_WXMAINFRAMETOOLBARTOOLS_INETUPDATE, configured)
            self.toolBar.EnableTool(wxID_WXMAINFRAMETOOLBARTOOLS_SCAN, configured and hasdb)
            self.toolBar.EnableTool(wxID_WXMAINFRAMETOOLBARTOOLS_SCANMEM, configured and hasdb)

            # check if the db is current (not older than 3 days)
            if hasdb:
                dbpath =  self._config.Get('ClamAV', 'Database')
                daily = os.path.join(dbpath, 'daily.cld')
                if not os.path.isfile(daily):
                    daily = os.path.join(dbpath, 'daily.cvd')
                ver, numv, updated = Utils.GetDBInfo(daily)

            # print updated, time.mktime(time.localtime()), time.mktime(time.localtime()) - updated
            if hasdb and self._config.Get('Updates', 'WarnOutOfDate') == '1' and (time.mktime(time.localtime()) - updated > 86400*5):
                if wx.ID_YES == MsgBox.MessageBox(None, 'ClamWin Free Antivirus', 'Virus signature database is older than 5 days and may not offer the latest protection. Would you like to update it now?', wx.YES_NO | wx.ICON_QUESTION):
                    wxDialogUtils.wxUpdateVirDB(self, self._config)
                    hasdb = Utils.CheckDatabase(self._config)

        except Exception as e:
            print('An Error occured while updating UI selection. %s' % str(e))

    def OnScanButton(self, event):
        scanPath = ''
        for path in self.dirCtrlScan.GetMultiplePath():
            scanPath += "\"%s\" " % path
        wxDialogUtils.wxScan(self, self._config, scanPath)

    def OnScanMemButton(self, event):
        wxDialogUtils.wxScan(self, self._config, None)

    def OnToolsUpdate(self, event):
        wxDialogUtils.wxUpdateVirDB(self, self._config)
        self._UpdateState()

    def OnButtonClose(self, event):
        self.Close()

    def OnViewUpdateLog(self, event):
        wxDialogUtils.wxShowLog(self, self._config.Get('Updates', 'DBUpdateLogFile'))

    def OnViewScanLog(self, event):
        wxDialogUtils.wxShowLog(self, self._config.Get('ClamAV', 'LogFile'))

    def OnHelpHelp(self, event):
        if sys.platform.startswith('win'):
            import win32api, win32con
            curDir = Utils.GetCurrentDir(True)
            helpfile = os.path.join(curDir, 'manual.chm')
            if not os.path.isfile(helpfile):
                MsgBox.ErrorBox(self, 'Could not open help file - %s not found.' % helpfile)
            else:
                try:
                    win32api.ShellExecute(self.GetHandle(), 'open',
                        helpfile,
                        None, curDir, win32con.SW_SHOWNORMAL)
                except Exception as e:
                    MsgBox.ErrorBox(self, 'Could not open help file. Please ensure that you have Adobe Acrobat Reader installed.')

    def OnHelpFAQ(self, event):
        wxDialogUtils.wxGoToInternetUrl('http://www.clamwin.com/content/category/3/7/27/')

    def OnHelpSupport(self, event):
        wxDialogUtils.wxGoToInternetUrl('http://forums.clamwin.com/')


    def OnHelpUpdate(self, event):
        wxDialogUtils.wxGoToInternetUrl('http://www.clamwin.com/index.php?option=content&task=view&id=40&Itemid=60&version='+version.clamwin_version.replace('0:', ''))


    def OnHelpWebsite(self, event):
        wxDialogUtils.wxGoToInternetUrl('http://www.clamwin.com')

class wxGenericDirCtrlEx(wx.GenericDirCtrl):
    def __init__(self,*_args,**_kwargs):
        try:
            if _kwargs.get('multiselect', True) == True:
                multiselect = True
                if 'multiselect' in _kwargs: del _kwargs['multiselect']
            else:
                multiselect = False
        except KeyError:
            multiselect = True

        try:
            if _kwargs.get('showhidden', True) == True:
                showhidden = True
                if 'showhidden' in _kwargs: del _kwargs['showhidden']
            else:
                showhidden = False
        except KeyError:
            showhidden = True

        wx.GenericDirCtrl.__init__(self, *_args, **_kwargs)
        self.ShowHidden(showhidden)
        if multiselect:
            tree = self.GetTreeCtrl()
            tree.SetWindowStyleFlag(tree.GetWindowStyleFlag() | wx.TR_MULTIPLE)

    def GetMultiplePath(self):
        multiPath = []
        tree = self.GetTreeCtrl()
        sels = tree.GetSelections()
        for sel in sels:
            item = sel
            path = ''
            itemtext = tree.GetItemText(item)
            while True:
                try:
                    if not sys.platform.startswith("win"):
                        # unix - terminate when path=='/'
                        if itemtext == '/':
                            path = itemtext + path
                            break
                        else:
                            path = itemtext + '/' + path
                    else:
                        # windows, root drive is enclosed in ()
                        if itemtext.startswith('(') and itemtext.endswith(':'):
                            # remove '(' and ')'
                            itemtext = itemtext.strip('()')
                            path = itemtext + '\\' + path
                            break
                        else:
                            path = itemtext + '\\' + path
                    item = tree.GetItemParent(item)
                    itemtext = tree.GetItemText(item)
                except Exception as e:
                    print(f"Error constructing path: {e}")
                    break
            if len(path) > 1:
                path = path.rstrip('\\/')
            multiPath.append(path)
        return multiPath
