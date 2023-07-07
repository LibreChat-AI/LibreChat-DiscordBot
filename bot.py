import discord
import os
import subprocess
import time
import asyncio

##############################################################################################################################

TOKEN = 'your-discord-bot-token'
USER_ID = 'your-discord-user-id'

##############################################################################################################################

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

        try:
            start_time = time.time()

            # Execute command "docker-compose stop"
            stop_command = 'docker-compose stop'
            await execute_command_with_status_message(status_message, stop_command, start_time)

            # Execute command "git pull"
            pull_command = 'git pull'
            await execute_command_with_status_message(status_message, pull_command, start_time)

            # Execute command "docker-compose build"
            build_command = 'docker-compose build'
            await execute_command_with_status_message(status_message, build_command, start_time)

            # Execute command "docker-compose up -d"
            up_command = 'docker-compose up -d'
            await execute_command_with_status_message(status_message, up_command, start_time)

            elapsed_time = time.time() - start_time
            await status_message.edit(content=f'✅ UPDATE SUCCESSFUL ✅')

        except subprocess.CalledProcessError as e:
            await status_message.edit(content=f'❌ UPDATE FAILED ❌\nError during the update.:\n```\n{e.output.decode()}\n```')

async def execute_command_with_status_message(message, command, start_time):
    log_message = ''
    elapsed_time = time.time() - start_time

    status = await message.channel.send(f'Command "{command}" ({elapsed_time:.2f}s)')
    process = await asyncio.create_subprocess_shell(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    while True:
        elapsed_time = time.time() - start_time
        await status.edit(content=f'Command "{command}" ({elapsed_time:.2f}s)')

        try:
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=1)
        except asyncio.TimeoutError:
            continue

        output = stdout.decode() if stdout else stderr.decode()
        log_message += output[-500:]  # Last 500 character of the log

        if process.returncode == 0:
            await status.edit(content=f'Command "{command}" executed in {elapsed_time:.2f} seconds:')
            break
        else:
            await status.edit(content=f'Error while executing the command "{command}":')
            break

    if log_message:
        await message.channel.send(f'```\n{log_message}\n```')

client.run(TOKEN)
