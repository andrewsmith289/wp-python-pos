from Tkinter import *
from tkFont import *
from SharedUtilities import printt

from Product import Product


class Frame_Product(Frame):
    field_just = LEFT
    field_pad_x = (0, 0)
    field_pad_y = 4

    lbl_pad_x = 1
    lbl_pad_y = 4
    lbl_sticky = W
    lbl_anchor = W

    lbl_heading_padx = (0, 0)
    lbl_heading_pady = (4, 0)

    col0_pad = (0, 6)
    packs_remaining = 0

    def __init__(self, master=None, item_data=None, **kwargs):

        printt(item_data)
        if master is not None:
            self.master = master
        else:
            self.master = Tk()

        Frame.__init__(self, self.master, kwargs)
        self.grid(padx=(0, 0), pady=4, sticky=W+E+N+S)
        self.grid_columnconfigure(0, weight=1, uniform="item_info")
        self.grid_columnconfigure(1, weight=1, uniform="item_info")

        # Fill down into parent
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(5, weight=1)

        self.label_heading_font = Font(size=10, underline=0)
        self.underline_heading_font = Font(size=10, underline=1)
        self.item_info_heading_font = Font(size=13, weight=NORMAL)
        self.frame_heading_font = Font(size=10, weight=BOLD, underline=1)

        self.product = Product(item_data)

        if item_data:
            self.load_data(item_data)

    def load_data(self, item_data):
        if type(item_data) is not DictionaryType:
            raise ValueError("Valid item_data dict is required")
        elif "line_items" in item_data:
            raise ValueError("Got Order data when expecting Item data")

        try:
            self.sku = item_data["sku"]
            self.name = item_data["name"]
            self.product_id = item_data["product_id"]
            self.variation_id = item_data["variation_id"]
            self.quantity = item_data["quantity"]
            printt("Quantity: " + str(item_data["quantity"]))
        except KeyError:
            printt("OrderItemInfoFrame.load_order: unable to locate keys in item_data.")
            return False
        self.product.packs_remaining = self.quantity

        ##
        # Name
        ##
        self.lbl_name = Label(
            self,
            text="Name",
            font=self.underline_heading_font
        )
        self.lbl_name.grid(
            row=0,
            column=0,
            pady=self.lbl_heading_pady,
            sticky=W+S
        )
        self.name_field = Label(
            self,
            text=self.name,
            font=self.item_info_heading_font,
            border=2,
            relief=GROOVE
        )
        self.name_field.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky=N+W+E+S
        )

        ##
        # SKU
        ##
        self.lbl_sku = Label(
            self,
            text="SKU",
            font=self.underline_heading_font
        )
        self.lbl_sku.grid(
            row=2,
            column=1,
            padx=self.lbl_heading_padx,
            pady=self.lbl_heading_pady,
            sticky=self.lbl_sticky
        )
        self.sku_field = Label(
            self,
            text=self.sku,
            font=self.item_info_heading_font,
            border=2,
            relief=GROOVE
        )
        self.sku_field.grid(
            row=3,
            column=1,
            sticky=N+S+W+E
        )

        ##
        # Product_id
        ##
        self.lbl_pid = Label(
            self,
            text="Product ID",
            font=self.underline_heading_font
        )
        self.lbl_pid.grid(
            row=2,
            column=0,
            padx=self.lbl_heading_padx,
            pady=self.lbl_heading_pady,
            sticky=N+W+S
        )

        self.pid_field = Label(
            self,
            text=self.product_id,
            font=self.item_info_heading_font,
            border=2,
            relief=GROOVE
        )
        self.pid_field.grid(
            row=3,
            column=0,
            padx=self.col0_pad,
            sticky=W+N+E+S
        )

        ##
        # Variation_id
        ##
        self.lbl_vid = Label(
            self,
            text="Variation ID",
            font=self.underline_heading_font,
        )
        self.lbl_vid.grid(
            row=4,
            column=0,
            padx=self.lbl_heading_padx,
            pady=self.lbl_heading_pady,
            sticky=W
        )
        self.vid_field = Label(
            self,
            text=self.variation_id,
            font=self.item_info_heading_font,
            border=2,
            relief=GROOVE
        )
        self.vid_field.grid(
            row=5,
            column=0,
            padx=self.col0_pad,
            # pady=self.field_pad_y,
            sticky=W+E+N+S
        )

        # ##
        # # Quantity
        # ##
        # self.lbl_quant = Label(
        #     self,
        #     text="Total Quantity",
        #     font=self.underline_heading_font
        # )
        # self.lbl_quant.grid(
        #     row=4,
        #     column=1,
        #     padx=self.lbl_heading_padx,
        #     pady=self.lbl_heading_pady,
        #     sticky=self.lbl_sticky
        # )
        # self.quant_field = Label(
        #     self,
        #     text=self.quantity,
        #     font=self.item_info_heading_font,
        #     border=2,
        #     relief=GROOVE
        # )
        # self.quant_field.grid(
        #     row=5,
        #     column=1,
        #     sticky=W+E
        # )

        ##
        # Remaining Packs
        ##
        self.lbl_remaining = Label(
            self,
            text="Packs to Go",
            font=self.underline_heading_font,
            anchor=W,
        )
        self.lbl_remaining.grid(
            row=4,
            column=1,
            padx=self.lbl_heading_padx,
            pady=self.lbl_heading_pady,
            sticky=self.lbl_sticky
        )
        self.remaining_field = Label(
            self,
            text=self.product.packs_remaining,
            font=self.item_info_heading_font,
            border=2,
            relief=GROOVE
        )
        self.remaining_field.grid(
            row=5,
            column=1,
            sticky=W+E+N+S
        )
