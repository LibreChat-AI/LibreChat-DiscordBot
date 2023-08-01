import os
from discord.ext import commands
import bot_config
from utils.command_utils import *

# Set the working directory from "bot_config.py"
WORKING_DIR = bot_config.WORKING_DIR
USER_ID = bot_config.USER_ID

# Create a class called "Docker" that inherits from "commands.Cog"
class Single(commands.Cog):
    # Define a constructor that takes a bot instance as an argument and assigns it to an attribute called "bot"
    def __init__(self, bot):
        self.bot = bot

    # Define a check function to verify if the user executing a command is the specified user
    @commands.check
    def is_user(self, ctx):
        return str(ctx.author.id) == USER_ID

    # Docker "start-single" command
    @commands.command(name="start-s", description="Start Docker with single-compose.yml")
    async def start_single(self, ctx):
        os.chdir(WORKING_DIR) # Change the working directory to the specified folder
        status_message = await ctx.send('Starting docker...')
        command = 'docker-compose -f ./docs/dev/single-compose.yml up -d'
        await execute_command_with_status_message(ctx, command)

    # Docker "stop-single" command
    @commands.command(name="stop-s", description="Stop Docker with single-compose.yml")
    async def stop_single(self, ctx):
        os.chdir(WORKING_DIR) # Change the working directory to the specified folder
        status_message = await ctx.send('Stopping docker...')
        command = 'docker-compose -f ./docs/dev/single-compose.yml stop'
        await execute_command_with_status_message(ctx, command)

    # Docker "update-s" command   
    @commands.command(name="update-s", description="Update single-compose.yml")
    async def update_single(self, ctx):
        os.chdir(WORKING_DIR) # Change the working directory to the specified folder
        status_message = await ctx.send('Update in progress...')
        start_time = time.time()
        commands = [
            'npm run update:single',
            'docker-compose -f ./docs/dev/single-compose.yml up -d'
        ]
        await execute_commands_with_status_messages(ctx, commands)
        elapsed_time = time.time() - start_time
        await status_message.edit(content=f'Update completed in {elapsed_time:.2f} seconds.')

# Define a function called "setup" that takes a bot instance as an argument and adds an instance of the "Docker" class to the bot's cogs using the "add_cog" method
async def setup(bot):
    await bot.add_cog(Single(bot))