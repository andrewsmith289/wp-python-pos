from Tkinter import *
from tkFont import Font

from pos_globals import posSystem


class Frame_Actions(Frame):
    def __init__(self, order_id, master=None):
        if master is None:
            self.master = Tk()
        else:
            self.master = master

        self.order_id = abs(int(order_id))

        # Init master Frame
        Frame.__init__(self, self.master)
        self.grid(sticky=W + E + N + S)

        # Config column + row resizing
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Fonts
        self.actions_main_heading = Font(size=9, weight="bold")
        self.font_buttons = Font(size=8)

        # System Actions Frame
        frame_sys_act = Frame_System_Actions(
            order_id=self.order_id, master=self)
        frame_sys_act.grid(row=0, column=0, pady=(4, 8),
                           sticky=W+E+N+S)

        # Order Actions Frame
        frame_ord_act = Frame_Order_Actions(
            order_id=self.order_id, master=self)
        frame_ord_act.grid(row=1, column=0, sticky=W+E+N+S, pady=(2, 0))

        def skip_current_order(self):
            self.scanner.cur_order = None
            self.scanner.set_state("READY")
            pass

        def take_snapshot(self, complete_order=True):
            self.scanner.take_order_snapshot()
            pass


class Frame_System_Actions(Frame):

    def __init__(self, order_id, master=None):
        self.master = master
        if self.master is None:
            self.master = Tk()

        Frame.__init__(self, self.master, border=2, relief=GROOVE)
        self.grid(pady=(4, 8),
                  sticky=W + E + N + S)

        # Config cols/rows to center + resize
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Fonts
        self.sys_act_main_heading = Font(size=9, weight="bold")
        self.label_heading = Label(
            self,
            font=self.sys_act_main_heading,
            text="System Actions",
            anchor=CENTER
        )

        self.label_heading.grid(row=0, column=0, sticky=W + E + N)

        self.order_id = order_id


class Frame_Order_Actions(Frame):

    def __init__(self, order_id=None, master=None):
        if master is None:
            self.master = Tk()
        else:
            self.master = master

        Frame.__init__(self, self.master, border=2, relief=GROOVE)
        self.grid(pady=(0, 4), sticky=W+E+N+S)

        # Center columns + rows + resize
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # initialize fonts
        self.order_act_main_heading = Font(size=9, weight="bold")
        self.font_buttons = Font(size=8)

        if hasattr(self.master, "actions_main_heading"):
            self.order_act_main_heading = master.actions_main_heading
        if hasattr(self.master, "actions_button_font"):
            self.font_buttons = master.font_buttons

        ################
        # Main heading #
        ################
        self.label_main_heading = Label(
            self,
            font=self.order_act_main_heading,
            text="Order Actions"
        )
        self.label_main_heading.grid(
            row=0,
            column=0,
            pady=(4, 8),
            sticky=W+E+N
        )
        self.btn_take_img = Button(
            self,
            font=self.font_buttons,
            text="Take Order Image",
            command=self.take_order_image,
            anchor=CENTER
        )
        self.btn_take_img.grid(row=1, column=0, sticky=N)

    def take_order_image(self):
        posSystem.take_order_snapshot()
        pass


# def main():  # run mainnloop
#     root = Tk()
#     app = Frame_Actions(123, root)
#     root.mainloop()
#
#
# if __name__ == '__main__':
#     main()
