from __future__ import print_function

table = """
 Id:    Type:           Compatible:     Description:
 ----   ------          -----------     -------------"""

class Constant:
	output = []

def reset_output():
	Constant.output = []

def print_table():
	print(table)
	Constant.output.append(("t", table))

def table_success(id, type, description):
	print(" {}\t{}\tYes\t\t{}".format(id, type, description))
	Constant.output.append(("ok", id + type + description))

def table_error(id, type, description):
	print(" {}\t{}\tNo\t\t{}".format(id, type, description))
	Constant.output.append(("error", id + type + description))

def print_success(message):
	print(" [+] " + message)
	Constant.output.append(("ok", message))

def print_error(message):
	print(" [-] " + message)
	Constant.output.append(("error", message))

def print_info(message):
	print(" [!] " + message)
	Constant.output.append(("info", message))

def print_warning(message):
	print(" [!] " + message)
	Constant.output.append(("warning", message))