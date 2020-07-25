import discord
from discord.ext import commands
from time import monotonic
from config import Config
from store import Store
from order import Order

ytc = Store(Config.WCM_URL, Config.WCM_KEY, Config.WCM_SECRET)
bot = commands.Bot(command_prefix='!')
bot.remove_command("help")


@bot.event
async def on_ready():
    print('logged in as {}'.format(bot.user))
    print(discord.utils.oauth_url(
        bot.user.id, permissions=discord.Permissions(8)))
    print('-----')


@bot.event
async def send_error(ctx, message, footer=None):
    embed = discord.Embed(title=message, colour=0xF44336)
    if footer is not None:
        embed.set_footer(text=footer)
    await ctx.send(embed=embed)


@bot.command()
async def status(ctx, order_id):
    start_time = monotonic()
    print("Check order id {}".format(order_id))
    if not order_id.isdigit():
        await send_error(ctx, ':warning: Invalid order ID entered')
        return
    response = ytc.get_order(order_id)
    if 'code' in response:
        if response['code'] == 'woocommerce_rest_shop_order_invalid_id':
            await send_error(ctx, ':warning: No order exists with the given ID')
        else:
            await send_error(ctx, ':warning: An error occurred',
                             response['code'])
        return
    notes = ytc.get_order_notes(order_id)
    order = Order(response, notes)
    embed = order.create_embed()
    await ctx.send(embed=embed)
    end_time = monotonic()
    print('ok, took {:.2f} s'.format(end_time - start_time))
    print('-----')


if __name__ == "__main__":
    bot.run(Config.BOT_TOKEN)
