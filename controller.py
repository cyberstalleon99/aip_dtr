from datetime import datetime
import time

from view import main_menu_view
from dtr import head_shots, register_unit, train_model
from dtr.dtr_app import aip
from helpers.print import clear, pretty_message, BColors

def start_dtr():
    clear()
    aip.start_dtr()

    clear()
    _main()

def register_employee():
    clear()
    head_shots.new_head_shot()

    _main()

def new_unit():
    try:
        clear()
        register_unit.new_unit()
    finally:
        _main()
        time.sleep

def _train_model():
    train_model.train_model()
    new_input()

def _exit():
    pass

def invalid_input():
    pretty_message("Invalid Input. Choose only from the choices.", BColors.FAIL)
    new_input()

def switch_main_menu(choice):
    switcher = {
        '1': start_dtr,
        '2': register_employee,
        '3': new_unit, 
        '4': _train_model,
        'Q': _exit,
        'q': _exit
    }
   
    choice = switcher.get(choice)

    if choice != None:
        return choice
    else:
        return invalid_input

def new_input():
    main_menu_choice = input('Choose from the Menu: ')
    switch_main_menu(main_menu_choice)()

def _main():
    main_menu_view()
    new_input()

if __name__ == "__main__":
    clear()
    _main()
