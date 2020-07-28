from dataclasses import dataclass
from discord.ext import commands
import jsonpickle
from misc import Misc


class CustomCommandsManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


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


    def load_commands(self):
        try:
            with open('commands.json', 'r') as file:
                return jsonpickle.decode(file)
        except IOError:
            print('commands.json not found; creating file')
            with open('commands.json', 'w') as file:
                file.write(jsonpickle.encode([]))
                return []


    # returns false if couldn't save commands
    def save_commands(self, commands_list) -> bool:
        try:
            with open('commands.json', 'w') as file:
                file.write(jsonpickle.encode(commands_list))
                return True
        except IOError:
            print('couldn\'t save commands')
            return False

