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


def is_staff(ctx):
    roles = [role.id for role in ctx.author.roles]
    return any(id in roles for id in Config.STAFF_IDS)


@bot.command()
async def status(ctx, order_id):
    start_time = monotonic()
    print("Check order id {}".format(order_id))
    if not order_id.isdigit():
        await send_error(ctx, ':warning: Invalid order ID entered')
        return
    await ctx.trigger_typing()
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
    if order.status in ['processing', 'completed']:
        await add_patron_role(ctx, order)
    end_time = monotonic()
    print('ok, took {:.2f} s'.format(end_time - start_time))
    print('-----')


async def add_patron_role(ctx, order: Order):
    # if customer didnt provide his discord ID
    if not order.discord_id:
        return
    user = ctx.guild.get_member_named(order.discord_id)
    if not user:
        print('User not in server')
    elif any(role.id == Config.PATRON_ID for role in user.roles):
        print('User already has role')
    else:
        try:
            role = discord.utils.get(ctx.guild.roles, id=Config.PATRON_ID)
            await ctx.author.add_roles(role)
            print('Added role to user {}'.format(order.discord_id))
        except discord.Forbidden:
            print('Missing permissions to add role')


@bot.command()
@commands.check(is_staff)
async def wcm(ctx, order_id):
    await ctx.author.send(
        "{}/wp-admin/post.php?post={}&action=edit".format(
            Config.WCM_URL, order_id))
    await ctx.message.delete()


@bot.event
async def on_message(message: discord.Message):
    # prevent bot from reacting to its own messages
    if message.author.id == bot.user.id:
        return
    # prevent bot from responding to already-removed messages
    if message.channel.id == Config.CHANNELS['gallery']:
        if await check_gallery_message(message):
            await bot.process_commands(message)
    else:
        await bot.process_commands(message)


async def check_gallery_message(message: discord.Message) -> bool:
    # ignore message if it has attachments
    if len(message.attachments) > 0:
        return True

    # check if user has previously uploaded any pics
    allowed = False
    async for old_message in message.channel.history(limit=75):
        if old_message.author == message.author and len(old_message.attachments) > 0:
            allowed = True
            break
    # if no pics from that user found, delete and notify
    if not allowed:
        await message.delete()
        await message.channel.send(content=get_gallery_warning(message.author),
                                   delete_after=12.5)
    return allowed


def get_gallery_warning(user: discord.Member) -> str:
    return '{} - this channel is for **pics only**. Please use <#{}> for ' \
           'discussion or ask in <#{}> if you have any questions.\n\nIf you ' \
           'want to voice your opinion - feel free to do so, just don\'t ' \
           'forget to send some pictures first!'.format(
               user.mention, Config.CHANNELS['lounge'], Config.CHANNELS['support'])


if __name__ == "__main__":
    bot.run(Config.BOT_TOKEN)
