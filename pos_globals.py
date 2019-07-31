from Tkinter import Tk

from Scanner import Scanner
from config_dev import CONFIG
from pos_ui.frame_order import Frame_Order

frame_order_info = Frame_Order(Tk())

posSystem = Scanner(CONFIG, frame_order_info)
