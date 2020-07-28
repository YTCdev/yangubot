import discord
from config import Config


class Misc:
    @staticmethod
    def is_staff(ctx):
        roles = [role.id for role in ctx.author.roles]
        return any(id in roles for id in Config.STAFF_IDS)

    @staticmethod
    async def send_error(ctx, message, footer=None):
        embed = discord.Embed(title=message, colour=0xF44336)
        if footer is not None:
            embed.set_footer(text=footer)
        await ctx.send(embed=embed)
        print(message)
        print('-----')
