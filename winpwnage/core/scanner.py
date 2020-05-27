from winpwnage.core.prints import print_info, print_error, print_table, table_success, table_error, Constant
from winpwnage.core.utils import information
from winpwnage.functions.uac.uacMethod1 import *
from winpwnage.functions.uac.uacMethod2 import *
from winpwnage.functions.uac.uacMethod3 import *
from winpwnage.functions.uac.uacMethod4 import *
from winpwnage.functions.uac.uacMethod5 import *
from winpwnage.functions.uac.uacMethod6 import *
from winpwnage.functions.uac.uacMethod7 import *
from winpwnage.functions.uac.uacMethod8 import *
from winpwnage.functions.uac.uacMethod9 import *
from winpwnage.functions.uac.uacMethod10 import *
from winpwnage.functions.uac.uacMethod11 import *
from winpwnage.functions.uac.uacMethod12 import *
from winpwnage.functions.uac.uacMethod13 import *
from winpwnage.functions.uac.uacMethod14 import *
from winpwnage.functions.uac.uacMethod15 import *
from winpwnage.functions.persist.persistMethod1 import *
from winpwnage.functions.persist.persistMethod2 import *
from winpwnage.functions.persist.persistMethod3 import *
from winpwnage.functions.persist.persistMethod4 import *
from winpwnage.functions.persist.persistMethod5 import *
from winpwnage.functions.persist.persistMethod6 import *
from winpwnage.functions.persist.persistMethod7 import *
from winpwnage.functions.persist.persistMethod8 import *
from winpwnage.functions.persist.persistMethod9 import *
from winpwnage.functions.persist.persistMethod10 import *
from winpwnage.functions.persist.persistMethod11 import *
from winpwnage.functions.persist.persistMethod12 import *
from winpwnage.functions.elevate.elevateMethod1 import *
from winpwnage.functions.elevate.elevateMethod2 import *
from winpwnage.functions.elevate.elevateMethod3 import *
from winpwnage.functions.elevate.elevateMethod4 import *
from winpwnage.functions.elevate.elevateMethod5 import *
from winpwnage.functions.elevate.elevateMethod6 import *
from winpwnage.functions.elevate.elevateMethod7 import *

functions = {
	"uac": (
		uacMethod1_info,
		uacMethod2_info,
		uacMethod3_info,
		uacMethod4_info,
		uacMethod5_info,
		uacMethod6_info,
		uacMethod7_info,
		uacMethod8_info,
		uacMethod9_info,
		uacMethod10_info,
		uacMethod11_info,
		uacMethod12_info,
		uacMethod13_info,
		uacMethod14_info,
		uacMethod15_info
	),
	"persist": (
		persistMethod1_info,
		persistMethod2_info,
		persistMethod3_info,
		persistMethod4_info,
		persistMethod5_info,
		persistMethod6_info,
		persistMethod7_info,
		persistMethod8_info,
		persistMethod9_info,
		persistMethod10_info,
		persistMethod11_info
	),
	"elevate": (
		elevateMethod1_info,
		elevateMethod2_info,
		elevateMethod3_info,
		elevateMethod4_info,
		elevateMethod5_info,
		elevateMethod6_info,
		elevateMethod7_info
	)
}

class scanner():
	def __init__(self, uac=True, persist=True, elevate=True):
		self.uac = uac
		self.persist = persist
		self.elevate = elevate
		Constant.output = []

	def start(self):
		print_info("Comparing build number ({buildnumber}) against 'Fixed In' build numbers".format(buildnumber=information().build_number()))
		print_table()
		for i in functions:
			if i == "uac" and not self.uac or i == "persist" and not self.persist or i == "elevate" and not self.elevate:
				continue

			for info in functions[i]:
				if int(info["Works From"]) <= int(information().build_number()) < int(info["Fixed In"]):
					table_success(id=info["Id"], type=info["Type"], description=info["Description"])
				else:
					table_error(id=info["Id"], type=info["Type"], description=info["Description"])
		return Constant.output

class function():
	def __init__(self, uac=True, persist=True, elevate=True):
		self.uac = uac
		self.persist = persist
		self.elevate = elevate
		Constant.output = []

	def run(self, id, payload, **kwargs):
		print_info("Attempting to run method ({id}) configured with payload ({payload})".format(id=id, payload=payload))
		for i in functions:
			if i == "uac" and not self.uac or i == "persist" and not self.persist or i == "elevate" and not self.elevate:
				continue

			for info in functions[i]:
				if id in str(info["Id"]):
					if int(info["Works From"]) <= int(information().build_number()) < int(info["Fixed In"]):
						f = globals()[info["Function Name"]]
						if "name" not in f.__code__.co_varnames and "add" in f.__code__.co_varnames:
							f(payload, add=kwargs.get("add", True))
						elif "name" in f.__code__.co_varnames and "add" in f.__code__.co_varnames:
							f(payload, name=kwargs.get("name", "WinPwnage"), add=kwargs.get("add", True))
						else:
							f(payload)
					else:
						print_error("Technique not compatible with this system.")
					return Constant.output
				else:
					pass