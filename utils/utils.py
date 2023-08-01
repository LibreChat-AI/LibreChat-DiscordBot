import os
import discord
from discord.ext import commands
import bot_config
from utils.command_utils import *

# Set the working directory from "bot_config.py"
WORKING_DIR = bot_config.WORKING_DIR
USER_ID = bot_config.USER_ID

# Create a class called "Docker" that inherits from "commands.Cog"
class Utils(commands.Cog):
    # Define a constructor that takes a bot instance as an argument and assigns it to an attribute called "bot"
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="config", description="Change working directory", cog_name="Utils")
    async def config(self, ctx):
        global WORKING_DIR
        current_working_dir = WORKING_DIR

        # Prepare the initial message with the current working directory
        message = await ctx.send(f"The current folder is: {current_working_dir}\nDo you want to change the working directory?")

        # Add reaction emojis to the message
        await message.add_reaction('✅')  # Green circle for yes
        await message.add_reaction('❌')  # Red circle for no

        # Define a check function to filter user reactions
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ['✅', '❌']

        try:
            # Wait for the user's reaction
            reaction, _ = await self.bot.wait_for('reaction_add', timeout=30, check=check)

            if str(reaction.emoji) == '✅':
                await ctx.send("Enter the new working directory")
                try:
                    # Wait for the user's message input
                    new_working_dir_msg = await self.bot.wait_for('message', timeout=30, check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
                    new_working_dir = new_working_dir_msg.content.strip()
                    WORKING_DIR = new_working_dir

                    with open("bot_config.py", "r") as config_file:
                        lines = config_file.readlines()

                    for i in range(len(lines)):
                        if lines[i].startswith("WORKING_DIR"):
                            lines[i] = f'WORKING_DIR = "{new_working_dir}"\n'
                            break

                    with open("bot_config.py", "w") as config_file:
                        config_file.writelines(lines)

                    await ctx.send(f"Working directory changed from {current_working_dir} to: {new_working_dir}")
                except asyncio.TimeoutError:
                    await ctx.send("Sorry, you didn't reply in time. Working directory change cancelled.")
            else:
                await ctx.send("Working directory change cancelled.")
        except asyncio.TimeoutError:
            await ctx.send("Sorry, you didn't reply in time. Working directory change cancelled.")

        # Remove the reactions from the message
        await message.clear_reactions()

    @commands.command(name="d-env", description="Download the .env file from the working directory", cog_name="Utils")
    async def download_env(self, ctx):
        global WORKING_DIR

        file_name = ".env"
        file_path = os.path.join(WORKING_DIR, file_name)

        if not os.path.isfile(file_path):
            await ctx.send("The .env file does not exist in the working directory.")
            return

        with open(file_path, "rb") as file:
            new_file_name = f".{file_name}"
            await ctx.send(file=discord.File(file, filename=new_file_name))

    @commands.command(name="env-example", description="Download the .env.example file from the working directory", cog_name="Utils")
    async def env_example(self, ctx):
        global WORKING_DIR

        file_name = ".env.example"
        file_path = os.path.join(WORKING_DIR, file_name)

        if not os.path.isfile(file_path):
            await ctx.send(f"The .env.example file does not exist in the working directory.")
            return

        with open(file_path, "rb") as file:
            await ctx.send(file=discord.File(file, filename=file_name))

    @commands.command(name="u-env", description="Upload an .env file to the working directory", cog_name="Utils")
    async def upload(self, ctx):
        global WORKING_DIR

        attachments = ctx.message.attachments

        if not attachments:
            await ctx.send("Please attach an .env file to upload.")
            return

        attachment = attachments[0]
        file_name = attachment.filename

        if not file_name.endswith("env"):
            await ctx.send("Invalid file format. Please upload an .env file.")
            return

        file_path = os.path.join(WORKING_DIR, ".env")
        existing_file_path = os.path.join(WORKING_DIR, ".env.bak")

        try:
            if os.path.isfile(file_path):
                os.rename(file_path, existing_file_path)
                await ctx.send("Existing .env file renamed to .env.bak.")

            await attachment.save(file_path)
        except Exception as e:
            await ctx.send(f"An error occurred while saving the file: {str(e)}")
            return

        await ctx.send("Uploaded .env file to the working directory.")
        await ctx.send("Please restart or update your environment to apply the changes.")

    @commands.command(name="restore-env", description="Delete the .env file and restore .env.bak as .env", cog_name="Utils")
    async def restore_env(self, ctx):
        global WORKING_DIR

        env_file_path = os.path.join(WORKING_DIR, ".env")
        env_bak_file_path = os.path.join(WORKING_DIR, ".env.bak")

        if not os.path.isfile(env_file_path) and not os.path.isfile(env_bak_file_path):
            await ctx.send("Both .env and .env.bak files do not exist in the working directory.")
            return

        if os.path.isfile(env_file_path):
            os.remove(env_file_path)
            await ctx.send(".env file deleted.")

        if os.path.isfile(env_bak_file_path):
            os.rename(env_bak_file_path, env_file_path)
            await ctx.send(".env.bak file restored as .env.")

        await ctx.send(".env file restored successfully.")
        await ctx.send("Please restart or update your environment to apply the changes.")

    # Docker "Status" command
    @commands.command(name="status", description="Docker status", cog_name="Utils")
    async def status(self, ctx):
        os.chdir(WORKING_DIR) # Change the working directory to the specified folder
        #status_message = await ctx.send('Getting Docker status...')
        command = 'docker ps -a'
        await execute_command_with_status_message(ctx, command)

# Define a function called "setup" that takes a bot instance as an argument and adds an instance of the "Docker" class to the bot's cogs using the "add_cog" method
async def setup(bot):
    await bot.add_cog(Utils(bot))