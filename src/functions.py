import csv, os, mss, cv2, pynput, time, win32api, win32con
import numpy as np

import src.plugins.seqta as sqt
import src.plugins.edval as edv

keyboard = pynput.keyboard.Controller()
curr_working_dir = os.getcwd()


def click_left(x, y):
    if x is not None and y is not None:
        win32api.SetCursorPos((x, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
    else:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def click_right(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, x, y, 0, 0)


def kbd_type(text: str):
    """Use pynput to enter text

    :param text: Text to enter on keyboard
    :type text: str
    """
    keyboard.type(text)


def moveto(image: str, confidence=0.9, wait=0.1):
    found = False
    i = 0
    while found == False:
        if i == 30:
            raise RuntimeError("Unable to find image in the 30 second window")
        coordds = imagesearch(image, confidence=confidence)
        i += 1
        time.sleep(1)
        if coordds != [-1, -1]:
            found = True
            win32api.SetCursorPos((int(coordds[0]), int(coordds[1])))


def clickon(image: str, confidence=0.9, clicktype="left", wait=0.1):
    found = False
    i = 0
    while found == False:
        if i == 2 and found == False:
            win32api.SetCursorPos((0, 1025))
        coordds = imagesearch(image, confidence=confidence)
        i += 1
        time.sleep(1)

        if i == 10:
            raise RuntimeError("Unable to find image in the 10 second window")

        if coordds != [-1, -1]:
            found = True
            if clicktype == "left":
                click_left(int(coordds[0]), int(coordds[1]))
            elif clicktype == "right":
                click_right(int(coordds[0]), int(coordds[1]))
            elif clicktype == "none":
                continue
            time.sleep(wait)


def imagesearch(image: str, confidence=0.9):
    with mss.mss() as sct:
        im = sct.grab(sct.monitors[0])
        img_rgb = np.array(im)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(image, 0)
        if template is None:
            raise FileNotFoundError("Image file not found: {}".format(image))
        template.shape[::-1]

        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if max_val < confidence:
            return [-1, -1]

        # Do some math to calculate the middle of the image
        templatesize = tuple(
            ti / 2 for ti in template.shape
        )  # Find the size of the template image and divide by 2

        # Convert H/W to W/H
        templatesize = list(templatesize)
        templatesize[0], templatesize[1] = templatesize[1], templatesize[0]

        # Calculate the middle of the image
        coords = tuple(
            map(lambda i, j: i + j, max_loc, templatesize)
        )  # Add the best match to half the image size to find the middle

    return coords


def imagecheck(image: str):
    """Continues to try to load an image until it successfully loads

    :param image: path to image to search for
    :type image: str
    """
    load = False
    i = 0
    while load == False:
        if imagesearch(image) == [-1, -1]:
            load == False
            print("[INFO] " + image + " not found")
            i = i + 1
            time.sleep(1)
        else:
            load == True
            print("[INFO] " + image + " found")
            break


def csv_export(export_list: list, path: str):
    with open(path, "w", newline="") as file:
        writer = csv.writer(file)

        # writer.writerow(["First Name", "Last Name"])

        for name in export_list:
            lastname = name.split(",")[0]
            firstname = name.split(",")[1].strip()
            print(firstname + " " + lastname)

            writer.writerow([firstname, lastname])


def csv_import(path: str):
    firstnames = []
    lastnames = []

    with open(path, newline="") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=",", quotechar="|")
        for row in spamreader:
            firstnames.append(row[0])
            lastnames.append(row[1])

    # i = 0
    # for firstname in firstnames:
    #     print(firstnames[i] + " " + lastnames[i])
    #     i += 1

    return firstnames, lastnames
