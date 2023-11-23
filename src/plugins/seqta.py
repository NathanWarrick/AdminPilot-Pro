import pyautogui
import time
import pynput

import src.functions as fnc

keyboard = pynput.keyboard.Controller()


def seqtacheck():
    if fnc.imagesearch(r"src\assets\seqta\logo.png") == [-1, -1]:
        print("[INFO] SEQTA not found")
        return False
    else:
        print("[INFO] SEQTA found")
        return True


def create_dm(name: str, dm_type: int):
    """_summary_

    :param name: The name of the student
    :type name: string
    :param dm_type: a value representing the recipients of the DM
    :type dm_type: int
    """

    # Check that the dm_type is valid
    if 1 <= dm_type <= 4:
        pass
    else:
        print("[ERROR] DM Student Error: " + str(dm_type) + " is not a valid option")
        print(
            "[INFO] 1 - DM Student\n2 - DM Guardians\n3 - DM Student and Guardians\n4 - DM Teachers"
        )
        exit()

    # Checking that SEQTA is open
    if seqtacheck() == False:
        exit()

    # Info message
    if dm_type == 1:
        recipients = "Student"
    elif dm_type == 2:
        recipients = "Parents"
    elif dm_type == 3:
        recipients = "Student and Parents"
    elif dm_type == 4:
        recipients = "Teachers"

    print("[INFO] Creating a DM for: " + name + "\n[INFO] Sending to: " + recipients)

    fnc.clickon(r"src\assets\seqta\sip\search.png", wait=0.2)

    keyboard.type(name)
    time.sleep(0.5)

    if fnc.imagesearch(r"src\assets\seqta\sip\nomatch.png", confidence=0.9) == [-1, -1]:
        print("[INFO] Student found")
    else:
        print("[INFO] Student Not Found")
        keyboard.tap(pynput.keyboard.Key.esc)
        return "NotFound"

    keyboard.tap(pynput.keyboard.Key.enter)

    # While loop to determine the SIP is loaded and can be interacted with
    # load = False
    # while load == False:  # Check if SIP has loaded
    #     if pyautogui.pixelMatchesColor(960, 582, (31, 49, 93)) == True:
    #         load == False
    #         print("[INFO] SIP not loaded")
    #         time.sleep(1)
    #     else:
    #         load == True
    #         print("[INFO] SIP loaded")
    #         try:
    #             fnc.clickon(r"src\assets\seqta\sip\general.png", wait=0.1)
    #             print("[INFO] Navigating to Overview")
    #         except:
    #             print("[INFO] Already on Overview")
    #         break

    load = False
    fnc.moveto(r"src\assets\seqta\sip\general.png")
    while fnc.imagesearch(r"src\assets\seqta\sip\generalnotes.png") == [-1, -1]:
        fnc.click_left(None, None)
        print("[INFO] SIP not loaded")
    print("[INFO] SIP loaded")

    # fnc.moveto(r"src\assets\seqta\sip\actions.png")
    # while load == False:
    #     fnc.click_left(None, None)
    #     if fnc.clickon(r"src\assets\seqta\sip\dmstudent.png", clicktype="none") != [
    #         -1,
    #         -1,
    #     ]:
    #         load = True
    fnc.clickon(r"src\assets\seqta\sip\actions.png", wait=0.5)
    if dm_type == 1:
        fnc.clickon(r"src\assets\seqta\sip\dmstudent.png", confidence=0.9)
    elif dm_type == 2:
        fnc.clickon(r"src\assets\seqta\sip\dmguardian.png", confidence=0.9)
    elif dm_type == 3:
        try:
            fnc.clickon(r"src\assets\seqta\sip\dmboth.png", confidence=0.9)
        except:
            return "NotFound"
    elif dm_type == 4:
        fnc.clickon(r"src\assets\seqta\sip\dmteachers.png", confidence=0.9)
    time.sleep(1)


