import time
import pynput
import os

import src.functions as fnc
import src.connectors as con

keyboard = pynput.keyboard.Controller()
curr_working_dir = os.getcwd()

con.dm_timetable("", "", False)
