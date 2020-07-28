import json
from discord.ext import commands
from misc import Misc


class CustomCommandsManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.commands: dict
        self.load_commands()

    def load_commands(self):
        try:
            with open('commands.json', 'r') as file:
                self.commands = json.load(file)
        except IOError:
            print('commands.json not found; creating file')
            with open('commands.json', 'w') as file:
                self.commands = dict()
                json.dump(self.commands, file)


    @commands.group()
    @commands.check(Misc.is_staff)
    async def cc(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Available subcommands: add, remove, list')


    @cc.command()
    async def add(self, ctx, title: str, content: str):
        await ctx.send('add')


    @cc.command()
    async def remove(self, ctx, title: str):
        pass


    @cc.command()
    async def list(self, ctx):
        pass
