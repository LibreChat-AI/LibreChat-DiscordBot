import os
from discord.ext import commands
import bot_config
from utils.command_utils import *

# Set the working directory from "bot_config.py"
WORKING_DIR = bot_config.WORKING_DIR
USER_ID = bot_config.USER_ID

# Create a class called "Docker" that inherits from "commands.Cog"
class Docker(commands.Cog):
    # Define a constructor that takes a bot instance as an argument and assigns it to an attribute called "bot"
    def __init__(self, bot):
        self.bot = bot

    # Define a check function to verify if the user executing a command is the specified user
    @commands.check
    def is_user(self, ctx):
        return str(ctx.author.id) == USER_ID

    # Docker "Start" command
    @commands.command(name="start", description="Start Docker")
    async def start(self, ctx):
        os.chdir(WORKING_DIR) # Change the working directory to the specified folder
        command = 'docker-compose up -d'
        await execute_command_with_status_message(ctx, command)

    # Docker "Stop" command
    @commands.command(name="stop", description="Stop Docker")
    async def stop(self, ctx):
        os.chdir(WORKING_DIR) # Change the working directory to the specified folder
        command = 'docker-compose stop'
        await execute_command_with_status_message(ctx, command)

    # Docker "Update" command   
    @commands.command(name="update", description="Update LibreChat")
    async def update(self, ctx):
        os.chdir(WORKING_DIR) # Change the working directory to the specified folder
        commands = [
            'npm run update:docker',
            'docker-compose up -d'
        ]
        await execute_commands_with_status_messages(ctx, commands)

# Define a function called "setup" that takes a bot instance as an argument and adds an instance of the "Docker" class to the bot's cogs using the "add_cog" method
async def setup(bot):
    await bot.add_cog(Docker(bot))
