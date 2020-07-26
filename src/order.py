import dateutil.parser
from pandas.tseries.offsets import BDay
from discord import Embed
from config import Config


class Order:
    def __init__(self, json, notes):
        self.json = json
        self.notes = notes
        self.id = json['id']
        self.status = json['status']
        self.product = json['line_items'][0]['name']
        self.sku = json['line_items'][0]['sku']
        self.country = json['shipping']['country'] or json['billing']['country']
        self.order_date = self.parse_date(json['date_created'])
        self.modified_date = self.parse_date(json['date_modified'])
        self.shipping_method = json['shipping_lines'][0]['method_title']
        self.arrival_estimate = self.estimate_shipping()
        self.has_tracking = self.is_tracked()

    def parse_date(self, date_str):
        return dateutil.parser.parse(date_str)

    def estimate_shipping(self):
        if 'tablet cover' not in self.product.lower():
            return None
        if self.status != 'completed':
            return None
        # Tablet cover shipping
        # 8-10 days for countries in config list
        # 15-23 everywhere else
        # Rush shipping: 4-7 business days
        shipped_on = self.ship_date()
        if not shipped_on:
            return None
        if self.shipping_method == 'Rush':
            return self.calc_bdays(shipped_on, 7)
        else:
            if self.country in Config.COUNTRIES:
                return self.calc_bdays(shipped_on, 10)
            return self.calc_bdays(shipped_on, 23)

    def calc_bdays(self, date, days):
        return date + BDay(days)

    def ship_date(self):
        for order_note in self.notes:
            if 'order confirmation' in order_note['note'].lower():
                return self.parse_date(order_note['date_created'])
        return None

    def is_tracked(self):
        for order_note in self.notes:
            if 'track' in order_note['note'].lower():
                return True
        return False

    def create_embed(self):
        embed = Embed(title='Order Status', timestamp=self.order_date)
        if self.status in Config.COLOURS:
            embed.colour = Config.COLOURS[self.status]
        else:
            embed.colour = Config.COLOURS['other']

        embed.add_field(
            name="#{} • :flag_{}:".format(self.id, self.country.lower()),
            value="**{}**\n{} shipping".format(
                self.status.capitalize(), self.shipping_method.capitalize()),
            inline=True
        )

        temp = ''
        if self.arrival_estimate is not None:
            temp += '*Estimated* arrival: {}\n'.format(
                self.arrival_estimate.strftime(
                    "%d %b %Y").lstrip("0").replace(" 0", " "))
        if self.has_tracking:
            temp += 'Check email for tracking info\n'
        if self.status == 'on-hold':
            temp += 'Please check your email'

        if temp == '':
            temp = 'No updates yet'

        embed.add_field(
            name="Notes",
            value=temp,
            inline=True
        )

        embed.add_field(
            name='Last updated',
            value=self.modified_date.strftime(
                "%d %b %Y, %H:%M:%S").lstrip("0").replace(" 0", " "),
            inline=False
        )

        embed.set_footer(text=self.sku)

        return embed
