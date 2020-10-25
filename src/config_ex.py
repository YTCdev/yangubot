from discord import Colour


class Config:
    # WooCommerce API settings
    #
    # Get an API key by going to WooCommerce > Settings > Advanced > REST API on
    # your WordPress installation.
    WCM_URL = ''
    WCM_KEY = ''
    WCM_SECRET = ''

    # Discord API settings
    #
    # Get your bot token at https://discord.com/developers/applications
    BOT_TOKEN = ''

    # Discord server settings
    # -----------------------
    # The user IDs of the owners of the bot
    OWNER_IDS = []
    # The role IDs of the staff role(s) on the server
    STAFF_IDS = []
    # The role to give users if they have purchased a product
    # (set to 0 if none)
    PATRON_ID = 0
    # The text channels designated to customer support, general discussion, and
    # a product gallery, respectively (set to 0 if none)
    CHANNELS = {
        'support': 0,
        'lounge': 0,
        'gallery': 0
    }
    # List of countries with faster shipping
    # TODO: WooCommerce integration to calculate shipping estimates
    COUNTRIES = ['CA', 'US', 'AU', 'AT', 'BE', 'BG', 'CY', 'CZ', 'DK', 'EE',
                 'FI', 'FR', 'DE', 'GR', 'HU', 'HR', 'IE', 'IT', 'LV', 'LT',
                 'LU', 'MT', 'NL', 'PL', 'PT', 'RO', 'SK', 'SI', 'ES', 'SE',
                 'GB']
    # Colours to use for each order status
    COLOURS = {
        'completed': Colour(0x4caf50),
        'cancelled': Colour(0xf44336),
        'failed': Colour(0xf44336),
        'pending': Colour(0xffeb3b),
        'processing': Colour(0xffeb3b),
        'on-hold': Colour(0xff9800),
        'other': Colour(0xffeb3b)
    }
