import os
from typing import Union
from Product import Product
from SharedUtilities import printt, is_valid_tracking, is_valid_item_scan
from WPRestInterface import WPRestInterface

from config import ORDER_CONFIG


class Order(object):

    wp_rest = None
    order_id = 0
    order_items = []
    image_path = None
    STATES = ORDER_CONFIG["ORDER_STATES"]
    state = ""
    status = ""
    tracking = ""

    def __init__(self, wp_rest_interface, data):
        self.wp_rest = wp_rest_interface
        self.order_id = data["order_id"]
        if "items" in data:
            for item in data["items"]:
                order_item = Product(item)
                self.add_item(order_item)
        self.set_state("OPEN")

    def __str__(self):
        NL = "\r\n"
        string = str(
            "Order " + self.order_id + NL +
            "    order_id: " + self.order_id + NL +
            "    state: " + self.state + NL +
            "    tracking: " + self.tracking + NL +
            "    items: [" + NL
        )
        for item in self.order_items:
            string += str(item) + NL
        string += "    ]" + NL
        string += "/>"

        return string

    def __len__(self):
        return len(self.order_items)

    @staticmethod
    def load_order(wp_rest_interface, order_id, filter=[]):
        # type: (WPRestInterface, int, dict) -> Order
        """
        :rtype: Order
        """
        order_items = wp_rest_interface.get_order_items(
            order_id,
            filter
        )
        if "error" in order_items:
            printt("An error occurred while loading the order: " +
                   str(order_items["error"]))
            return None
        data = {
            "order_id": order_id,
            "items": order_items
        }
        order = Order(wp_rest_interface, data)
        printt("----Loaded order " + str(order_id) + "----")

        return order

    def set_state(self, state):

        state = str(state).upper()
        if state in self.STATES:
            printt("Order State Change: " + self.state + "->" + state)
            self.state = state

    def set_tracking(self, code):
        if is_valid_tracking(code):
            self.tracking = code

    def set_status(self, status):
        if status not in ["completed"]:
            return False
        self.status = status

    def index_of(self, item):
        if type(item) is Product:
            for i, cur_item in enumerate(self.order_items):
                if item == cur_item:
                    return i
        elif type(item) is dict and is_valid_item_scan(item):
            for i, cur_item in enumerate(self.order_items):
                prod_id = cur_item.product_id
                if int(item["product_id"]) == prod_id:
                    var_id = cur_item.variation_id
                    cur_var_id = int(item["variation_id"])
                    if cur_var_id == 0 and var_id == 0:
                        return i
                    elif cur_var_id == var_id:
                        return i
            return -1

    def has_item(self, item):
        if -1 == self.index_of(item):
            return False
        return True

    def remove_item(self, item):
        index = self.index_of(item)
        if not index == -1:
            self.order_items.pop(index)
            self.update_order_items()
            return True
        else:
            return False

    def update_order_items(self):
        for item in self.order_items:
            if item.packs_remaining <= 0:
                printt("Finished filling items of this type. Removing.")
                self.remove_item(item)

    def decrease_item_quantity(self, qr_data, amount=1):
        index = self.index_of(qr_data)
        if index == -1:
            return False
        else:
            printt("Decreasing item quantity by " + str(amount))
            self.order_items[index].fill_packs(amount)
            self.update_order_items()
            return True

    def add_item(self, item):
        self.order_items.append(item)
        printt("Added item to order.")

    def is_empty(self):
        if 0 == len(self):
            return True
        return False

    def set_image(self, path):
        if not os.path.isfile(path):
            printt("The provided path is invalid.")
            return
        self.image_path = path

    def save(self):
        order_id = self.order_id
        if self.tracking:
            tracking = self.wp_rest.save_tracking(
                order_id,
                self.tracking
            )
            if tracking:
                printt("Saved Tracking Number")
            else:
                printt("Issue saving tracking number")

        if self.image_path:
            result = self.wp_rest.upload_order_image(
                order_id,
                self.image_path
            )
            printt(result)

        if self.status:
            data = {
                "status": str(self.status)
            }
            status = self.wp_rest.update_order(
                order_id,
                data
            )
            if status:
                printt("Updated Order Status")
            else:
                printt("Issue updating order status")

    # def get_items(self):
    #     return self.order_items
    #
    # def has_image(self):
    #     out = True
    #     if not self.image_path:
    #         out = False
    #     return out
    #
    # def has_tracking(self):
    #     if not self.get_tracking():
    #         return False
    #     else:
    #         return True
    #
    # def count(self):
    #     return len(self.order_items)
    #
    # def has_status(self):
    #
    #     if self.get_status():
    #         return True
    #     else:
    #         return False
    #
    # def get_tracking(self):
    #
    #     if not self.tracking:
    #         return False
    #
    #     return self.tracking
    # def get_status(self):
    #     return self.status
    #
    # def get_state(self):
    #     return self.state
