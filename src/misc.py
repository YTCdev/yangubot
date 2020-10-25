import discord
from config import Config


class Misc:
    @staticmethod
    def is_staff(ctx):
        roles = [role.id for role in ctx.author.roles]
        return any(id in roles for id in Config.STAFF_IDS)

    @staticmethod
    def is_owner(ctx):
        return ctx.author.roles in Config.STAFF_IDS

    @staticmethod
    async def send_error(ctx, message, footer=None):
        embed = discord.Embed(title=message, colour=Config.COLOURS['failed'])
        if footer is not None:
            embed.set_footer(text=footer)
        await ctx.send(embed=embed)
        print(message)
        print('-----')

    @staticmethod
    async def send_msg(ctx, message):
        embed = discord.Embed(title=message, colour=Config.COLOURS['completed'])
        await ctx.send(embed=embed)
        print(message)
        print('-----')
