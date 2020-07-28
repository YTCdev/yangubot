from dataclasses import dataclass
from discord.ext import commands
from discord import Embed
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
    async def add(self, ctx, trigger: str, title: str, content: str):
        command_list = self.get_commands()
        if any(x.trigger == trigger for x in command_list):
            await Misc.send_error(
                ctx, 'Trigger {} already exists.'.format(trigger))
            return
        command = CustomCommand(trigger, title, content)
        command_list.append(command)
        if self.save_commands(command_list):
            await Misc.send_msg(
                ctx, 'Command {} successfully added.'.format(trigger))
        else:
            await Misc.send_error(ctx, 'Couldn\'t save command.')


    @cc.command()
    async def remove(self, ctx, trigger: str):
        command_list = self.get_commands()
        if not any(x.trigger == trigger for x in command_list):
            await Misc.send_error(
                ctx, 'Trigger {} not found.'.format(trigger))
            return
        command = [x for x in command_list if x.trigger == trigger][0]
        command_list.remove(command)
        if self.save_commands(command_list):
            await Misc.send_msg(
                ctx, 'Command {} successfully removed.'.format(trigger))
        else:
            await Misc.send_error(ctx, 'Couldn\'t remove command.')


    @cc.command()
    async def list(self, ctx):
        command_list = self.get_commands()
        response = '```List of custom commands\n(trigger - title)\n\n'
        for i, command in enumerate(command_list, 1):
            response += '{}. {} - {}\n'.format(
                i, command.trigger, command.title)
        response += '```'
        await ctx.send(response)


    async def send_response(self, ctx, command):
        embed = Embed(title=command.title, description=command.content)
        await ctx.send(embed=embed)


    def get_commands(self):
        try:
            with open('commands.json', 'r') as file:
                return jsonpickle.decode(file.read())
        except IOError:
            print('commands.json not found; creating file')
            self.save_commands([])
            return self.get_commands()


    # returns false if couldn't save commands
    def save_commands(self, command_list) -> bool:
        try:
            with open('commands.json', 'w') as file:
                file.write(jsonpickle.encode(command_list))
                return True
        except IOError:
            print('couldn\'t save commands')
            return False


@dataclass
class CustomCommand:
    trigger: str
    title: str
    content: str
