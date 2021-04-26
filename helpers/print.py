from os import system, name

class BColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    INFO = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def pretty_message(msg, msg_type, decorated=True):
	if decorated:
		hdr_type = ''
		if msg_type == BColors.OKGREEN:
			# Green
			hdr_type = "SUCCESS"
		elif msg_type == BColors.INFO:
			# Yellow
			hdr_type = "INFO"
		elif msg_type == BColors.FAIL:
			# Red
			hdr_type = "WARNING"
		
		if hdr_type == "INFO":
			print(f'{msg_type}[{hdr_type}]   {BColors.ENDC} {msg}')
		else:
			print(f'{msg_type}[{hdr_type}]{BColors.ENDC} {msg}')
	else:
		print(f'{msg_type}{msg}{BColors.ENDC}')

def clear():
    # for windows
	if name == 'nt':
		_ = system('cls')
		
	# for linux
	else:
		_ = system('clear')