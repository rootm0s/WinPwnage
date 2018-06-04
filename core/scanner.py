import os
import _winreg
from prints import *
from uac import *

silentcleanup = ["silentcleanup",
			"9600", # Works from
			"999999"] # Fixed in

sdclt_isolatedcommand = ["sdcltisolatedcommand",
				"10240", # Works from
				"17025"] # Fixed in

computerdefaults = ["computerdefaults",
			"10240", # Works from
			"999999"] # Fixed in
					
compmgmtlauncher = ["compmgmtlauncher",
			"7600", # Works from
			"15031"] # Fixed in

sdclt_control = ["sdcltcontrol",
			"10240", # Works from
			"16215"] # Fixed in

eventviewer = ["eventviewer",
			"7600", # Works from
			"15031"] # Fixed in

fodhelper = ["fodhelper",
		"10240", # Works from
		"999999"] # Fixed in

perfmon = ["perfmon",
		"7600", # Works from
		"16299"] # Fixed in

slui = ["slui", 
		"9600", # Works from
		"17134"] # Fixed in

sysprep = ["sysprep", 
		"7600", # Works from
		"10240"] # Fixed in

cliconfg = ["cliconfg",
		"7600", # Works from
		"10240"] # Fixed in

mcx2prov = ["mcx2prov",
		"7600", # Works from
		"10240"] # Fixed in

runas = ["runas", 
		"2600", # Works from
		"999999"] # Fixed in

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

	for function in (sdclt_isolatedcommand,
			silentcleanup,
			computerdefaults,
			compmgmtlauncher,
			sdclt_control,
			eventviewer,
			fodhelper,
			perfmon,
			sysprep,
			cliconfg,
			mcx2prov,			 
			slui):
		
		if int(cbn[0]) < int(function[2]) and int(cbn[0]) > int(function[1]):
			print_success("We can use ({}) supposed to work on build number: {}-{}".format(function[0],function[1],function[2]))
		else:
			print_error("Cannot use ({}) supposed to work on build number: {}-{}".format(function[0],function[1],function[2]))
			
	if (uac_status() == True):
		print_success("We can use ({}) supposed to work on build number: {}-{}".format(runas[0],runas[1],runas[2]))
	else:
		print_error("Cannot use ({}) supposed to work on build number: {}-{}".format(runas[0],runas[1],runas[2]))
