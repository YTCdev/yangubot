import discord
from discord.ext import commands
from config import Config
from store import Store

ytc = Store(Config.WCM_URL, Config.WCM_KEY, Config.WCM_SECRET)
bot = commands.Bot(command_prefix='!')
bot.remove_command("help")


@bot.command()
async def status(ctx, order_id):
    order = ytc.get_order(order_id)
    notes = ytc.get_order_notes(order_id)




if __name__ == "__main__":
    bot.run(Config.BOT_TOKEN)
