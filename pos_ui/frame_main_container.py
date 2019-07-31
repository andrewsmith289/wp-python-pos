# from Tkinter import *
# from SharedUtilities import printt
#
# from frame_order_info import Frame_Order_Info
# from frame_order_actions import Frame_Order_Actions
# from frame_system_actions import Frame_System_Actions
#
#
# class Frame_Main_Container(Frame):
#
#     def __init__(self, order_data, master=None, width=800, height=480):
#         if not order_data:
#             return
#         if master is not None:
#             self.master = master
#         else:
#             self.master = Tk()
#
#         Frame.__init__(self, self.master)
#         self.grid(sticky=N+E+S+W)
#         # self.rowconfigure(0, weight=1)
#         self.columnconfigure(0, weight=1)
#         # self.columnconfigure(1, weight=1)
#         # self.columnconfigure(2, weight=1)
#
#
#         #
#         # self.grid_columnconfigure()
#         # Force window dimensions to touchscreen resolution
#         self.master.geometry('{}x{}'.format(width, height))
#         self.master.config(bg="blue")
#         self.master.grid_columnconfigure(0, weight=1)
#
#         self.order_id = order_data["id"]
#
#         ####
#         # Order Info Frame
#         ####
#         self.frame_order_info = Frame_Order_Info(master=self, order_data=order_data)
#         self.frame_order_info.grid(
#             row=0,
#             padx=2,
#             column=0,
#             rowspan=2,
#             sticky=W+E+N+S
#         )
#         # self.frame_order_info.rowconfigure(0, weight=1)
#         # self.frame_order_info.columnconfigure(0, weight=1)
#         # self.frame_order_info.columnconfigure(1, weight=2)
#         # self.frame_order_info.columnconfigure(2, weight=1)
#         # self.frame_order_info.columnconfigure(3, weight=1)
#         # self.frame_order_info.columnconfigure(3, weight=1)
#
#         self.frame_order_info.config(bg="purple")
#
#
#
#
#     def set_active_order(self, order_items):
#         """
#         Adds the given order items to the
#         :param order_items:
#         :return:
#         """
#         pass
#
#
# def main():  # run mainnloop
#         root = Tk()
#         app = Frame_Main_Container(order_data=None)
#         root.mainloop()
#
# if __name__ == '__main__':
#     main()
