from wordpress import api
import sys
from os import path, name
from SharedUtilities import printt
if name is 'nt':
    sys.path.append('C:/Users/Public/wp-api-python/')
else:
    sys.path.append('/home/pi/possystem/src')


class WPRestInterface(object):

    wcapi = None
    wpapi = None

    def __init__(self, wcapi, wpapi):

        self.wcapi = api.API(
            url=wcapi["api_uri"],
            consumer_key=wcapi["api_key"],
            consumer_secret=wcapi["api_secret"],
            api="wp-json",
            version="wc/v2",
            oauth_version=1,
            timeout=15
        )

        self.wpapi = api.API(
            url=wpapi["api_uri"],
            consumer_key=wpapi["api_key"],
            consumer_secret=wpapi["api_secret"],
            api="wp-json",
            version="wp/v2",
            token=wpapi["token"],
            oauth_version=wpapi["oauth_version"],
            timeout=15
        )

    def get_order_info(self, order_id):

        r = self.wcapi.get("orders/" + str(order_id))
        if r.status_code == 404:
            return {"error": "Order not found"}
        elif r.status_code == 401:
            return {"error": "Unauthorized"}
        elif r.status_code == 403:
            return {"error": "Forbidden"}
        elif r.status_code != 200:
            return {"error": "Unexpected response"}
        response = None
        try:
            response = r.json()
        except ValueError():
            printt("get_order_info(): Can't parse response JSON")
        if response:
            order_data = {}
            order_data["id"] = response["number"]
            order_data["status"] = response["status"]
            order_data["date_created"] = response["date_created"]
            order_data["total"] = response["total"]
            order_data["customer_note"] = response["customer_note"]
            # populate customer data
            order_data["customer"] = {}
            order_data["customer"]["first_name"] = response["shipping"]["first_name"]
            order_data["customer"]["last_name"] = response["shipping"]["last_name"]
            order_data["customer"]["full_name"] = order_data["customer"]["first_name"] + \
                " " + order_data["customer"]["last_name"]
            order_data["customer"]["phone"] = response["billing"]["phone"]
            order_data["customer"]["email"] = response["billing"]["email"]
            order_data["customer"]["address_1"] = response["shipping"]["address_1"]
            order_data["customer"]["address_2"] = response["shipping"]["address_2"]
            order_data["customer"]["city"] = response["shipping"]["city"]
            order_data["customer"]["state"] = response["shipping"]["state"]
            order_data["customer"]["postcode"] = response["shipping"]["postcode"]
            order_data["customer"]["country"] = response["shipping"]["country"]

            ##
            # Delivery Signature Fee
            ##
            if "fee_lines" in response:
                sig_fee = False
                fee_data = response["fee_lines"]
                for fee in fee_data:
                    if fee["name"] == "Delivery Signature Fee":
                        sig_fee = True
                order_data["delivery_signature"] = sig_fee
                order_data["fees"] = fee_data
            if "line_items" in response:
                order_data["line_items"] = response["line_items"]
            return order_data
        return None

    def get_order_items(self, order_id, filter="default"):
        """

        :rtype: list
        """
        items = []

        if filter is "default":
            filter = [
                "id",
                "name",
                "product_id",
                "quantity",
                "sku",
                "variation_id"
            ]

        def dictfilt(x, y): return dict([(i, x[i]) for i in x if i in set(y)])

        r = self.wcapi.get("orders/" + str(order_id))
        if r.status_code == 404:
            return {"error": "Order not found"}
        elif r.status_code == 401:
            return {"error": "Unauthorized"}
        elif r.status_code != 200:
            return {"error": "Unexpected response"}

        line_items = r.json()["line_items"]
        for line_item in line_items:
            if "sku" not in line_item or not line_item["sku"]:
                continue
            item = line_item
            if filter:
                item = dictfilt(line_item, filter)
            items.append(item)

        if not items:
            return []
        return items

    def update_order(self, order_id, data):
        r = self.wcapi.post("orders/" + str(order_id), data)

        if r.status_code == 404:
            result = {"error": "404"}
        elif r.status_code == 401:
            result = {"error": "Unauthorized"}
        elif r.status_code == 200:
            result = True
        else:
            result = {"error": "unexpected error."}

        return result

    def save_tracking(self, order_id, code):
        data = {
            "order_id": str(order_id),
            "tracking_num": str(code)
        }

        self.wpapi.set_api_version('xxxx/v1')
        r = self.wpapi.post("tracking/", data)

        if r.status_code == 404:
            tracking = {"error": "404"}
        elif r.status_code == 200:
            tracking = True
        else:
            tracking = {"error": "unexpected error."}

        printt(r.json(), True)
        return tracking

    def upload_order_image(self, order_id, src_path):
        if not src_path:
            printt("Upload order image failed: order_image_path not set.")
            return False
        elif not path.exists(src_path):
            printt("Upload order image failed: provided path doesn't exist.")
            return False

        filename = "order_" + str(order_id) + "_contents_proof.jpg"

        headers = {
            "content-disposition": "attachment; filename=" + filename,
            # "content-type": "image/jpg"
        }
        files = {
            'file': (filename, open(src_path, 'rb'), 'image/jpg', {})
        }
        data = [
            ("title", "Order# " + str(order_id) + " Contents Proof"),
            ("description", "Order # " + str(order_id) + "Contents"),
            ("media_type", "image"),
            # "source_url": "https://xxxxxxx.store/"
        ]

        self.wpapi.set_api_version('wp/v2')
        r = self.wpapi.post("media/", data=data, files=files, headers=headers)

        file_uri = None
        try:
            file_uri = r.json()['media_details']['sizes']['full']['source_url']
        except KeyError:
            printt("Unable to retrieve order image url. Key(s) not found. ")

        if file_uri:
            note = "xxxx POS:  <a href='%s' target='_blank'>Attached Order Image</a>" % file_uri
        else:
            note = "xxxx POS: Unsuccessfully tried to add Order image link.</a>"
            self.add_order_note(order_id, note)

        printt('Added order note to Order %s: %s' % (order_id, note))
        return r.json()

    def add_order_note(self, id, note, customer_note=False):
        if not id:
            printt('add_order_note failed: order_id not set.')
        elif not note:
            printt('add_order_note_failed: note cannot be empty.')

        data = {
            "note": str(note),
            "customer_note": customer_note
        }
        r = self.wcapi.post("orders/" + str(id) + "/notes", data)

        result = False
        if r.status_code == 404:
            result = {"error": "404"}
        elif r.status_code == 200:
            result = True
        elif r.status_code == 201:
            result = {"error": "Unauthorized"}
        else:
            result = {"error": "unexpected error."}

        return result
