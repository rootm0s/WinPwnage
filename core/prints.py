import datetime
from colorama import init, Fore
init(convert=True)

def print_success(message):
	print (Fore.GREEN + " [+] " + Fore.RESET + str(datetime.datetime.now()) + ": " + message)

def print_error(message):
	print (Fore.RED + " [+] " + Fore.RESET + str(datetime.datetime.now()) + ": " + message)

def print_info(message):
	print (Fore.CYAN + " [!] " + Fore.RESET + str(datetime.datetime.now()) + ": " + message)
	
def print_warning(message):
	print (Fore.YELLOW + " [!] " + Fore.RESET + str(datetime.datetime.now()) + ": " + message)