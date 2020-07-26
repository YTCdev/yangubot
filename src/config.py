from discord import Colour


class Config:
    WCM_URL = ''
    WCM_KEY = ''
    WCM_SECRET = ''

    BOT_TOKEN = ''
    OWNER_IDS = []
    ROLE_IDS = []

    CHANNELS = {
        'support': 210588354096529416,
        'lounge': 210828828300279808,
        'gallery': 212328069082513408
    }

    COUNTRIES = ['CA', 'US', 'AU', 'AT', 'BE', 'BG', 'CY', 'CZ', 'DK', 'EE',
                 'FI', 'FR', 'DE', 'GR', 'HU', 'HR', 'IE', 'IT', 'LV', 'LT',
                 'LU', 'MT', 'NL', 'PL', 'PT', 'RO', 'SK', 'SI', 'ES', 'SE',
                 'GB']

    COLOURS = {
        'completed': Colour(0x4caf50),
        'cancelled': Colour(0xf44336),
        'failed': Colour(0xf44336),
        'pending': Colour(0xffeb3b),
        'processing': Colour(0xffeb3b),
        'on-hold': Colour(0xff9800),
        'other': Colour(0xffeb3b)
    }
