from Tkinter import *
from SharedUtilities import printt
from pos_ui.frame_actions import Frame_Actions
from pos_ui.frame_product import Frame_Product
from tkFont import Font


class Frame_Order(Frame):

    VFILL = (N, S)
    HFILL = (E, W)
    AFILL = (N, S, E, W)

    def __init__(self, master=None, order_data=None, width=800, height=480, **kwargs):
        if master is None:
            master = Tk()
        self.master = master
        Frame.__init__(self, self.master)

        self.grid(sticky=W + E + N + S)
        self.config(bg="red")

        # Force master window size to touchscreen resolution
        self.master.geometry('{}x{}'.format(width, height))
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(0, weight=1)
        self.master.config(bg="blue")

        # Configure Order Data rows & columns
        self.grid_columnconfigure(3, weight=3)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=2)
        self.grid_rowconfigure(2, weight=1)

        # Fonts
        self.label_heading_font = Font(size=10, weight="bold", underline=1)
        self.label_font = Font(size=10, underline=1)
        self.list_item_font = Font(size=12, weight=NORMAL)

        # Fields and label padding
        self.field_pad_x_sm = 4
        self.field_pad_y_sm = 4
        self.lbl_pad_x = 4
        self.lbl_pad_y = 4

        self.order_item_index = 0
        self.order_data = order_data

    def load_data(self, order_data):
        if not len(order_data):
            printt("OrderInfoFrame.load_order: valid order_data must be provided.")
            raise IndexError("Order data must be provided.")

        # Order Data defaults
        self.order_note = "None provided."
        self.quantity = 0
        self.packs_remaining = 0
        self.customer = {}

        # Load Order information
        self.id = str(order_data["id"])
        self.status = str(order_data["status"])
        self.date_created = str(order_data["date_created"])
        self.value = str(order_data["total"])
        self.customer_note = str(order_data["customer_note"])
        self.signature_waived = order_data["delivery_signature"]

        # Load the Customer information
        self.customer["first_name"] = str(order_data["customer"]["first_name"])
        self.customer["last_name"] = str(order_data["customer"]["last_name"])
        self.customer["full_name"] = str(
            self.customer["first_name"] + " " + self.customer["last_name"])
        self.customer["phone"] = str(order_data["customer"]["phone"])
        self.customer["email"] = str(order_data["customer"]["email"])
        self.customer["address_1"] = str(order_data["customer"]["address_1"])
        self.customer["address_2"] = str(order_data["customer"]["address_2"])
        self.customer["city"] = str(order_data["customer"]["city"])
        self.customer["state"] = str(order_data["customer"]["state"])
        self.customer["postcode"] = str(order_data["customer"]["postcode"])
        self.customer["country"] = str(order_data["customer"]["country"])

        # Create Fields
        self.lbl_order_num = Label(
            self,
            text="Order# " + self.id,
            font=Font(size=14, weight="bold", underline=1),
            anchor=W
        )
        self.lbl_order_num.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=self.field_pad_x_sm,
            pady=(self.field_pad_y_sm, 0),
            sticky=W
        )

        ###
        # Creation date
        ###
        self.lbl_created = Label(
            self,
            text="Received " + self.extract_date(self.date_created)
        )
        self.lbl_created.grid(
            row=1,
            column=0,
            padx=self.field_pad_x_sm,
            pady=self.field_pad_y_sm,
            sticky=W
        )

        ##
        # Status
        ##
        self.order_status_field = Label(
            master=self,
            text="-" + str.upper(self.status) + "-"
        )
        self.order_status_field.grid(
            row=1,
            column=1,
            padx=self.field_pad_x_sm * 1.5,
            pady=self.field_pad_y_sm
        )

        #######
        # Inner frame_cust_info
        #######
        self.frame_cust_info = Frame(
            master=self,
            border=2,
            relief=GROOVE
        )
        self.frame_cust_info.grid(
            row=2,
            rowspan=2,
            column=0,
            padx=(self.field_pad_x_sm, 0),
            sticky="wens"
        )
        self.frame_cust_info.grid_columnconfigure(0, weight=1)

        self.lbl_cust_info_heading = Label(
            master=self.frame_cust_info,
            text="Customer Info",
            font=self.label_heading_font,
        )
        self.lbl_cust_info_heading.grid(
            row=0,
            column=0,
            padx=self.field_pad_x_sm,
            pady=self.field_pad_y_sm,
            sticky=W+E+N+S
        )

        ####
        # Customer Address Frame
        ####
        self.frame_cust_info.address = Frame(
            master=self.frame_cust_info,
            borderwidth=2,
            relief=GROOVE
        )
        self.frame_cust_info.address.grid(
            row=1,
            column=0,
            padx=self.field_pad_x_sm,
            pady=self.field_pad_y_sm,
            sticky=W+E
        )
        frame_cust_addr = self.frame_cust_info.address

        ##
        # Full Name
        ##
        self.name_field = Label(
            master=frame_cust_addr,
            text=self.customer["full_name"],
            anchor=W
        )
        self.name_field.grid(
            row=0,
            column=0,
            padx=self.field_pad_x_sm,
            pady=self.field_pad_y_sm,
            sticky=W
        )

        ##
        # Address
        ##
        self.address_field = Label(
            master=frame_cust_addr,
            text=self.customer["address_1"],
        )
        self.address_field.grid(
            row=1,
            column=0,
            padx=self.field_pad_x_sm,
            pady=self.field_pad_y_sm)

        ##
        # Address Line 2
        ##
        text = str(self.customer["address_2"])

        if self.customer["address_2"] is not "":
            self.address2_field = Label(
                master=frame_cust_addr,
                text=text,
            )
            self.address2_field.grid(
                row=2,
                column=0,
                padx=self.field_pad_x_sm,
                pady=self.field_pad_y_sm
            )

        ###
        # City, State
        ###
        the_row = 3
        if self.customer["address_2"] is not "":
            the_row = 2

        self.city_state_field = Label(
            master=frame_cust_addr,
            text=self.customer["city"] + ", " + self.customer["state"],
            anchor=W
        )
        self.city_state_field.grid(
            row=the_row,
            column=0,
            padx=self.field_pad_x_sm,
            pady=self.field_pad_y_sm,
            sticky=W+E
        )

        ###############################
        # Outer Order Note Container  #
        ###############################
        self.frame_order_note_container = Frame(
            self.frame_cust_info,
            border=2,
            relief=GROOVE,
        )
        self.frame_order_note_container.grid(
            row=2,
            column=0,
            padx=self.field_pad_x_sm,
            pady=self.field_pad_y_sm,
            sticky=W+E
        )

        ###
        # Order Note Frame
        ###
        self.frame_order_note = Frame(
            self.frame_order_note_container,
            border=2,
            relief=GROOVE,
        )
        self.frame_order_note.grid(
            row=2,
            column=0,
            padx=self.field_pad_x_sm,
            pady=self.field_pad_y_sm,
            sticky=W+E+N+S
        )

        self.order_note_label = Label(
            master=self.frame_order_note_container,
            text="Order Note",
            font=self.label_heading_font,
        )
        self.order_note_label.grid(
            row=0,
            column=0,
            padx=self.field_pad_x_sm,
            pady=self.field_pad_y_sm,
            sticky=W+E
        )

        self.order_note_field = Label(
            master=self.frame_order_note,
            text=self.order_note,
        )
        self.order_note_field.grid(
            row=3,
            column=0,
            padx=self.field_pad_x_sm,
            pady=self.field_pad_y_sm,
            sticky=S+N+E+W
        )

        ##
        # Signature on Delivery Opt-out
        ##
        text = "--SIGNATURE REQUIRED--"
        color = "green"
        if self.signature_waived:
            text = "--NO SIGNATURE REQ.--"
            color = "red"
        self.lbl_sig_delivery = Label(
            self,
            text=text,
            font=self.label_heading_font,
            fg=color
        )
        self.lbl_sig_delivery.grid(
            row=1,
            column=2,
            padx=self.field_pad_x_sm,
            pady=self.field_pad_y_sm
        )

        ##########################
        # Order Items List Frame #
        ##########################
        self.frame_items_list = Frame(
            self
        )
        self.frame_items_list.config(bg="green")
        self.frame_items_list.grid(
            row=2,
            column=1,
            rowspan=2,
            columnspan=2,
            sticky=N+E+W+S
        )
        self.frame_items_list.grid_columnconfigure(0, weight=1)

        #####
        # Order Items heading
        #####
        self.order_items_label = Label(
            master=self.frame_items_list,
            text="Order Items",
            font=self.label_heading_font,
            anchor=W
        )
        self.order_items_label.grid(
            row=2,
            column=0,
            padx=self.field_pad_x_sm,
            pady=self.field_pad_y_sm,
            sticky=W
        )

        ##
        # Items Scrollbar
        ##
        self.items_scrollbar = Scrollbar(self.frame_items_list)
        self.items_scrollbar.grid(
            row=3,
            column=1,
            padx=(0),
            pady=(0, self.field_pad_y_sm),
            sticky=N+S+W
        )

        ####
        # Items Listbox
        #####
        self.items_listbox = Listbox(
            master=self.frame_items_list,
            font=self.list_item_font,
            selectmode=SINGLE,
            yscrollcommand=self.items_scrollbar.set,
            width=52
        )
        self.items_listbox.grid(
            row=3,
            column=0,
            padx=(self.field_pad_x_sm, 0),
            pady=(0, self.field_pad_y_sm),
            sticky=W+E+N+S
        )
        self.items_scrollbar.config(command=self.items_listbox.yview)
        self.frame_items_list.grid_rowconfigure(3, weight=1)
        self.frame_items_list.grid_rowconfigure(0, weight=1)

        #####
        # Item Info Container
        #####
        self.frame_order_item_info = Frame_Product(
            master=self.frame_items_list,
            item_data=order_data["line_items"][self.order_item_index],

            border=2,
            relief=GROOVE,

        )
        self.frame_order_item_info.grid(
            row=0,
            column=0,
            columnspan=2,
            pady=(0, 4),
            sticky=W+E+N+S
        )
        self.frame_order_item_info.config(bg="orange")

        # process new listbox selections
        self.items_listbox.bind('<<ListboxSelect>>', self.get_selection)
        self.fill_listbox(order_data["line_items"])

        #############################
        # Actions Toolbox Container #
        #############################
        self.frame_actions_toolbox = Frame_Actions(self.id, master=self)
        self.frame_actions_toolbox.grid(
            row=2, rowspan=2, column=3, sticky=W+E+N+S)

        self.frame_actions_toolbox.config(bg="green")

        # Stretch actions container to height and width available
        self.frame_actions_toolbox.rowconfigure(0, weight=1)
        self.frame_actions_toolbox.rowconfigure(1, weight=1)
        self.frame_actions_toolbox.columnconfigure(0, weight=1)

        self.mainloop()

    def get_selection(self, event=None):
        try:
            selection = self.items_listbox.curselection()[0]
            printt(selection)
            # Load selected Order data
            self.frame_order_item_info.load_data(
                self.order_data["line_items"][selection])
            return int(selection)
        except TypeError:
            printt("There was an issue getting the listbox selection index.")
            return 0

    @staticmethod
    def extract_date(datetime):
        date = str(datetime).split('-', 2)
        if len(date) == 3:
            # strip time component
            date[2] = date[2].split("T", 1)
            date = date[0] + "/" + date[1] + "/" + date[2][0]
        else:
            date = "<Err>"
        return date

    def fill_listbox(self, with_item_data):
        count = 1
        for item in with_item_data:
            id = str(item["product_id"])
            # vid = str(item["variation_id"])
            sku = str(item["sku"])
            name = str(item["name"])
            self.items_listbox.insert(
                END, str(count) + ") " + sku + "(" + id + ") - " + name)
            count += 1
            if self.items_listbox.size > 0:
                self.items_listbox.select_set(0, 0)
