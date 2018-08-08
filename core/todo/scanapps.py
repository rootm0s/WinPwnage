"""
Really simple method to look for auto elevated applications
by searching for strings in binary data:

* <autoElevate>true</autoElevate>
* <autoElevate xmlns=\"http://schemas.microsoft.com/SMI/2005/WindowsSettings\">true</autoElevate>
"""
import os
import sys
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

def look_for_autoelevated_apps(path):
	process_list = []
	
	for root, dirs, files in os.walk(os.path.join(path)):
		for file in files:
			if (".exe" in file):
				try:
					exe = open(os.path.join(path,file), "rb")
					manifest = exe.read()
					exe.close()
				except IOError:
					pass

				if ("<autoElevate>true</autoElevate>" in manifest):
					process_list.append(os.path.join(path,file))
				if ("<autoElevate xmlns=\"http://schemas.microsoft.com/SMI/2005/WindowsSettings\">true</autoElevate>" in manifest):
					process_list.append(os.path.join(path,file))
	
	print " {} Listing processes:".format(infoBox())
	for process in process_list:
		print " {} {}".format(successBox(),process)