def create_dm_adv(**kwargs):
    students = kwargs.get("students", None)
    staff = kwargs.get("staff", None)
    tutors = kwargs.get("tutors", None)
    guardians = kwargs.get("guardians", None)

    print("[INFO] Sending to Students: ")
    for x in students:
        print(x)
    print("\n[INFO] Sending to Staff:")
    for x in staff:
        print(x)
    print("\n[INFO] Sending to Tutors:")
    for x in tutors:
        print(x)
    print("\n[INFO] Sending to Guardians:")
    for x in guardians:
        print(x)

    fnc.clickon(r"src\assets\seqta\home.png")
    keyboard.press(pynput.keyboard.Key.alt)
    keyboard.type("m")
    keyboard.release(pynput.keyboard.Key.alt)
    time.sleep(1)

    fnc.clickon(r"src\assets\seqta\dm\selectstudent.png", wait=0.2)
    for x in students:
        time.sleep(0.3)
        keyboard.type(x)
        time.sleep(0.5)
        keyboard.tap(pynput.keyboard.Key.enter)
    keyboard.tap(pynput.keyboard.Key.esc)
    time.sleep(0.2)

    fnc.clickon(r"src\assets\seqta\dm\selectstaff.png", wait=0.2)
    for x in staff:
        time.sleep(0.3)
        keyboard.type(x)
        time.sleep(0.5)
        keyboard.tap(pynput.keyboard.Key.enter)
    keyboard.tap(pynput.keyboard.Key.esc)
    time.sleep(0.2)

    fnc.clickon(r"src\assets\seqta\dm\selecttutor.png", wait=0.2)
    for x in tutors:
        time.sleep(0.3)
        keyboard.type(x)
        time.sleep(0.5)
        keyboard.tap(pynput.keyboard.Key.enter)
    keyboard.tap(pynput.keyboard.Key.esc)
    time.sleep(0.2)

    fnc.clickon(r"src\assets\seqta\dm\selectguardian.png", wait=0.2)
    for x in guardians:
        time.sleep(0.3)
        keyboard.type(x)
        time.sleep(0.5)
        keyboard.tap(pynput.keyboard.Key.enter)
    keyboard.tap(pynput.keyboard.Key.esc)
    time.sleep(0.2)


def write_dm(subject: str, message: str, **kwargs):
    """Add contents to the SEQTA DM

    :param subject: The subject of the SEQTA message
    :type subject: string
    :param message: The body of the SEQTA message
    :type message: string
    :param filepath: The filepaths of any associated documents you would like attached
    :type filepath: string
    """
    filepath = []
    filepath = kwargs.get("filepath", None)

    fnc.clickon(r"src\assets\seqta\dm\subject.png")
    keyboard.type(subject)  # Write Subject
    keyboard.tap(pynput.keyboard.Key.tab)
    keyboard.tap(pynput.keyboard.Key.tab)
    keyboard.type(message)  # Write main Message

    if filepath == None:
        pass
    else:
        # print(len(filepath))
        for path in filepath:
            print("[INFO] Attaching: " + path)
            time.sleep(0.5)
            fnc.clickon(r"src\assets\seqta\dm\addfiles.png", wait=1, confidence=0.8)
            fnc.clickon(r"src\assets\seqta\dm\mydevice.png", wait=1, confidence=0.8)
            time.sleep(1)
            keyboard.type(path)
            keyboard.tap(pynput.keyboard.Key.enter)
            time.sleep(1)
    time.sleep(1)


def send_dm():
    """Send the SEQTA DM"""
    print("[INFO] Sending DM")
    fnc.clickon(r"src\assets\seqta\dm\send.png", confidence=0.9)
    time.sleep(1)
    fnc.clickon(r"src\assets\seqta\sip\clear.png")
    time.sleep(1)
    print("[INFO] Sent")
    print("-------------------------------------------------------\n")


def cancel_dm():
    fnc.clickon(r"src\assets\seqta\dm\cancel.png")
    print("[INFO] Canceled")
