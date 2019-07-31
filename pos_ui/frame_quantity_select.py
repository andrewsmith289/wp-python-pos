import os
import Tkinter
import tkFont


class Frame_Quantity_Select(Tkinter.Frame):

    output = ''

    def __init__(self, master=None, qty_max=None  , prod_id=False, prod_name=False, prod_quant=False, **kw):
        if not master:
            master = Tkinter.Tk()
        self.master = master
        Tkinter.Frame.__init__(self, master, **kw)

        self.heading_font = tkFont.Font(family="Times", size=14, weight=tkFont.NORMAL)
        self.entry_value_font = tkFont.Font(family="Times", size=22, weight=tkFont.NORMAL)
        self.keypad_font = tkFont.Font(family="Times", size=16, weight=tkFont.NORMAL)
        self.master.wm_title("Action Required")
        self.default_main_msg = "Subitem Package Scanned! (i.e. one eighth from an ounce)."
        self.default_details_msg = \
            "Key in remaining subitems to save time? \n\n" \
            "Either choose the number of packages you are adding to the tray, or " \
            "press the X button to skip."
        self.incomplete_error_msg = "You must provide a response, please try again."

        self.cur_value = 1
        self.qty_max = qty_max

        self.create_widgets()

    def isnumeric(self, why, where, what):
        try:
            val = int(what)
        except ValueError:
            return False
        return True

    def create_widgets(self):
        self.lbl_main = Tkinter.Label(
            self,
            text=self.default_main_msg,
            font=self.heading_font
        )
        self.lbl_main.grid(row=1, column=1, columnspan=3, sticky="W", padx=5, pady=5)

        self.lbl_details = Tkinter.Label(
            self,
            text=self.default_details_msg,
            justify="left"
        )
        self.lbl_details.grid(row=2, column=1, columnspan=3, sticky="W", padx=5, pady=5)

        # Value box
        keypress_validator = self.register(self.isnumeric)
        self.entry_value = Tkinter.Entry(
            self,
           # value=1,
            justify="center",
            font=self.entry_value_font,
            width=25,
            validate="key",
            validatecommand=(keypress_validator, '%d', '%i', '%S')
        )
        self.entry_value.insert(0, str(self.cur_value))
        self.entry_value.grid(row=3, column=1, columnspan=4, padx=5, pady=4)

        ########
        # Keypad Frame
        ########
        self.keypad_frame = Tkinter.Frame(self)
        self.keypad_frame.grid(row=4, column=1, columnspan=4, pady=2, sticky="")
        self.keypad_btn_w = 4
        self.keypad_btn_h = 2
        self.keypad_padx = 8
        self.keypad_pady = 8

        # Row 1
        self.btn_1 = Tkinter.Button(
            self.keypad_frame,
            text="1",
            font=self.keypad_font,
            width=self.keypad_btn_w,
            height=self.keypad_btn_h,
            command=lambda: self.keypad_press(1)
        )
        self.btn_1.grid(row=1, column=2, padx=self.keypad_padx, pady=self.keypad_pady)

        self.btn_2 = Tkinter.Button(
            self.keypad_frame,
            text="2",
            font=self.keypad_font,
            width=self.keypad_btn_w,
            height=self.keypad_btn_h,
            command=lambda: self.keypad_press(2)
        )
        self.btn_2.grid(row=1, column=3, padx=self.keypad_padx, pady=self.keypad_pady)

        self.btn_3 = Tkinter.Button(
            self.keypad_frame,
            text="3",
            font=self.keypad_font,
            width=self.keypad_btn_w,
            height=self.keypad_btn_h,
            command=lambda: self.keypad_press(3)
        )
        self.btn_3.grid(row=1, column=4, padx=self.keypad_padx, pady=self.keypad_pady)

        # Row 2
        self.btn_4 = Tkinter.Button(
            self.keypad_frame,
            text="4",
            font=self.keypad_font,
            width=self.keypad_btn_w,
            height=self.keypad_btn_h,
            command=lambda: self.keypad_press(4)
        )
        self.btn_4.grid(row=1, column=5, padx=self.keypad_padx, pady=self.keypad_pady)

        self.btn_5 = Tkinter.Button(
            self.keypad_frame,
            text="5",
            font=self.keypad_font,
            width=self.keypad_btn_w,
            height=self.keypad_btn_h,
            command=lambda: self.keypad_press(5)
        )
        self.btn_5.grid(row=2, column=2, padx=self.keypad_padx, pady=self.keypad_pady)

        self.btn_6 = Tkinter.Button(
            self.keypad_frame,
            text="6",
            font=self.keypad_font,
            width=self.keypad_btn_w,
            height=self.keypad_btn_h,
            command=lambda: self.keypad_press(6)
        )
        self.btn_6.grid(row=2, column=3, padx=self.keypad_padx, pady=self.keypad_pady)

        # Row 3
        self.btn_7 = Tkinter.Button(
            self.keypad_frame,
            text="7",
            font=self.keypad_font,
            width=self.keypad_btn_w,
            height=self.keypad_btn_h,
            command=lambda: self.keypad_press(7)
        )
        self.btn_7.grid(row=2, column=4, padx=self.keypad_padx, pady=self.keypad_pady)

        self.btn_8 = Tkinter.Button(
            self.keypad_frame,
            text="8",
            font=self.keypad_font,
            width=self.keypad_btn_w,
            height=self.keypad_btn_h,
            command=lambda: self.keypad_press(8)
        )
        self.btn_8.grid(row=2, column=5, padx=self.keypad_padx, pady=self.keypad_pady)

        self.btn_9 = Tkinter.Button(
            self.keypad_frame,
            text="9",
            font=self.keypad_font,
            width=self.keypad_btn_w,
            height=self.keypad_btn_h,
            command=lambda: self.keypad_press(9)
        )
        self.btn_9.grid(row=3, column=2, padx=self.keypad_padx, pady=self.keypad_pady)

        # Row 4
        self.btn_0 = Tkinter.Button(
            self.keypad_frame,
            text="0",
            font=self.keypad_font,
            width=self.keypad_btn_w,
            height=self.keypad_btn_h,
            command=lambda: self.keypad_press(0)
        )
        self.btn_0.grid(row=3, column=3, padx=self.keypad_padx, pady=self.keypad_pady)

        self.btn_clr = Tkinter.Button(
            self.keypad_frame,
            text="CLR",
            font=self.keypad_font,
            width=self.keypad_btn_w,
            height=self.keypad_btn_h,
            command=lambda: self.keypad_press("C")
        )
        self.btn_clr.grid(row=3, column=4, padx=self.keypad_padx, pady=self.keypad_pady)

        self.btn_del = Tkinter.Button(
            self.keypad_frame,
            text="DEL",
            font=self.keypad_font,
            width=self.keypad_btn_w,
            height=self.keypad_btn_h,
            command=lambda: self.keypad_press("D")
        )
        self.btn_del.grid(row=3, column=5, padx=self.keypad_padx, pady=self.keypad_pady)

        self.img_x = Tkinter.PhotoImage(file=self.get_resource_path("red_x_64.gif"))
        self.btn_no = Tkinter.Button(
            self.keypad_frame,
            borderwidth="0",
            image=self.img_x,
            width=64,
            height=64,
            command=lambda: self.btn_x_press()
        )
        self.btn_no.grid(row=2, column=1, padx=64, pady=2)

        self.img_check = Tkinter.PhotoImage(file=self.get_resource_path("green_check_64.gif"))
        self.btn_yes = Tkinter.Button(
            self.keypad_frame,
            borderwidth="0",
            image=self.img_check,
            width=64,
            height=64,
            command = lambda: self.btn_check_press()
        )
        self.btn_yes.grid(row=2, column=6, padx=64, pady=2)

        self.grid()
        self.pristine = True

    def center(self, toplevel):
        toplevel.update_idletasks()
        w = toplevel.winfo_screenwidth()
        h = toplevel.winfo_screenheight()
        size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
        x = w / 2 - size[0] / 2
        y = h / 2 - size[1] / 2
        toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

    def get_resource_path(self, resource):
        dir = os.path.dirname(__file__)
        resources_path = os.path.join(dir, 'resources', resource)
        return resources_path

    def keypad_press(self, value):
        cur = self.cur_value

        if value is "C":
            self.entry_value.delete(0, "end")
            self.entry_value.insert(0, "0")
            self.cur_value = 0
        elif value is "D":
            if cur <= 1:
                self.cur_value = 0
            else:
                self.cur_value = int(str(self.cur_value)[:-1])

            self.entry_value.delete(0, "end")
            self.entry_value.insert(0, self.cur_value)
        else:
            if not self.isnumeric(None, None, value):
                return
            cur = self.cur_value
            out = ""
            if cur is not 0 and not self.pristine:
                out += str(cur)
            out += str(value)
            self.entry_value.delete(0, "end")
            self.entry_value.insert(0, out)
            self.cur_value = int(out)

        if self.cur_value > self.qty_max:
            self.entry_value.delete(0, "end")
            self.entry_value.insert(0, self.cur_value)

        self.pristine = False

    def btn_check_press(self):
        self.output = self.cur_value
        self.quit()

    def btn_x_press(self):
        self.output = 1
        self.quit()

    def get_quantity_selection(self):
        self.mainloop()
        return self.output
