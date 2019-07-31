from os import makedirs
from errno import EEXIST
import re
from pprint import pprint
from random import randint
import os
import datetime

debug = True


def is_valid_tracking(code):
    cp_xpress_pattern = r'\b\w{2}\s?(\d{3}\s?){3}\w{2}\b'
    if re.search(cp_xpress_pattern, code):
        return True
    return False


def printt(msg, pretty=False):
    if not debug:
        return
    if not pretty:
        print msg
    else:
        pprint(msg)


def is_valid_item_data(data):
    if not data:
        return
    req_keys = ["product_id", "variation_id", "quantity", "sku", "name"]
    if all(k in data for k in req_keys):
        return True
    return False


def is_valid_order_data(data):
    if "order_id" in data:
        return True
    return False


def is_valid_item_scan(data):
    if not data:
        return False
    elif "order_id" in data:
        return True
    elif "product_id" in data and "variation_id" in data:
        return True
    else:
        return False


def generate_random(length, keyset="abcdef1234567890"):
    max = len(keyset)
    out = ""
    for i in range(0,length):
        rand = randint(0, max-1)
        out += keyset[rand]
    return out


def ensure_path_exists(path):
    try:
        makedirs(path)
    except OSError as exception:
        if exception.errno != EEXIST:
            raise


def delete_old_files(path, days_old):
    ensure_path_exists(path)
    if not os.path.exists(path):
        raise IOError("path " + str(path) + " does not exist.")

    now = datetime.datetime.today()

    for filename in os.listdir(path):
        full_path = path + filename
        file_cdate = datetime.datetime.fromtimestamp(
            os.path.getctime(full_path)
        )
        duration = now - file_cdate
        if duration.days > days_old:
            os.remove(full_path)
            printt("Removed " + full_path + " as it was older than " + str(days_old) + " days old.")
