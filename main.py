from tkinter import *
import sqlite3
from app_interface import AppInterface
from sql_manager import SqlManager

# todo errors should be saved to logfile

# Create an example database table
sql_m = SqlManager()
try:
    sql_m.sql_create_exam_database("example_exam_database")
    print("Example Table Was Created")
except sqlite3.OperationalError as oe:
    print("sqlite3.OperationalError occurred: " + str(oe))

# ===== Main =====
root = Tk()
root.title("SQL Exam Simulator")
gui_w = AppInterface(root)
gui_w.gui_main_menu(root)
AppInterface().set_up_settings()
root.mainloop()
