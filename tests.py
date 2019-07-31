from pos_ui.frame_order import Frame_Product
from pos_ui.frame_order import Frame_Order
import sys
from pos_ui import frame_quantity_select
from woocommerce import API as WCAPI
from WPRestInterface import WPRestInterface

from wordpress import API
import os
from Scanner import Scanner
import Tkinter
from config import SCANNER_CONFIG

import SharedUtilities

import config_dev

sys.path.append('C:/Users/Andrew/Desktop/xxxxx/requests-oauth2/')

consumer_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxx"
consumer_secret = "xxxxxxxxxxxxxxxxxxxxxxxxx"

api = None
order_id = 0
pos_system = None


def test_order_item_info_frame():

    posSystem = Scanner(config_dev.CONFIG)
    order_data = posSystem.wp_rest_interface.get_order_info(order_id)
    print order_data

    item_info_frame = Frame_Product(
        master=Tkinter.Tk(), item_data=order_data["line_items"][0])
    item_info_frame.mainloop()
# test_order_item_info_frame()


def test_order_info_frame():

    posSystem = Scanner(config_dev.CONFIG)
    order_info = posSystem.wp_rest_interface.get_order_info(order_id)
    print order_info

    order_info_frame = Frame_Order(master=Tkinter.Tk(), order_data=order_info)
    order_info_frame.mainloop()


def test_add_order_note():
    posSystem.wp_rest_interface.add_order_note(order_id, "he's a fungi")


test_add_order_note()

# def test_main_container_frame():
#     print "testing 1.2.3"
#     print None in (2, "5", None)
#     posSystem = Scanner(config_dev.CONFIG)
#     order_data = posSystem.wp_rest_interface.get_order_info(order_id)
#     main_frame = Frame_Main_Container(order_data, master=Tkinter.Tk())
#     main_frame.mainloop()


def test_quantity_select():
    mqs = frame_quantity_select.Frame_Quantity_Select(
        master=Tkinter.Tk(), qty_max=3)
    q = mqs.get_quantity_selection()
    print "quantity select output: " + str(q)


def test_upload_order_image():
    payload = os.path.dirname(
        os.path.abspath(
            os.path.realpath(__file__)
        )
    ) + os.sep + 'tests_res' + os.sep

    SharedUtilities.printt(payload)
    pos_system.wp_rest_interface.upload_order_image(
        order_id, payload + 'smiley.jpg')


# test_upload_order_image()

def test_new_post(self, wpapi):
    WPRestInterface
    data = {
        "title": "hello"
    }
    #r = requests.post("posts/", data, oauth1=True)
    r = wpapi.post("posts/", data)

    print r

    result = False
    if r.status_code == 404:
        result = {"error": "404"}
    elif r.status_code == 200:
        result = True
    else:
        result = {"error": "unexpected error."}

    # printt(r.json(), True)

    return result

# def restart_program():
#     """Restarts the current program.
#     Note: this function does not return. Any cleanup action (like
#     saving data) must be done before calling this function."""
#     py = sys.executable
#     os.execl(py, py, * sys.argv)

# api.oauth2.get_new_auth_token()


def main():  # run mainloop
    test_order_info_frame()
    # test_order_item_info_frame()
    # test_main_container_frame()
    # test_quantity_select()


if __name__ == '__main__':
    main()
