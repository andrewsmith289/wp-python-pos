from SharedUtilities import printt
import types


class Product(object):

    packs_quantity = 0
    packs_filled = 0
    packs_remaining = 0
    variation_quantity = 0
    sku = ''
    name = ''

    def __init__(self, data):
        self.product_id = data['product_id']
        self.variation_id = data['variation_id']
        self.sku = data['sku']
        self.name = data['name']
        self.quantity = data['quantity']
        self.packs_remaining = self.packs_to_go

    def __str__(self):
        NL = "\r\n"
        string = (
            '      <OrderItem ' + NL +
            '          product_id=' + str(self.product_id) + NL +
            '          variation_id=' + str(self.variation_id) + NL +
            '          quantity=' + str(self.quantity) + NL +
            '          packs_quantity=' + str(self.packs_to_go) + NL +
            '          packs_remaining=' + str(self.packs_remaining) + NL +
            '          sku=' + self.sku + NL +
            '          name=' + self.name + NL +
            '      />'
        )
        return string

    def __eq__(self, other):
        if self.product_id == other.product_id:
            if self.variation_id == other.variation_id:
                return True
        return False

    def fill_packs(self, amount=1):
        self.packs_filled += 1
        if self.packs_filled < 0:
            self.packs_filled = 0
        elif self.packs_filled > self.packs_to_go:
            self.packs_filled = self.packs_to_go

    @property
    def packs_to_go(self):
        remain = self.total_packs - self.packs_remaining
        if remain < 0:
            remain = 0
        return remain

    @property
    def total_packs(self):
        # get packages required to fill this product or variation
        packs_qty = Product.extract_variation_qty(self.sku)
        if packs_qty == -1:
            packs_qty = 1
        return self.quantity * packs_qty

    @staticmethod
    def extract_variation_qty(line_item):
        sku = []
        if not line_item:
            if isinstance(line_item, types.StringType) is not True and 'sku' not in line_item:
                printt("extract_variation_qty: line_item must be provided as either: \n"
                       "OrderItem, str, or dict with an sku key present. Provided: " + str(line_item))
            return -1
        elif isinstance(line_item, types.DictionaryType):
            sku.append(line_item["sku"])
        elif isinstance(line_item, types.StringTypes):
            sku.append(str(line_item))
        elif isinstance(line_item, Product):
            sku.append(line_item.sku)

        pieces = str.split(sku[0], '-')
        if len(pieces) != 2:
            printt("Variation quantity not found in SKU '" +
                   str(sku[0]) + "'. Assuming product is non variable.")
            return -1
        return int(pieces[1])
