import sys, os, inspect

# print(sys.path)
# currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# parentdir = os.path.dirname(currentdir)

# print('System Path: ')
# print(sys.path)

# print("Current Directory: ")
# print(currentdir)

# print("Parent Directory: ")
# print(parentdir)

# sys.path.insert(0, '/home/pi/aip_mvc')

# print('System Path: ')
# print(sys.path)


# currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# parentdir = os.path.dirname(currentdir)
# sys.path.insert(0,parentdir)

# from helpers.rfid import rfid_reader
# # from ...helpers import pushbuttons
# # from ...helpers.print import pretty_message, BColors

# import helpers.rfid
# from aip_mvc.helpers.rfid import rfid_reader
# from aip_mvc.helpers.rfid import rfid_reader
# from AIP_MVC.helpers.rfid import rfid_reader


# import sys
# from os import path
# print(sys.path)
# sys.path.append( path.dirname( path.dirname( path.dirname(path.dirname(path.abspath(__file__))) ) ) )

# print(sys.path)
# from aip_mvc.helpers.rfid import rfid_reader
# import head_shots

# from datetime import datetime

# print(datetime.now())

# def test():

#     return (1, 'Clyde Khayad')

# key, name = test()

# print(name)
# open("/home/pi/aip_mvc/dtr/dtr_app/encodings.pickle")

path = os.path.join("/home/pi/aip_mvc/dtr/dtr_app/dataset", "Clyde Khayad")
print(path.find("Clyed"))