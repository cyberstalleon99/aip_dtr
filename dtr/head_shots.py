import cv2
import os
from datetime import datetime

from helpers.print import pretty_message, BColors
from helpers import pushbuttons
import settings

from dtr.train_model import train_model_partial

name = ''

DONE = 'Done'
CLOSED = 'Closed'

def show_menu():
    print("*******************************************************")
    print('Program started at: %s' % (datetime.now()))
    pretty_message("AIP Facial Capture!", BColors.OKGREEN, False)
    print("*******************************************************")
    pretty_message("Choices: ", BColors.OKCYAN, False)
    pretty_message(" - (Space):  Capture", BColors.OKGREEN, False)
    pretty_message(" - (Esc):    Close the camera", BColors.HEADER, False)
    pretty_message(" - (Q):      Go back to Main Menu", BColors.FAIL, False)
    print("*******************************************************")
    
def _print_switcher(img_counter):
    
    choices = {
        0: 'Look at the Camera!',
        1: 'Slightly tilt your head UP!',
        2: 'Slightly tilt your head DOWN!',
        3: 'Slightly tilt your head to your LEFT!',
        4: 'Slightly tilt your head to your RIGHT!',
        5: 'Look at the Camera AGAIN!',
        6: 'Successfully registered a new Employee. Press again to continue...'
    }
    
    if img_counter == 6:
        pretty_message(choices.get(img_counter), BColors.OKGREEN)
    else:
        pretty_message(choices.get(img_counter), BColors.INFO)

def _new_input():
    global name
    name = input('Employee (Firstname Lastname): ')

    if name == "Q" or name == "q":
        return
    else:
        print("")
        _main()
    
def init_camera():
    
    pretty_message('Opening camera...', BColors.INFO)
    
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("press space to take a photo", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("press space to take a photo", 500, 300)

    pretty_message('Camera ready. Please follow the instructions.\n', BColors.INFO)
    
    return cam
    
def close_camera(cam):
    cam.release()
    cv2.destroyAllWindows()

# Entry Point
def new_head_shot():
    pushbuttons.init()
    settings.ACTIVE_APP = os.path.splitext(os.path.basename(__file__))[0]
    show_menu()
    _new_input()
    pushbuttons.clean_up()

def _main():
    cam = init_camera()
    
    img_counter = 0                                                                                           
    call_back = ''
    _print_switcher(img_counter)
    
    while True:
        ret, frame = cam.read()
        if not ret:                                                         
            print("failed to grab frame")
            break
        cv2.imshow("press space to take a photo", frame)

        k = cv2.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            call_back = CLOSED
            break
        elif k%256 == 32:
            # SPACE pressed
            if img_counter <= 5:

                dataset_path = os.path.join(settings.DATASET_UNTRAINED_PATH, name)
                if not os.path.exists(dataset_path):
                    os.mkdir(dataset_path)

                # Create a folder for untrained models
                img_name = os.path.join(dataset_path, "image_{}.jpg".format(img_counter))
                cv2.imwrite(img_name, frame)
                pretty_message("{} written!".format(img_name), BColors.OKGREEN)
                
                img_counter += 1
                _print_switcher(img_counter)
            else:
                call_back = DONE
                again = input('Would you like to register a new employee? (Y/N): ')
                if again == 'N' or again == 'n':
                    # Call train_model function
                    train_model_partial()
                    close_camera(cam)
                    return
                elif again == 'Y' or again == 'y':
                    close_camera(cam)
                    _new_input()
                else:
                    pretty_message('Invalid input. Please choose between Y/N', BColors.FAIL)

        pushbuttons.read_kboard()

    close_camera(cam)

    return call_back

if __name__ == "__main__":
    new_head_shot()
