import time
import pynput
import os

import src.functions as fnc
import src.connectors as con

keyboard = pynput.keyboard.Controller()
curr_working_dir = os.getcwd()

con.dm_timetable(
    "Updated Headstart Timetable",
    "Good Morning, \n\
Find attached an updated headstart timetable, if your timetable hasn't changed you can ignore this message\n\
If you have any issues please contact your co-ordinators.",
    1,
    True,
)
