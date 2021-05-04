#!/usr/bin/python3

from datetime import datetime
import time

print('Importing Views.....')
from view import main_menu_view
print('Importing Apps. Please wait.....')
from dtr import head_shots, register_unit, train_model
from dtr.dtr_app import aip
from dtr.dtr_app.models import Entry
from helpers.print import clear, pretty_message, BColors

def _start_dtr():
    clear()
    aip.start_dtr()

    clear()
    _main()

def _register_employee():
    clear()
    head_shots.new_head_shot()

    _main()

def _new_unit():
    try:
        clear()
        register_unit.new_unit()
    finally:
        _main()
        time.sleep

def _train_model():
    train_model.train_model_partial()
    new_input()

def _extract_dtr():
    Entry.export_to_excel()
    new_input()

def _exit():
    pass

def invalid_input():
    pretty_message("Invalid Input. Choose only from the choices.", BColors.FAIL)
    new_input()

def switch_main_menu(choice):
    switcher = {
        '1': _start_dtr,
        '2': _register_employee,
        '3': _train_model, 
        '4': _extract_dtr, 
        '5': _new_unit,
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
