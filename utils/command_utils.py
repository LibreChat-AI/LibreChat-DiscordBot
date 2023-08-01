import subprocess
import time
import asyncio

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