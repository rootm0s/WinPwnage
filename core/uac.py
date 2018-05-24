import os
import _winreg
from prints import *

def uac_status():
	"""
	Identify if UAC is set to Never Notify, if true
	we can use runas to elevate process instead of using
	some exploit
	"""
	try:
		key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,
					os.path.join("Software\Microsoft\Windows\CurrentVersion\Policies\System"),0,_winreg.KEY_READ)

		ConsentPromptBehaviorAdmin = _winreg.QueryValueEx(key,"ConsentPromptBehaviorAdmin")							
		ConsentPromptBehaviorUser = _winreg.QueryValueEx(key,"ConsentPromptBehaviorUser")
		_winreg.CloseKey(key)
		
		if (ConsentPromptBehaviorAdmin[0] == 0) and (ConsentPromptBehaviorUser[0] == 3):
			return True
		else:
			return False
	except Exception as error:
		return False
