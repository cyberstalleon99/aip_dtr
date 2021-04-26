import sys
from datetime import datetime

import settings

from helpers.rfid import rfid_reader
from helpers.print import pretty_message, BColors

body_no = ''
    
def show_menu():
    print("*******************************************************")
    print('Program started at: %s' % (datetime.now()))
    pretty_message("Register New Unit", BColors.OKGREEN, False)
    print("*******************************************************")
    pretty_message("Choices: ", BColors.OKCYAN, False)
    pretty_message(" - (Q):      Go back to Main Menu", BColors.FAIL, False)
    print("*******************************************************")

def new_unit():
    show_menu()
    _new_input()

def _new_input():
    print("")
    global body_no
    body_no = input('Entery the Body No. of the Unit (Press Q to exit): ')
    
    if body_no == 'Q' or body_no == 'q':
        return

    pretty_message('Swipe the new RFID Card/Tag', BColors.INFO)
    rfid_reader.write(body_no)
    pretty_message(f'Unit: {body_no}', BColors.INFO)
    pretty_message('Thank you, your new RFID card has been registered!', BColors.OKGREEN)

    _again()

def _again():
    again = input('Would you like to register a new unit? (Y/N): ')

    if again == 'N' or again == 'n':
        return
    elif again == 'Y' or again == 'y':
        _new_input()
    else:
        pretty_message('Invalid input. Please choose between Y/N', BColors.FAIL)

def _main():
    new_unit()
    
if __name__ == "__main__":
    _main()
