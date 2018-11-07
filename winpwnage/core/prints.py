from colorama import init, Fore
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
	print(Fore.GREEN + " " + id + Fore.RESET + message)
	Constant.output.append(("ok", id + message))


def table_error(id, message):
	print(Fore.RED + " " + id + Fore.RESET + message)
	Constant.output.append(("error", id + message))


def print_success(message):
	print(Fore.GREEN + " [*] " + Fore.RESET + message)
	Constant.output.append(("ok", message))


def print_error(message):
	print(Fore.RED + " [-] " + Fore.RESET + message)
	Constant.output.append(("error", message))


def print_info(message):
	print(Fore.CYAN + " [!] " + Fore.RESET + message)
	Constant.output.append(("info", message))


def print_warning(message):
	print(Fore.YELLOW + " [!] " + Fore.RESET + message)
	Constant.output.append(("warning", message))
