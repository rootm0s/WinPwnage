import os
import wmi
import ctypes
import _winreg

wmi = wmi.WMI()

class disable_fsr():
	"""
	A class to disable file system redirection
	"""
	disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
	revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection

	def __enter__(self):
		self.old_value = ctypes.c_long()
		self.success = self.disable(ctypes.byref(self.old_value))
	def __exit__(self,type,value,traceback):
		if self.success:
			self.revert(self.old_value)

class process():
	"""
	A class to spawn, elevate or terminate processes
	"""
	def create(self,payload,window):
		try:
			pid,result = wmi.Win32_Process.Create(CommandLine=os.path.join(payload),ProcessStartupInformation=wmi.Win32_ProcessStartup.new(ShowWindow=window))
		except Exception as error:
			return False

		if (result == 0):
			return True
		else:
			return False

	def runas(self,payload):
		try:
			if (ctypes.windll.Shell32.ShellExecuteA(None,"runas",os.path.join(payload),None,None,1) >= 42):
				return True
			else:
				return False
		except Exception as error:
			return False
		
	def terminate(self,processname):
		for process in wmi.Win32_Process():
				if (process.Caption == processname):
					try:
						process.Terminate(process.ParentProcessId)
					except Exception as error:
						return False
					else:
						return True
						break

class information():
	"""
	A class to handle all the information gathering
	"""
	def system_directory(self):
		for os in wmi.Win32_OperatingSystem():
			return os.SystemDirectory
			
	def windows_directory(self):
		for os in wmi.Win32_OperatingSystem():
			return os.WindowsDirectory
			
	def architecture(self):
		for os in wmi.Win32_OperatingSystem():
			return os.OSArchitecture				

	def admin(self):
		if (ctypes.windll.shell32.IsUserAnAdmin() == True):
			return True
		else:
			return False

	def build_number(self):
		try:
			key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,os.path.join("Software\Microsoft\Windows NT\CurrentVersion"),0,_winreg.KEY_READ)									
			cbn = _winreg.QueryValueEx(key,"CurrentBuildNumber")
			_winreg.CloseKey(key)
		except Exception as error:
			return False
		else:
			return cbn[0]
		
	def uac_level(self):
		try:
			key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,os.path.join("Software\Microsoft\Windows\CurrentVersion\Policies\System"),0,_winreg.KEY_READ)											
			cpba = _winreg.QueryValueEx(key,"ConsentPromptBehaviorAdmin")							
			cpbu = _winreg.QueryValueEx(key,"ConsentPromptBehaviorUser")
			posd = _winreg.QueryValueEx(key,"PromptOnSecureDesktop")
			_winreg.CloseKey(key)
		except Exception as error:
			return False
				
		if (cpba[0] == 0) and (cpbu[0] == 3) and (posd[0] == 0):
			return 1
		elif (cpba[0] == 5) and (cpbu[0] == 3) and (posd[0] == 0):
			return 2
		elif (cpba[0] == 5) and (cpbu[0] == 3) and (posd[0] == 1):
			return 3
		elif (cpba[0] == 2) and (cpbu[0] == 3) and (posd[0] == 1):
			return 4
		else:
			return False				
