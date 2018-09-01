from colorama import init, Fore
init(convert=True)

table = """
 Id:    Type:           Payload:        Admin:          Description:
 ----   -----------     -----------     --------        -----------------------"""

def print_table():
	print (table)

def table_success(id,message):
	print (Fore.GREEN + " " + id + Fore.RESET + message)
	
def table_error(id,message):
	print (Fore.RED + " " + id + Fore.RESET + message)
	
def print_success(message):
	print (Fore.GREEN + " [*] " + Fore.RESET + message)

def print_error(message):
	print (Fore.RED + " [-] " + Fore.RESET + message)

def print_info(message):
	print (Fore.CYAN + " [!] " + Fore.RESET + message)
	
def print_warning(message):
	print (Fore.YELLOW + " [!] " + Fore.RESET + message)
