#!/usr/bin/python
#Boa:App:BoaApp

#-----------------------------------------------------------------------------
# Name:        ClamWin.py
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
import SetUnicode
import sys, os, locale
import RedirectStd
import wx # <--- 이 줄이 변경되었습니다.
import wxFrameMain
#import Config
import win32api

# --- 추가된 부분 시작 ---
# MinGW DLL들이 있는 경로를 os.add_dll_directory()로 추가
# Python 3.8+에서 권장되는 DLL 검색 경로 추가 방법
try:
    os.add_dll_directory("D:/msys64_231026/mingw32/bin") # MinGW 32bit DLLs
    # ClamAV 빌드 디렉토리도 추가 (libclamav.dll이 여기에 있을 수 있음)
    os.add_dll_directory("D:/msys64_231026/home/user/clamav-win32-0.103/build")
    # Python이 현재 스크립트 디렉토리도 검색하므로 이 부분은 선택 사항이지만, 명시적 추가는 안전합니다.
    os.add_dll_directory(os.path.abspath(os.path.dirname(__file__)))
except AttributeError:
    # Python 3.8 이전 버전에서는 os.add_dll_directory가 없으므로 pass
    pass
# --- 추가된 부분 끝 ---

# import pyclamav here
#hLibClamAV = 0
#try:
#    hLibClamav = win32api.LoadLibrary(os.path.join(Utils.GetCurrentDir(False), "libclamav.dll"))
#except Exception, e:
#    print str(e), os.path.join(Utils.GetCurrentDir(False), "libclamav.dll")

#hLibClamUnrar = 0
#try:
#    hLibClamUnrar = win32api.LoadLibrary(os.path.join(Utils.GetCurrentDir(False), "libclamunrar.dll"))
#except Exception, e:
#    print str(e), os.path.join(Utils.GetCurrentDir(False), "libclamunrar.dll")

#hLibClamUnrar_iface = 0
#try:
#    hLibClamUnrar_iface = win32api.LoadLibrary(os.path.join(Utils.GetCurrentDir(False), "libclamunrar_iface.dll"))
#except Exception, e:
#    print str(e), os.path.join(Utils.GetCurrentDir(False), "libclamunrar_iface.dll")

#sys.path.insert(0, Utils.GetCurrentDir(False))
#print sys.path
import clamav


modules ={'ClamTray': [0, '', 'ClamTray.py'],
 'CloseWindows': [0, '', 'CloseWindows.py'],
 'Config': [0, '', 'Config.py'],
 'EmailAlert': [0, '', 'EmailAlert.py'],
 'ExplorerShell': [0, '', 'ExplorerShell.py'],
 'MsgBox': [0, '', 'MsgBox.py'],
 'OlAddin': [0, '', 'OlAddin.py'],
 'Process': [0, '', 'Process.py'],
 'RedirectStd': [0, '', 'RedirectStd.py'],
 'Scheduler': [0, '', 'Scheduler.py'],
 'SplashScreen': [0, '', 'SplashScreen.py'],
 'Utils': [0, '', 'Utils.py'],
 'wxDialogAbout': [0, '', 'wxDialogAbout.py'],
 'wxDialogCheckUpdate': [0, '', 'wxDialogCheckUpdate.py'],
 'wxDialogLogViewer': [0, '', 'wxDialogLogViewer.py'],
 'wxDialogPreferences': [0, '', 'wxDialogPreferences.py'],
 'wxDialogScheduledScan': [0, '', 'wxDialogScheduledScan.py'],
 'wxDialogStatus': [0, '', 'wxDialogStatus.py'],
 'wxDialogUtils': [0, '', 'wxDialogUtils.py'],
 'wxFrameMain': [1, 'Main frame of Application', 'wxFrameMain.py']}

class BoaApp(wx.App): # <--- wxApp -> wx.App 으로 변경되었습니다.
    def __init__(self, params, config, mode='main', autoClose=False, path=''):
        self.config = config
        self.mode = mode
        self.path = path
        self.autoClose = autoClose
        self.exit_code = 0
        wx.App.__init__(self, params) # <--- wxApp -> wx.App 으로 변경되었습니다.

    def OnInit(self):
        wx.InitAllImageHandlers() # <--- wxInitAllImageHandlers -> wx.InitAllImageHandlers 로 변경되었습니다.
        if self.mode == 'scanner':
            if clamav.isWow64():
                self.DisablefsRedirect()
            self.exit_code = wxDialogUtils.wxScan(parent=None, config=self.config, path=self.path, autoClose=self.autoClose)
        elif self.mode == 'update':
            self.exit_code = wxDialogUtils.wxUpdateVirDB(parent=None, config=self.config, autoClose=self.autoClose)
        elif self.mode == 'configure':
            wxDialogUtils.wxConfigure(parent=None, config=self.config)
        elif self.mode == 'configure_schedule':
            wxDialogUtils.wxConfigure(parent=None, config=self.config, switchToSchedule=True)
        elif self.mode == 'about':
            wxDialogUtils.wxAbout(parent=None, config=self.config)
        elif self.mode == 'viewlog':
            wxDialogUtils.wxShowLog(parent=None, logfile=self.path.strip('"'))
        elif self.mode == 'checkversion':
            if not wxDialogUtils.wxCheckUpdate(parent=None, config=self.config):
                self.exit_code = 1

        else: #  mode == 'main'
            if clamav.isWow64():
                self.DisablefsRedirect()
            self.main = wxFrameMain.create(parent=None, config=self.config)
            self.main.Show()
            #workaround for running in wxProcess
            self.SetTopWindow(self.main)
        return True

    def DisablefsRedirect(self):
        try:
            #load dlls that fail after fs redir is disabled
            win32api.LoadLibrary(os.path.join(win32api.GetSystemDirectory(), "riched32.dll"))
            win32api.LoadLibrary(os.path.join(win32api.GetSystemDirectory(), "shfolder.dll"))
        except Exception as e:
            print("Error disabling redirect on WOW64 %s" % str(e))

        try:
            #disable fs redir
            clamav.disableFsRedir()
        except Exception as e:
            print("Error disabling redirect on WOW64 %s" % str(e))


def main(config=None, mode='main', autoClose=False, path='', config_file=None):
    """
    currentDir = Utils.GetCurrentDir(True)
    os.chdir(currentDir)
    Utils.CreateProfile()    
    if config is None:
        if(config_file is None):
            config_file = os.path.join(Utils.GetProfileDir(True),'ClamWin.conf')
        else:
            config_file = Utils.SafeExpandEnvironmentStrings(config_file)
        config = Config.Settings(config_file)
        b = config.Read()

    """
    app = BoaApp(0, config, mode=mode, autoClose=autoClose, path=path)
    
    app.MainLoop()
    return app.exit_code


if __name__ == '__main__':
    import locale, codecs, encodings
    print("System Locale:", locale.getdefaultlocale())
    print("Default Encoding:", sys.getdefaultencoding())

    # set C locale, otherwise python and wxpython complain
    locale.setlocale(locale.LC_ALL, 'C')
    close = False
    mode = 'main'
    path = ''
    config_file = None
    for arg in sys.argv[1:]:
        if arg == '--close':
            close = True
        if arg.find('--mode=') == 0:
            mode = arg[len('--mode='):]
        if arg.find('--path=') == 0:
            path += '"' + arg[len('--path='):].replace('/', '\\') + '" '
        if arg.find('--config_file=') == 0:
            config_file = arg[len('--config_file='):]

    print("command line path: %s" % path.strip())
    exit_code = main(mode=mode, autoClose=close, path=path.strip(), config_file=config_file)
    sys.exit(exit_code)
