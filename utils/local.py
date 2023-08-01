import os
from discord.ext import commands
import bot_config
from utils.command_utils import *

# Set the working directory from "bot_config.py"
WORKING_DIR = bot_config.WORKING_DIR
USER_ID = bot_config.USER_ID

class Local(commands.Cog):
    # Define a constructor that takes a bot instance as an argument and assigns it to an attribute called "bot"
    def __init__(self, bot):
        self.bot = bot

    # Define a check function to verify if the user executing a command is the specified user
    @commands.check
    def is_user(self, ctx):
        return str(ctx.author.id) == USER_ID
    
    # Local "start-local" command
    @commands.command(name="start-l", description="Start Local")
    async def start_local(self, ctx):
        os.chdir(WORKING_DIR) # Change the working directory to the specified folder
        status_message = await ctx.send('Starting LibreChat...')
        command = 'npm run backend'
        await execute_command_with_status_message(ctx, command)

    # Local "stop-local" command
    @commands.command(name="stop-l", description="Stop Local")
    async def stop_local(self, ctx):
        os.chdir(WORKING_DIR) # Change the working directory to the specified folder
        status_message = await ctx.send('Stopping LibreChat...')
        command = 'npm run backend:stop'
        await execute_command_with_status_message(ctx, command)

    # Local "Update" command   
    @commands.command(name="update-l", description="Update Local")
    async def update_local(self, ctx):
        os.chdir(WORKING_DIR) # Change the working directory to the specified folder
        status_message = await ctx.send('Update in progress...')
        start_time = time.time()
        commands = [
            'npm run backend:stop'
            'npm run update:local',
            'npm run backend'
        ]
        await execute_commands_with_status_messages(ctx, commands)
        elapsed_time = time.time() - start_time
        await status_message.edit(content=f'Update completed in {elapsed_time:.2f} seconds.')

# Define a function called "setup" that takes a bot instance as an argument and adds an instance of the "Docker" class to the bot's cogs using the "add_cog" method
async def setup(bot):
    await bot.add_cog(Local(bot))
