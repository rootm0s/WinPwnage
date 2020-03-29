from __future__ import print_function
try:
	status = None
	from colorama import init, Fore
except:
	status = False
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
	if status == False:
		print("" + " " + id + message)
	else:
		print(Fore.GREEN + " " + id + Fore.RESET + message)
	Constant.output.append(("ok", id + message))


def table_error(id, message):
	if status == False:
		print("" + " " + id + message)
	else:
		print(Fore.RED + " " + id + Fore.RESET + message)
	Constant.output.append(("error", id + message))

def print_success(message):
	if status == False:
		print(" [+] " + message)
	else:
		print(Fore.GREEN + " [+] " + Fore.RESET + message)
	Constant.output.append(("ok", message))

def print_error(message):
	if status == False:
		print(" [-] " + message)
	else:
		print(Fore.RED + " [-] " + Fore.RESET + message)
	Constant.output.append(("error", message))

def print_info(message):
	if status == False:
		print(" [!] " + message)
	else:
		print(Fore.CYAN + " [!] " + Fore.RESET + message)
	Constant.output.append(("info", message))

def print_warning(message):
	if status == False:
		print(" [!] " + message)
	else:
		print(Fore.YELLOW + " [+] " + Fore.RESET + message)
	Constant.output.append(("warning", message))
