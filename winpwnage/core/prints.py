from __future__ import print_function
try:
	from colorama import init, Fore
except:
	pass
else:
	init(convert=True)

table = """
 Id:    Type:           Payload:        Admin:          Description:
 ----   -----------     -----------     --------        -----------------------"""


class Constant:
	output = []


def reset_output():
	Constant.output = []


def print_table():
	print(table)
	Constant.output.append(("t", table))


def table_success(id, message):
	print("\033[92m" + " " + id + "\033[0m" + message)
	Constant.output.append(("ok", id + message))


def table_error(id, message):
	print("\033[31m" + " " + id + "\033[0m" + message)
	Constant.output.append(("error", id + message))


def print_success(message):
	print("033[92m" + " [+] " + "\033[0m" + message)
	Constant.output.append(("ok", message))


def print_error(message):
	print("\033[31m" + " [-] " + "\033[0m" + message)
	Constant.output.append(("error", message))


def print_info(message):
	print("\033[36m" + " [!] " + "\033[0m" + message)
	Constant.output.append(("info", message))


def print_warning(message):
	print("\033[93m" + " [!] " + "\033[0m" + message)
	Constant.output.append(("warning", message))
