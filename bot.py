import discord
import subprocess
import time
import asyncio

TOKEN = 'your-discord-bot-token'
USER_ID = 'your-discord-client-id'

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Connected as {client.user.name}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == 'update' and str(message.author.id) == USER_ID:
        status_message = await message.channel.send('Update in progress...')
        start_time = time.time()
        commands = [
            'docker-compose stop',
            'git pull',
            'docker-compose build',
            'docker-compose up -d'
        ]
        await execute_commands_with_status_messages(status_message, commands)
        elapsed_time = time.time() - start_time
        await status_message.edit(content=f'Update completed in {elapsed_time:.2f} seconds.')

    if message.content == 'start' and str(message.author.id) == USER_ID:
        status_message = await message.channel.send('Starting docker...')
        command = 'docker-compose up -d'
        await execute_command_with_status_message(status_message, command)

async def execute_command_with_status_message(message, command):
    start_time = time.time()
    status = await message.channel.send(f'Command "{command}"')
    process = await asyncio.create_subprocess_shell(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = await process.communicate()
    elapsed_time = time.time() - start_time

    output = stdout.decode() if stdout else stderr.decode()
    log_message = output[-500:]  # Last 500 characters of the log

    if process.returncode == 0:
        await status.edit(content=f'Command "{command}" executed in {elapsed_time:.2f} seconds:')
    else:
        await status.edit(content=f'Error while executing the command "{command}":')

    if log_message:
        await message.channel.send(f'```\n{log_message}\n```')

async def execute_commands_with_status_messages(status_message, commands):
    for command in commands:
        await execute_command_with_status_message(status_message, command)

client.run(TOKEN)
