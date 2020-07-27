from time import monotonic
import discord
from discord.ext import commands
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
    print(message)
    print('-----')


@bot.event
async def is_staff(user):
    roles = [role.id for role in user.roles]
    for staff_role in Config.ROLE_IDS:
        if staff_role in roles:
            return True
    return False


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


@bot.command()
async def wcm(ctx, order_id):
    if await is_staff(ctx.author):
        await ctx.author.send(
            "{}/wp-admin/post.php?post={}&action=edit".format(
                Config.WCM_URL, order_id))
        await ctx.message.delete()


@bot.event
async def on_message(message: discord.Message):
    # prevent bot from reacting to its own messages
    if message.author.id == bot.user.id:
        return
    # gallery chat control
    if message.channel.id == Config.CHANNELS['gallery']:
        # if message has pics don't do anything
        if len(message.attachments) > 0:
            return
        # else check if user has previously uploaded any pics
        allowed = False
        async for old_message in message.channel.history(limit=75):
            if old_message.author == message.author and len(
                    old_message.attachments) > 0:
                allowed = True
                break
        # if no pics from that user found, delete and notify
        if not allowed:
            await message.delete()
            await message.channel.send(
                content=get_gallery_warning(message.author), delete_after=12.5)
    await bot.process_commands(message)


def get_gallery_warning(user: discord.Member) -> str:
    return '{} - this channel is for **pics only**. Please use <#{}> for ' \
           'discussion or ask in <#{}> if you have any questions.\n\nIf you ' \
           'want to voice your opinion - feel free to do so, just don\'t ' \
           'forget to send some pictures first!'.format(
               user.mention, Config.CHANNELS['lounge'], Config.CHANNELS['support'])


if __name__ == "__main__":
    bot.run(Config.BOT_TOKEN)
