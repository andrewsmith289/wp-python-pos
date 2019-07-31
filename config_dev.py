ORDER_CONFIG = {
    "ORDER_STATES": ["OPEN", "FILLING", "FILLED"]
}
SCANNER_CONFIG = {
    "SYS_STATES": [
        "OFF",
        "READY",
        "ORDER_FILL",
        "IMAGE_CAPTURE",
        "WAIT_TRACKING",
        "DONE_ORDER",
        "ERROR"
    ],
    "DEFAULT_DATA_COLS": [
        "id",
        "name",
        "product_id",
        "quantity",
        "sku",
        "variation_id"
    ]
}
CONFIG = {
    "wcapi": {
        "api_uri": "https://dev.xxxxx.com",

        "api_key": "ck_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  # new dev
        "api_secret": "cs_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "oauth_version": 1
    },
    "wpapi": {
        "api_uri": "https://dev.xxxxx.store",
        "api_key": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  # new dev
        "api_secret": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "token": "",
        "oauth_version": 2
    }
}
