# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=line-too-long
# pylint: disable=broad-exception-caught
# pylint: disable=import-error

# 💻 SHELL COMMANDS

import asyncio
import time
import importlib
import subprocess
import bot_config

# 🖨️ SHELL COMMAND
async def run_shell_command(ctx, command):
    importlib.reload(bot_config)
    current_path = bot_config.LIBRECHAT_PATH
    start_time = time.time()

    process = await asyncio.create_subprocess_shell(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=current_path
    )

    stdout, stderr = await process.communicate()
    elapsed_time = time.time() - start_time

    output = stdout.decode() if stdout else stderr.decode()
    log_message = output[-1000:]

    if process.returncode == 0 or command == "npm run backend:stop":
        initial_content = f'💫 Command "{command}" executed in {elapsed_time:.2f} seconds:'
    else:
        error_message = stderr.decode() if stderr else "Unknown error occurred"
        initial_content = f'⚠️ Error while executing the command "{command}": \n\n{error_message}'

    if log_message:
        message = f'"{initial_content}"\n```\n{log_message}\n```'
    else:
        message = initial_content

    await ctx.send(message, ephemeral=True)


# 🖨️ LOCAL SHELL COMMAND (FOR "npm run start" STREAMED OUTPUT)
async def run_local_shell_command(ctx, command):
    importlib.reload(bot_config)
    current_path = bot_config.LIBRECHAT_PATH
    start_time = time.time()
    try:
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=current_path
        )

        output_lines = []
        success_flag = False  # Flag to track success condition
        async for line in process.stdout:
            line = line.decode()
            output_lines.append(line)

            # Uncomment the line below if you want to see each line as it's received
            # await ctx.edit(content=f'```\n{line}\n```')

            if "Server listening on all interfaces" in line:
                elapsed_time = time.time() - start_time
                success = f'💫 Command "{command}" executed in {elapsed_time:.2f} seconds:\n```\n{"".join(output_lines)}\n```'
                success_flag = True
                break

        if success_flag:
            await ctx.edit(content=success)  # Display success output if success_flag is True

        else:
            output_err = []
            async for line in process.stderr:
                line = line.decode()
                output_err.append(line)

            if not output_err:
                fail = f'⚠️ Error while executing the command "{command}": No output received.\n'
            else:
                fail = f'⚠️ Error while executing the command "{command}":\n\n```{"".join(output_err)}\n```'
            await ctx.edit(content=fail)  # Display failure output

    except asyncio.CancelledError:
        await ctx.send(content=f'Command "{command}" cancelled.', ephemeral=True)

    except Exception as e:
        await ctx.send(content=f'Error occurred while executing the command `{command}`: {e}', ephemeral=True)
