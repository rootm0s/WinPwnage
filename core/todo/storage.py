"""
Works from: Windows XP
Fixed in: unfixed
"""
import os
import _winreg
from colorama import init, Fore
init(convert=True)

def successBox():
	return (Fore.GREEN + '[+]' + Fore.RESET)

def errorBox():
	return (Fore.RED + '[-]' + Fore.RESET)

def infoBox():
	return (Fore.CYAN + '[!]' + Fore.RESET)	

def warningBox():
	return (Fore.YELLOW + '[!]' + Fore.RESET)

def reader(file_path):
	print " {} storage: Checking file size".format(infoBox())
	if (os.path.getsize(file_path) < 1000000):
		print " {} storage: Reading binary data: {}".format(infoBox(),file_path) 
		try:
			file = open(file_path, "rb")
			return file.read()
			print " {} storage: Successfully read binary data".format(successBox())
		except Exception as error:
			print " {} storage: Unable to read binary data".format(errorBox())
			return False
	else:
		print " {} storage: File size error".format(errorBox())
		return False

def storage_delete():
	print " {} storage: Attempting to delete registry key".format(infoBox())
	try:
		_winreg.DeleteKey(_winreg.HKEY_CURRENT_USER,
							os.path.join("Software\Classes\.storage\container"))
		print " {} storage: Registry key deleted".format(successBox())
	except Exception as error:
		print " {} storage: Unable to delete registry key".format(errorBox())
		return False
		
def storage_save_to_disk(file_path):
	print " {} storage: Attempting to read binary data from the registry key".format(infoBox())
	try:
		key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,
							os.path.join("Software\Classes\.storage\container"),
							0,
							_winreg.KEY_READ)

		data = _winreg.QueryValueEx(key,None)
		_winreg.CloseKey(key)
		print " {} storage: Successfully read binary data".format(successBox())
	except Exception as error:
		print " {} storage: Unable to read binary data from the registry".format(errorBox())
		return False

	print " {} storage: Attempting to save file to disk: {}".format(infoBox(),file_path)
	try:
		file = open(file_path,"wb")
		file.write(data[0])
		file.close()
		print " {} storage: File saved to disk: {}".format(successBox(),file_path)
	except Exception as error:
		print " {} storage: Unable to save file on disk".format(errorBox())
		return False

def storage_save_to_reg(file_path):
	print " {} storage: Attempting to store binary data inside a registry key".format(infoBox())
	try:
		key = _winreg.CreateKey(_winreg.HKEY_CURRENT_USER,
								os.path.join("Software\Classes\.storage\container"))
								
		_winreg.SetValueEx(key,
							None,
							0,
							_winreg.REG_BINARY,
							reader(file_path))
		_winreg.CloseKey(key)
		print " {} storage: Registry key created containing our binary data".format(successBox())
	except Exception as error:
		print " {} storage: Unable to store binary data inside the registry key".format(errorBox())
		return False
		
def storage_list():
	print " {} storage: Listing available binary data".format(infoBox())
	try:
		key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,
							os.path.join("Software\Classes\.storage\container"),
							0,
							_winreg.KEY_READ)

		data = _winreg.QueryValueEx(key,None)
		_winreg.CloseKey(key)
		print " {} storage: {}".format(successBox(),data[0])
	except Exception as error:
		print " {} storage: Unable to list binary data".format(errorBox())
		return False