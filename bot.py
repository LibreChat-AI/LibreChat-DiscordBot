import os
import subprocess
import time
import asyncio
import discord
from discord.ext import commands
import bot_config
from utils import docker, local, single, utils
from utils.command_utils import *

# Set the bot's token, user ID and working directory in "bot_config.py"
TOKEN = bot_config.TOKEN
USER_ID = bot_config.USER_ID
WORKING_DIR = bot_config.WORKING_DIR

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents, heartbeat_timeout=60)

@bot.event
async def on_ready():
    print(f'Connected as {bot.user.name}')
    invite_url = f"https://discord.com/api/oauth2/authorize?client_id={bot.user.id}&permissions=8&scope=bot"
    print('Use this URL to invite the bot:')
    print(invite_url)
    print('-------------------------------')
    await docker.setup(bot)
    await local.setup(bot)
    await single.setup(bot)
    await utils.setup(bot)
    await bot.tree.sync ()

# Remove the default help command
bot.remove_command('help')

# Create a custom help command class that inherits from HelpCommand
class CustomHelpCommand(commands.HelpCommand):
    # Override the send_bot_help method to customize the help embed
    async def send_bot_help(self, mapping):
        help_embed = discord.Embed(title="Help", description="List of Commands:", color=0x00ff00)
        for cog, commands in mapping.items():
            # Filter out the commands that the user can't run
            filtered_commands = await self.filter_commands(commands, sort=True)
            if filtered_commands:
                # Get the name and description of the cog
                cog_name = getattr(cog, "qualified_name", "Help")
                cog_description = getattr(cog, "description", "")
                # Add a field for the cog and its commands
                help_embed.add_field(name=f"{cog_name} - {cog_description}", value="\n".join(f"/{command.name} - {command.description}" for command in filtered_commands), inline=False)
        # Send the help embed to the context channel
        await self.get_destination().send(embed=help_embed)

# Assign an instance of the custom help command class to the bot's help_command attribute
bot.help_command = CustomHelpCommand()

# Run the bot with the provided token
bot.run(TOKEN)
