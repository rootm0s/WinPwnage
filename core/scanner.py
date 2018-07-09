import os
import _winreg
from prints import *
from uac import *

silentcleanup = ["silentcleanup","9600","999999"]
sdclt_isolatedcommand = ["sdcltisolatedcommand","10240","17025"]
computerdefaults = ["computerdefaults","10240","999999"]			
compmgmtlauncher = ["compmgmtlauncher","7600","15031"]
sdclt_control = ["sdcltcontrol","10240","16215"]
eventviewer = ["eventviewer","7600","15031"]
fodhelper = ["fodhelper","10240","999999"]
perfmon = ["perfmon","7600","16299"]
slui = ["slui","9600","17134"] 
sysprep = ["sysprep","7600","10240"] 
cliconfg = ["cliconfg","7600","10240"] 
mcx2prov = ["mcx2prov","7600", "10240"]	
migwiz = ["migwiz", "7600", "10240"]
runas = ["runas", "2600","999999"]
explorer = ["explorer", "7600", "9600"]	
schtask = ["schtask","7600", "999999"]
ifeo = ["ifeo","7600", "999999"]
hklmrun = ["hklm_run","2900","999999"]

def scan():
	"""
	Read build number from registry in attempt to match
	it against our exploits and functions
	"""
	try:
		key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,
					os.path.join("Software\Microsoft\Windows NT\CurrentVersion"),0,_winreg.KEY_READ)
		cbn = _winreg.QueryValueEx(key,
					"CurrentBuildNumber")
		_winreg.CloseKey(key)
		print_info("Build number: {}".format(cbn[0]))
	except Exception as error:
		print_error("Unable to identify build number: {}".format(error))
		return False

	"""
	UAC bypass techniques
	"""
	for function in (sdclt_isolatedcommand,silentcleanup,computerdefaults,compmgmtlauncher,sdclt_control,eventviewer,fodhelper,sysprep,cliconfg,mcx2prov,migwiz,perfmon,slui):
		if int(cbn[0]) < int(function[2]) and int(cbn[0]) > int(function[1]):
			print_success("UAC bypass > We can use ({}) supposed to work on build number: {}-{}".format(function[0],function[1],function[2]))
		else:
			print_error("UAC bypass > Cannot use ({}) supposed to work on build number: {}-{}".format(function[0],function[1],function[2]))

	if (uac_status() == True):
		print_success("UAC bypass > We can use ({}) supposed to work on build number: {}-{}".format(runas[0],runas[1],runas[2]))
	else:
		print_error("UAC bypass > Cannot use ({}) supposed to work on build number: {}-{}".format(runas[0],runas[1],runas[2]))

	"""
	Pestistence techniques
	"""
	for function in (schtask,explorer,ifeo,hklmrun):
		if int(cbn[0]) < int(function[2]) and int(cbn[0]) > int(function[1]):
			print_success("Persist > We can use ({}) supposed to work on build number: {}-{}".format(function[0],function[1],function[2]))
		else:
			print_error("Persist > Cannot use ({}) supposed to work on build number: {}-{}".format(function[0],function[1],function[2]))
