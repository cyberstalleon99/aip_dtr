from datetime import datetime
from helpers.print import pretty_message, BColors

def main_menu_view():
    print("*******************************************************")
    print('Program started at: %s' % (datetime.now()))
    pretty_message("Main Menu", BColors.OKGREEN, False)
    print("*******************************************************")
    pretty_message("Choices:", BColors.OKCYAN, False)
    pretty_message(" - (1): Start DTR", BColors.OKGREEN, False)
    pretty_message(" - (2): New Employee", BColors.FAIL, False)
    pretty_message(" - (3): Train Model", BColors.INFO, False)
    pretty_message(" - (4): Extract DTR", BColors.INFO, False)
    pretty_message(" - (5): New Unit", BColors.OKCYAN, False)
    pretty_message(" - (Q): To Exit", BColors.HEADER, False)
    print("*******************************************************")

