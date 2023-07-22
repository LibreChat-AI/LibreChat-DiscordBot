import os
import subprocess
import time
import asyncio
import discord
from discord.ext import commands
import bot_config

# Set the bot's token, user ID and working directory in "bot_config.py"
TOKEN = bot_config.TOKEN
USER_ID = bot_config.USER_ID
WORKING_DIR = bot_config.WORKING_DIR

# Create an instance of the bot with the provided token and user ID
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents, heartbeat_timeout=60)

# Define a check function to verify if the user executing a command is the specified user
@bot.check
def is_user(ctx):
    return str(ctx.author.id) == USER_ID

# Define an event function that runs when the bot is ready and prints a message indicating the bot's connection
@bot.event
async def on_ready():
    print(f'Connected as {bot.user.name}')
    await bot.tree.sync ()

# Docker "Status" command
@bot.hybrid_command(name="status", description="Docker status")
async def status(ctx):
    os.chdir(WORKING_DIR) # Change the working directory to the specified folder
    #status_message = await ctx.send('Getting Docker status...')
    command = 'docker ps -a'
    await execute_command_with_status_message(ctx, command)

# Docker "Start" command
@bot.hybrid_command(name="start", description="Start Docker")
async def start(ctx):
    os.chdir(WORKING_DIR) # Change the working directory to the specified folder
    status_message = await ctx.send('Starting docker...')
    command = 'docker-compose up -d'
    await execute_command_with_status_message(ctx, command)

# Docker "Stop" command
@bot.hybrid_command(name="stop", description="Stop Docker")
async def stop(ctx):
    os.chdir(WORKING_DIR) # Change the working directory to the specified folder
    status_message = await ctx.send('Stopping docker...')
    command = 'docker-compose stop'
    await execute_command_with_status_message(ctx, command)

# Docker "Update" command   
@bot.hybrid_command(name="update", description="Update LibreChat")
async def update(ctx):
    os.chdir(WORKING_DIR) # Change the working directory to the specified folder
    status_message = await ctx.send('Update in progress...')
    start_time = time.time()
    commands = [
        'npm run update:docker',
        'docker-compose up -d'
    ]
    await execute_commands_with_status_messages(ctx, commands)
    elapsed_time = time.time() - start_time
    await status_message.edit(content=f'Update completed in {elapsed_time:.2f} seconds.')

@bot.command(name="config", description="Change working directory")
async def config(ctx):
    global WORKING_DIR
    current_working_dir = WORKING_DIR

    # This will make sure that the response will only be registered if the following
    # conditions are met:
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    await ctx.send("Enter the new working directory")

    try:
        # Wait for a message that satisfies the check
        msg = await bot.wait_for("message", check=check, timeout=30) # 30 seconds to reply
        new_working_dir = msg.content # Get the content of the message
    except asyncio.TimeoutError:
        # If the user doesn't reply within 30 seconds, send a message
        await ctx.send("Sorry, you didn't reply in time!")
        return # End the command here

    if new_working_dir == current_working_dir:
        await ctx.send(f"The current working directory is already set to: {current_working_dir}")
    else:
        WORKING_DIR = new_working_dir

        # Update the working directory in bot_config.py
        with open("bot_config.py", "r") as config_file:
            lines = config_file.readlines()

        for i in range(len(lines)):
            if lines[i].startswith("WORKING_DIR"):
                lines[i] = f'WORKING_DIR = "{new_working_dir}"\n'
                break

        with open("bot_config.py", "w") as config_file:
            config_file.writelines(lines)

        await ctx.send(f"Working directory changed from {current_working_dir} to: {new_working_dir}")


# Remove the default help command
bot.remove_command('help')

# Help command
@bot.hybrid_command(name="help", description="Show help message")
async def help(ctx):
    # Create an embed object with a title, color and description
    embed = discord.Embed(title="LibreChat Discord Bot", color=0x00ff00, description="A bot that allows you to control LibreChat from Discord.")

    # Add fields for each slash command with its name and description
    embed.add_field(name="/status", value="Docker status", inline=False)
    embed.add_field(name="/start", value="Start Docker", inline=False)
    embed.add_field(name="/stop", value="Stop Docker", inline=False)
    embed.add_field(name="/update", value="Update LibreChat", inline=False)
    embed.add_field(name="/config", value="Change working directory", inline=False)

    # Add fields for each link with its name and url
    embed.add_field(name="GitHub Repo", value="https://github.com/Berry-13/LibreChat-DiscordBot", inline=False)
    embed.add_field(name="LibreChat Website", value="https://librechat.ai/", inline=False)
    embed.add_field(name="LibreChat Docs", value="https://docs.librechat.ai/", inline=False)
    embed.add_field(name="LibreChat Discord Server", value="https://discord.librechat.ai/", inline=False)

    # Send the embed object as a message
    await ctx.send(embed=embed)

# Function to execute a command and display the status message and log output
async def execute_command_with_status_message(ctx, command):
    start_time = time.time()
    status = await ctx.send(f'Command "{command}"')
    process = await asyncio.create_subprocess_shell(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = await process.communicate()
    elapsed_time = time.time() - start_time

    output = stdout.decode() if stdout else stderr.decode()
    log_message = output[-750:]  # Last 750 characters of the log

    if process.returncode == 0:
        await status.edit(content=f'Command "{command}" executed in {elapsed_time:.2f} seconds:')
    else:
        await status.edit(content=f'Error while executing the command "{command}":')

    if log_message:
        await ctx.send(f'```\n{log_message}\n```')

# Function to execute multiple commands and display the status messages and log outputs
async def execute_commands_with_status_messages(ctx, commands):
    for command in commands:
        await execute_command_with_status_message(ctx, command)

# Run the bot with the provided token
bot.run(TOKEN)