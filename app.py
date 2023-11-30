import time
import pynput
import os

import src.functions as fnc
import src.connectors as con

keyboard = pynput.keyboard.Controller()
curr_working_dir = os.getcwd()

# con.dm_timetable(
#     "Updated Headstart Timetable",
#     "Good Morning, \n\
# Find attached your 2024 timetable!\n\
# If you have any issues please contact your co-ordinators.",
#     1,
#     False,
# )
