import os
import threading
import sys
import Tkinter
import types
import SharedUtilities as utils
import Order
import Product
import UsbCamera
import Buzzer
from WPRestInterface import WPRestInterface
from pos_ui import frame_quantity_select

# try:
#     import curses
# except ImportError, NameError:
#     pass

from config import SCANNER_CONFIG


class Scanner(object):
    DATA_COLS = SCANNER_CONFIG['DEFAULT_DATA_COLS']
    STATES = SCANNER_CONFIG['SYS_STATES']

    buzzer = None
    usb_camera = None

    state = "OFF"  # This system's initial state

    wp_rest_interface = None

    cur_order = None

    last_scan_data = {}
    scan_cooldown = False
    cooldown_squelch = False

    silent_mode = False
    debug = True

    def __init__(self, api_creds, frame_order_info):
        self.wp_rest_interface = WPRestInterface(
            wcapi=api_creds["wcapi"], wpapi=api_creds["wpapi"])
        self.usb_camera = UsbCamera.UsbCamera(
            os.getcwd() + "/captures/", resolution=(1920, 1080))
        self.usb_camera.remove_old_captures(days_old=3)
        self.buzzer = Buzzer.Buzzer(pin=18)
        self.photo_only_mode = False
        self.set_state("READY")
        self.frame_order_info = frame_order_info

    def create_listener_thread(self):
        pass
        # Collect events until released
        # with Listener(
        #         on_press=self.on_key_press,
        #         on_release=self.on_key_release) as listener:
        #     listener.join()

    def on_key_press(self, key):
        pass
        # if key is Key.f2:
        #     self.photo_only_mode = not self.photo_only_mode

    def on_key_release(self, key):
        pass
        # print('{0} release'.format(key))
        # if key == Key.esc:
        #     # Stop listener
        #     return False

    def buzz(self, millis=1000):
        self.buzzer.buzz(millis)

    def process_qr_data(self, data):
        if not data:
            utils.printt("process_qr_data: data must be provided.")
            return False
        elif utils.is_valid_tracking(data):
            return {"track_num": data}
        elif not data[0].isalpha():  # valid order / product data has an alpha char at pos. 0
            return {"Error": "Unexpected data format."}
        elif data.count(','):
            ids = data.split(',')
            if ('p' == ids[0][0]) and ('v' == ids[1][0]):
                return {"product_id": ids[0][1:], "variation_id": ids[1][1:]}
        elif data[0] == 'o':
            return {"order_id": data[1:]}
        else:
            return {"Error": "Unable to parse the data."}

    def take_order_snapshot(self):
        utils.printt("Say cheese!")
        order_id = self.cur_order.order_id
        img_path = self.usb_camera.save_image(
            "order " + str(order_id), "order " + str(order_id))
        self.cur_order.set_image(img_path)

    def t_stop_cooldown(self):
        utils.printt('Thread called to turn off cooldown')
        self.scan_cooldown = False
        self.cooldown_squelch = False
        sys.exit()

    def on_scan_cooldown(self, last_data):
        utils.printt("Last scan data:")
        utils.printt(self.last_scan_data)
        utils.printt("Last data:")
        utils.printt(last_data)
        utils.printt("State:")
        utils.printt(self.get_state())

        if self.get_state() not in ["READY", "ORDER_FILL"]:
            return False
        elif self.scan_cooldown and self.last_scan_data == last_data:
            return True

        return False

    def get_state(self):
        return self.state

    def set_state(self, state):
        state = str(state).upper()
        if state in self.STATES:
            utils.printt("State Change: " + self.get_state() + "->" + state)
            self.state = state

    def process_scan_event(self, data):
        qr_data = self.process_qr_data(data)
        if self.on_scan_cooldown(data):
            utils.printt("----Scan Cooldown----")
            self.last_scan_data = {}
            return
        elif self.last_scan_data == data:
            self.scan_cooldown = True
            # spawn a thread to reset the cooldown after x seconds
            threading.Timer(5, self.t_stop_cooldown).start()
            self.last_scan_data = {}
            return

        self.last_scan_data = data

        state = self.get_state()
        if "READY" == state:
            if "order_id" not in qr_data:
                utils.printt(
                    "Order data not found in scan data. Please try again.")
                self.do_negative_feedback()
                return
            self.cur_order = Order.Order.load_order(
                self.wp_rest_interface,
                qr_data["order_id"],
                filter=self.DATA_COLS
            )
            utils.printt(self.wp_rest_interface.get_order_info(
                qr_data["order_id"]))
            self.frame_order_info.load_data(
                self.wp_rest_interface.get_order_info(qr_data["order_id"]))

            if not self.cur_order:
                utils.printt("Unable to load order data. Please try again.")
                return
            elif self.photo_only_mode:
                self.set_state("IMAGE_CAPTURE")
            else:
                utils.printt("----ORDER CONTENTS----")
                utils.printt(str(self.cur_order))
                self.set_state("ORDER_FILL")
        elif "ORDER_FILL" == state:
            utils.printt("----QR Data----")
            utils.printt(qr_data, True)

            if "product_id" not in qr_data or "variation_id" not in qr_data:
                utils.printt("Product and/or variation ids were not provided.")
                return

            index = self.cur_order.index_of(qr_data)
            if index == -1:
                self.do_negative_feedback()
                utils.printt("Scanned item not part of order")
                utils.printt(self.cur_order.order_items, pretty=True)
                return
            utils.printt("Item found in Order.")

            order_item = self.cur_order.order_items[index]
            if not order_item:
                utils.printt("Scanned item not part of order")
                return

            decrease_by = 1
            if order_item.packs_to_go > 1:
                mqs = frame_quantity_select.Frame_Quantity_Select(
                    master=Tkinter.Tk(), qty_max=3)
                decrease_by = mqs.get_quantity_selection()
                utils.printt("Quantity Select Choice: " + str(decrease_by))

                if type(decrease_by) is not int:
                    utils.printt("There was a problem retrieving the user's choice for the "
                                 "Quantity Select UI. Defaulting to 1.")
                    decrease_by = 1

            self.cur_order.decrease_item_quantity(qr_data, amount=decrease_by)
            if self.cur_order.is_empty():
                utils.printt("Last item scanned!")
                self.take_order_snapshot()
                self.set_state("WAIT_TRACKING")

        elif "IMAGE_CAPTURE" == state:
            self.take_order_snapshot()
            self.set_state("DONE_ORDER")

        elif "WAIT_TRACKING" == state:
            if utils.is_valid_tracking(data):
                self.cur_order.set_tracking(data)
                self.set_state("DONE_ORDER")
        elif "DONE_ORDER" == state:
            self.cur_order.set_status("completed")
            self.cur_order.save()
            msg = "Order filled."
            if self.photo_only_mode:
                msg = "Saved Order image."
            utils.printt(msg)
            self.set_state("READY")
        elif "ERROR" == state:
            utils.printt("An ERROR was encountered!")
        else:
            utils.printt("The system has entered an invalid state!")
        return

    def do_decoded_qr_feedback(self):
        if self.silent_mode:
            return
        utils.printt(
            "<Decoded QR Feedback: Flash Blue LED and Play Boop Sound>")

    def do_positive_feedback(self):
        if self.silent_mode:
            return
        utils.printt(
            "<Positive Feedback: Flash Green Light and Play Ding Sound>")

    def do_negative_feedback(self):
        if self.silent_mode:
            return
        utils.printt(
            "<Negative Feedback: Flash Orange Light and Play Buzz Sound>")
        self.buzz()

    def do_error_feedback(self):
        if self.silent_mode:
            return
        utils.printt(
            "<Error Cond. Feedback: Flash Red Light and Play Beep Sound>")
