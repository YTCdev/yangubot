from dataclasses import dataclass
from discord.ext import commands
from discord import Embed, Message
import jsonpickle
from config import Config
from misc import Misc


class CustomCommandsManager(commands.Cog):
    def __init__(self, bot, prefix=''):
        self.bot = bot
        self.prefix = prefix
        self.commands = self.load_commands()


    @commands.group()
    @commands.check(Misc.is_staff)
    async def cc(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Available subcommands: add, remove, list')


    @cc.command()
    async def add(self, ctx, trigger: str, title: str, content: str):
        # prevent blocking the command if prefix here is identical to the main one
        if trigger == 'cc':
            return
        command_list = self.commands[:]
        if any(x.trigger == trigger for x in command_list):
            await Misc.send_error(
                ctx, 'Trigger {} already exists.'.format(trigger))
            return
        command = CustomCommand(trigger, title, content)
        command_list.append(command)
        if self.save_commands(command_list):
            await Misc.send_msg(
                ctx, 'Command {} added.'.format(trigger))
        else:
            await Misc.send_error(ctx, 'Couldn\'t save command.')


    @cc.command()
    async def remove(self, ctx, trigger: str):
        command_list = self.commands[:]
        if not any(x.trigger == trigger for x in command_list):
            await Misc.send_error(
                ctx, 'Trigger {} not found.'.format(trigger))
            return
        command = [x for x in command_list if x.trigger == trigger][0]
        command_list.remove(command)
        if self.save_commands(command_list):
            await Misc.send_msg(
                ctx, 'Command {} removed.'.format(trigger))
        else:
            await Misc.send_error(ctx, 'Couldn\'t remove command.')


    @cc.command()
    async def list(self, ctx):
        command_list = self.commands
        if len(command_list) > 0:
            response = 'List of custom commands (trigger -> title):\n```'
            for i, command in enumerate(command_list, 1):
                response += '{}. {} -> {}\n'.format(
                    i, command.trigger, command.title)
            response += '```'
        else:
            response = 'No custom commands yet.'
        await ctx.send(response)


    async def check_message(self, message: Message) -> bool:
        command_list = self.commands
        triggers = [self.prefix + x.trigger for x in command_list]
        if message.content in triggers:
            command = next(
                x for x in command_list if self.prefix + x.trigger == message.content)
            await self.send_response(message.channel, command)
            return True
        return False


    async def send_response(self, channel, command):
        embed = Embed(
            title=command.title, 
            description=command.content,
            colour=Config.COLOURS['completed'])
        await channel.send(embed=embed)


    def load_commands(self):
        try:
            with open('commands.json', 'r') as file:
                return jsonpickle.decode(file.read())
        except IOError:
            print('commands.json not found; creating file')
            self.save_commands([])
            return self.load_commands()


    # returns false if unable to save commands
    def save_commands(self, command_list) -> bool:
        try:
            with open('commands.json', 'w') as file:
                file.write(jsonpickle.encode(command_list))
                self.commands = command_list
                return True
        except IOError:
            print('couldn\'t save commands')
            return False


@dataclass
class CustomCommand:
    trigger: str
    title: str
    content: str
