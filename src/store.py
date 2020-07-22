from woocommerce import API
from .config import Config


class Store:
    def __init__(self, url, key, secret):
        self.wcapi = API(
            url=url,
            consumer_key=key,
            consumer_secret=secret,
            wp_api=True,
            version="wc/v3"
        )

    def get_order(self, order_id):
        return self.wcapi.get('orders/' + order_id).json()

    def get_order_notes(self, order_id):
        return self.wcapi.get('orders/' + order_id + '/notes').json()
