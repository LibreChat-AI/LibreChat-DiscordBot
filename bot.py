import interactions #Interactions.py 5.9.2
from interactions import *
import bot_config
import logging
import os
import time
import asyncio
import subprocess
import requests

TOKEN = bot_config.TOKEN

logging.basicConfig()
cls_log = logging.getLogger('MyLogger')
cls_log.setLevel(logging.INFO)

client = Client(intents=interactions.Intents.ALL, token=TOKEN, sync_interactions=True, asyncio_debug=False, logger=cls_log, send_command_tracebacks=False)


# 👂
@listen()
async def on_startup():
    print(f'{client.user} connected to discord')
    print('----------------------------------------------------------------------------------------------------------------')
    print(f'Bot invite link: https://discord.com/api/oauth2/authorize?client_id={bot_config.CLIENT_ID}&permissions=551903348736&scope=bot')
    print('----------------------------------------------------------------------------------------------------------------')


# 📞 PING
@slash_command(name="ping", description="📞 Ping")
async def ping(ctx: SlashContext):
    latency_ms = round(client.latency * 1000, 2)
    await ctx.send(f"Ping: {latency_ms}ms", ephemeral=True)


# 📄 HELP
@slash_command(name="help", description="Show a list of available commands")
async def help_command(ctx: SlashContext):
    embed = interactions.Embed(title="LibreChat Updater", description="Here is a list of available commands:", color=0x8000ff, url="https://github.com/Berry-13/LibreChat-DiscordBot")
    
    # Add fields for each command
    embed.add_field(
        name="/ping", 
        value="📞 Ping the bot \n"
        "- ping the bot, returns the latency in milliseconds"
        )
    embed.add_field(
        name="/librechat", 
        value="🌐 Explore LibreChat URLs \n"
        "- Quick access to LibreChat **GitHub**, **Documentation**, **Discord** and **YouTube**"
        )
    embed.add_field(
        name="/path", 
        value="📂 Configure the LibreChat path \n"
        "- Set the path of the LibreChat folder. \n"
        "- Use either the absolute path format \n"
        "Example: `C:\LibreChat` \n"
        "- or the relative path format (relative to the bot folder).\n"
        "Example: `../LibreChat`"
        )
    embed.add_field(
        name="/env", 
        value="⚙️ Manage the .env file \n"
        "- **Download**: Download a copy of the .env file from the LibreChat folder. \n"
        "- **Upload**: Upload a new `.env` file to replace the current one (You must include the `.env` file when calling **/env**) This command will also backup your current `.env` file before replacing it with the uploaded file \n"
        "- **Restore**: Restore the `.env` file backup and __**delete**__ the current .env file \n"
        "- **Example**: Download the `.env.example` from the LibreChat folder"
        )
    embed.add_field(
        name="/docker", 
        value="🐳 Regular Docker commands \n"
        "- **Start**: Start the docker container \n"
        "- **Stop**: Stop the docker container \n"
        "- **Update**: Update LibreChat (this may take several minutes). \n"
        "- **Status**: Display the status of all Docker containers."
        )
    embed.add_field(
        name="/docker-single", 
        value="🐳 Docker commands for `single-compose.yml` \n"
        "- **Start**: Start the docker container \n"
        "- **Stop**: Stop the docker container \n"
        "- **Update**: Update LibreChat (this may take several minutes). \n"
        "- **Status**: Display the status of all Docker containers."
        )
    embed.add_field(
        name="/local", 
        value=
        "💻 Commands for local LibreChat install \n"
        "- **Start**: start LibreChat \n"
        "- **Stop**: Stop LibreChat \n"
        "- **Update**: Update LibreChat (this may take several minutes)."
        )
    embed.add_field(
        name="/balance", 
        value=
        "💸 Set credit balance for a user \n"
        "- user email is required \n"
        "- Set the following .env variable to enable this `CHECK_BALANCE=true` \n"
        "- 1000 credits = $0.001"
        )
    embed.add_field(
        name="---",
        value=" \n"
    )
    embed.add_field(
        name="Visit our GitHub page for the latest updates, additional information or to report any problems",
        value="**[GitHub](https://github.com/Berry-13/LibreChat-DiscordBot)**"
    )

    await ctx.send(embed=embed, ephemeral=True)


# 🌐 LIBRECHAT HYPERLINKS 
@slash_command(name='librechat', description='🌐 LibreChat URLs')
async def librechat(ctx: SlashContext):
    librechat = [
        ActionRow(
            Button(
                style=ButtonStyle.URL,
                label="GitHub",
                url="https://librechat.ai"
            ),
            Button(
                style=ButtonStyle.URL,
                label="Docs",
                url="https://docs.librechat.ai"
            ),
            Button(
                style=ButtonStyle.URL,
                label="Discord",
                url="https://discord.librechat.ai"
            ),
            Button(
                style=ButtonStyle.URL,
                label="Youtube",
                url="https://www.youtube.com/@LibreChat"
            )
        )
    ]
    await ctx.send("Useful LibreChat links:", components=librechat)


# 📂 LIBRECHAT DIR
@slash_command(name="path", description="📂 Configure the LibreChat path")
async def set_path(ctx: SlashContext):
    import bot_config
    current_path = bot_config.LIBRECHAT_PATH

    path = await send_path_modal(ctx, current_path)
    new_path = await handle_path_response(ctx, path, current_path)

    if new_path is not None:
        bot_config.LIBRECHAT_PATH = new_path

async def send_path_modal(ctx: SlashContext, current_path):
    path = Modal(
        ShortText(
            label=f"📂 Enter the LibreChat folder path",
            custom_id="new_path",
            value=f"{current_path}",
        ),
        title="LibreChat Path",
    )
    await ctx.send_modal(modal=path)
    return path

async def handle_path_response(ctx: SlashContext, path, current_path):
    old_path = current_path
    modal_ctx = await ctx.bot.wait_for_modal(path)  # Pass the custom_id as the path parameter
    new_path = modal_ctx.responses["new_path"]
    
    try: # try to open and write to the file
        with open("bot_config.py", "r") as file: # open the file in read mode
            lines = file.readlines() # store the lines in a variable

        for i in range(len(lines)):
            if lines[i].startswith("LIBRECHAT_PATH"):
                lines[i] = f'LIBRECHAT_PATH = "{new_path}"\n'
                break

        with open("bot_config.py", "w") as file: # open the file again in write mode
            file.writelines(lines) # write the modified lines to the file

        await modal_ctx.send(f"Path updated successfully! ✅ \n\n📂 Path changed from **{old_path}** to **{new_path}**", ephemeral=True)
        
        return new_path

    except Exception as e: # catch any errors or exceptions
        await ctx.send(f"Oops, something went wrong. 😢 \nThe error message is: {e}", ephemeral=True)
        return current_path


# 💸 ADD BALANCE
@slash_command(name="balance", description="💸 Add credit to user’s balance")

async def balance_modal(ctx: SlashContext):
    balance = Modal(
        ShortText(
            label="📧 User's email",
            custom_id="email",
            required=True,
            min_length=6,
            max_length=64,
            placeholder="example@example.com",
        ),
        ShortText(
            label="💰 Credit quantity - 1000 credits = $0.001",
            custom_id="credits",
            required=True,
            min_length=4,
            max_length=12,
            placeholder="Enter a number between 1000 and 999999999999",
        ),
        title="💸 Set Balance",
        custom_id="balance",
    )
    await ctx.send_modal(modal=balance)

@modal_callback("balance")
async def on_modal_answer(ctx: ModalContext, email: str, credits: str):
    command = f"npm run add-balance {email} {credits}"
    await ctx.send(f"{command}", ephemeral=True)
    await run_shell_command(ctx, command)

# ⚙️ DOTENV FILE COMMANDS
uploaded_files = {}

@slash_command(name='env', description='⚙️ Commands to download/upload/restore the .env file')
@slash_option(name='file', description='📄 .env file', opt_type=OptionType.ATTACHMENT)
async def env(ctx: SlashContext, file: Attachment = None):
    uploaded_files[ctx.author.id] = file

    env = [
        ActionRow(
            Button(
                style=ButtonStyle.GREEN,
                label="Download",
                custom_id="down",
            ),
            Button(
                style=ButtonStyle.RED,
                label="Upload ⚠️",
                custom_id="up",
            ),
            Button(
                style=ButtonStyle.RED,
                label="Restore ⚠️",
                custom_id="rest",
            ),
            Button(
                style=ButtonStyle.BLUE,
                label="Example",
                custom_id="example",
            )
        )
    ]
    await ctx.send("⚙️ .env Commands:", components=env, ephemeral=True)

# UPLOAD ⏫
@component_callback("up")
async def up_callback(ctx: ComponentContext):
    import bot_config
    current_path = bot_config.LIBRECHAT_PATH
    
    file = uploaded_files.get(ctx.author.id)
    if file is None:
        await ctx.send("No file uploaded.👀 \n\nPlease upload an .env file with the **/env** command to use this feature")
        return
    
    attachment = file
    file_name = attachment.filename
    
    if not file_name.endswith("env"):
        await ctx.send("⛔Invalid file format.⛔ \n\nPlease upload an .env file.", ephemeral=True)
        return
    
    file_path = os.path.join(current_path, ".env")
    existing_file_path = os.path.join(current_path, ".env.bak")
    temp_file_path = os.path.join(current_path, ".env.bak.temp")
    
    if os.path.isfile(file_path):
        confirmation = [
            ActionRow(
                Button(
                    style=ButtonStyle.SUCCESS,
                    label="✔️",
                    custom_id="confirm_upload",
                ),
                Button(
                    style=ButtonStyle.DANGER,
                    label="✖️",
                    custom_id="cancel_upload",
                )
            )
        ]
        await ctx.send("⚠️ Are you sure you want to upload a new .env file? If you proceed, your current .env file will be backed up and can be restored using the restore function.", components=confirmation, ephemeral=True)
    else:
        try:
            if os.path.isfile(existing_file_path):
                os.rename(existing_file_path, temp_file_path)
    
            os.rename(file_path, existing_file_path)
            await ctx.send("💾 Existing .env file renamed to .env.bak.", ephemeral=True)
    
            response = requests.get(attachment.url)
            with open(file_path, "wb") as f:
                f.write(response.content)
    
            await ctx.send("Uploaded .env file to the LibreChat directory. 🎉 \n\nPlease restart or update LibreChat to apply the changes.", ephemeral=True)
            
            if os.path.isfile(temp_file_path):
                os.remove(temp_file_path)
    
        except Exception as e:
            if os.path.isfile(temp_file_path):
                if os.path.isfile(existing_file_path):
                    os.rename(temp_file_path, existing_file_path)
                else:
                    os.rename(temp_file_path, file_path)
    
            await ctx.send(f"😬 An error occurred while saving the file: {str(e)}", ephemeral=True)


@component_callback("confirm_upload")
async def confirm_upload_callback(ctx: ComponentContext):
    import bot_config
    current_path = bot_config.LIBRECHAT_PATH
    
    file = uploaded_files.get(ctx.author.id)
    if file is None:
        await ctx.send("No file uploaded.👀 \n\nPlease upload an .env file with the **/env** command to use this feature")
        return
    
    attachment = file
    file_path = os.path.join(current_path, ".env")
    existing_file_path = os.path.join(current_path, ".env.bak")
    temp_file_path = os.path.join(current_path, ".env.bak.temp")
    
    try:
        if os.path.isfile(existing_file_path):
            os.rename(existing_file_path, temp_file_path)

        os.rename(file_path, existing_file_path)
        await ctx.send("💾 Existing .env file renamed to .env.bak.", ephemeral=True)

        response = requests.get(attachment.url)
        with open(file_path, "wb") as f:
            f.write(response.content)

        await ctx.send("Uploaded .env file to the LibreChat directory. 🎉 \n\nPlease restart or update LibreChat to apply the changes.", ephemeral=True)

        if os.path.isfile(temp_file_path):
            os.remove(temp_file_path)

    except Exception as e:
        if os.path.isfile(temp_file_path):
            if os.path.isfile(existing_file_path):
                os.rename(temp_file_path, existing_file_path)
            else:
                os.rename(temp_file_path, file_path)

        await ctx.send(f"😬 An error occurred while saving the file: {str(e)}", ephemeral=True)


@component_callback("cancel_upload")
async def cancel_upload_callback(ctx: ComponentContext):
    await ctx.send("Upload operation cancelled. ❌", ephemeral=True)

# DOWNLOAD ⏬
@component_callback("down")
async def down_callback(ctx: ComponentContext):
    import bot_config
    current_path = bot_config.LIBRECHAT_PATH

    file_name = ".env"
    file_path = os.path.join(current_path, file_name)

    if not os.path.isfile(file_path):
        await ctx.send("The .env file does not exist in the provided directory. 🤔 \n\nUse **/path** if you need to set the LibreChat path", ephemeral=True)
        return

    with open(file_path, "rb") as file:
        await ctx.send(file=interactions.File(file, file_name), ephemeral=True)

# DOWNLOAD .ENV.EXAMPLE 👀
@component_callback("example")
async def example_callback(ctx: ComponentContext):
    file_name = ".env.example"
    import bot_config
    current_path = bot_config.LIBRECHAT_PATH
    file_path = os.path.join(current_path, file_name)

    if not os.path.isfile(file_path):
        await ctx.send("The .env.example file does not exist in the provided directory. 🤔 \n\nUse **/path** if you need to set the LibreChat path", ephemeral=True)
        return

    with open(file_path, "rb") as file:
        await ctx.send(file=interactions.File(file, file_name), ephemeral=True)

# RESTORE ⏪
from interactions import ButtonStyle

@component_callback("rest")
async def rest_callback(ctx: ComponentContext):
    import bot_config
    current_path = bot_config.LIBRECHAT_PATH
    
    env_file_path = os.path.join(current_path, ".env")
    env_bak_file_path = os.path.join(current_path, ".env.bak")

    if os.path.isfile(env_file_path) and os.path.isfile(env_bak_file_path):
        confirmation = [
            ActionRow(
                Button(
                    style=ButtonStyle.SUCCESS,
                    label="✔️",
                    custom_id="confirm_rest",
                ),
                Button(
                    style=ButtonStyle.DANGER,
                    label="✖️",
                    custom_id="cancel_rest",
                )
            )
        ]
        await ctx.send("⚠️ Are you sure you want to restore the .env file? This will delete the current .env file and restore the .env.bak file.", components=confirmation, ephemeral=True)
    elif os.path.isfile(env_file_path):
        await ctx.send("No backup file (.env.bak) found. 😔", ephemeral=True)
    elif os.path.isfile(env_bak_file_path):
        confirmation = [
            ActionRow(
                Button(
                    style=ButtonStyle.SUCCESS,
                    label="✔️",
                    custom_id="confirm_rest",
                ),
                Button(
                    style=ButtonStyle.DANGER,
                    label="✖️",
                    custom_id="cancel_rest",
                )
            )
        ]
        await ctx.send("⚠️ Are you sure you want to restore the .env file? \nThis will delete the current .env file and restore the .env.bak file.", components=confirmation, ephemeral=True)
    else:
        await ctx.send("Both .env and .env.bak files do not exist in the current directory. 🤷‍♂️ \n\nUse /path if you need to update the LibreChat path", ephemeral=True)

@component_callback("confirm_rest")
async def confirm_rest_callback(ctx: ComponentContext):
    import bot_config
    current_path = bot_config.LIBRECHAT_PATH
    
    env_file_path = os.path.join(current_path, ".env")
    env_bak_file_path = os.path.join(current_path, ".env.bak")
    
    if os.path.isfile(env_file_path):
        os.remove(env_file_path)
    os.rename(env_bak_file_path, env_file_path)
    await ctx.send(".env.bak file restored as .env. ✅ \n\nPlease restart or update LibreChat to apply the changes.", ephemeral=True)

@component_callback("cancel_rest")
async def cancel_rest_callback(ctx: ComponentContext):
    await ctx.send("Restore operation cancelled. ❌", ephemeral=True)


# 🐳 DOCKER
@slash_command(name='docker', description='🐳 Docker Commands')
async def docker(ctx: SlashContext):
    docker = [
        ActionRow(
            Button(
                style=ButtonStyle.GREEN,
                label="Start",
                custom_id="start",
            ),
            Button(
                style=ButtonStyle.RED,
                label="Stop",
                custom_id="stop",
            ),
            Button(
                style=ButtonStyle.BLUE,
                label="Update",
                custom_id="update",
            ),
            Button(
                style=ButtonStyle.GREY,
                label="Status",
                custom_id="status",
            )
        )
    ]
    await ctx.send("🐳 Docker Commands:", components=docker, ephemeral=True)

@component_callback("start")
async def start_callback(ctx: ComponentContext):
    command = 'docker-compose up -d'
    await ctx.send("▶️ Starting the docker container...", ephemeral=True)
    await run_shell_command(ctx, command)

@component_callback("stop")
async def stop_callback(ctx: ComponentContext):
    command = 'docker-compose stop'
    await ctx.send("🛑 Stopping the docker container...", ephemeral=True)
    await run_shell_command(ctx, command)

@component_callback("update")
async def update_callback(ctx: ComponentContext):
    command = 'npm run update:docker'
    await ctx.send("Update in progress... This might take a couple of minutes... ⌛", ephemeral=True)
    await run_shell_command(ctx, command)

@component_callback("status")
async def status_callback(ctx: ComponentContext):
    command = 'docker ps -a'
    await ctx.send("👀 Docker Status", ephemeral=True)
    await run_shell_command(ctx, command)


# 🐳 SINGLE_COMPOSE DOCKER
@slash_command(name='docker-single', description='🐳 Docker Commands for single-compose.yml')
async def single(ctx: SlashContext):
    single = [
        ActionRow(
            Button(
                style=ButtonStyle.GREEN,
                label="Start",
                custom_id="start-s",
            ),
            Button(
                style=ButtonStyle.RED,
                label="Stop",
                custom_id="stop-s",
            ),
            Button(
                style=ButtonStyle.BLUE,
                label="Update",
                custom_id="update-s",
            ),
            Button(
                style=ButtonStyle.GREY,
                label="Status",
                custom_id="status",
            )
        )
    ]
    await ctx.send("🐳 Docker Commands:", components=single, ephemeral=True)

@component_callback("start-s")
async def start_s_callback(ctx: ComponentContext):
    command = 'docker-compose -f ./docs/dev/single-compose.yml up -d'
    await ctx.send("▶️ Starting the docker container...", ephemeral=True)
    await run_shell_command(ctx, command)

@component_callback("stop-s")
async def stop_s_callback(ctx: ComponentContext):
    command = 'docker-compose -f ./docs/dev/single-compose.yml stop'
    await ctx.send("🛑 Stopping the docker container...", ephemeral=True)
    await run_shell_command(ctx, command)

@component_callback("update-s")
async def update_s_callback(ctx: ComponentContext):
    command = 'npm run update:single'
    await ctx.send("Update in progress... This might take a couple of minutes... ⌛", ephemeral=True)
    await run_shell_command(ctx, command)


# 💻 LOCAL
@slash_command(name='local', description='💻 Commands for "local" LibreChat install')
async def local(ctx: SlashContext):
    local = [
        ActionRow(
            Button(
                style=ButtonStyle.GREEN,
                label="Start",
                custom_id="start-l",
            ),
            Button(
                style=ButtonStyle.RED,
                label="Stop",
                custom_id="stop-l",
            ),
            Button(
                style=ButtonStyle.BLUE,
                label="Update",
                custom_id="update-l",
            )
        )
    ]
    await ctx.send("💻 Local Commands:", components=local, ephemeral=True)

@component_callback("start-l")
async def start_l_callback(ctx: ComponentContext):
    command = 'npm run backend'
    await ctx.send("▶️ Starting the local instance of LibreChat...", ephemeral=True)
    await run_local_shell_command(ctx, command)

@component_callback("stop-l")
async def stop_l_callback(ctx: ComponentContext):
    command = 'npm run backend:stop'
    await ctx.send("🛑 Stopping the local instance of LibreChat...", ephemeral=True)
    await run_shell_command(ctx, command)

@component_callback("update-l")
async def update_l_callback(ctx: ComponentContext):
    await ctx.send("Update in progress... This might take a couple of minutes... ⌛", ephemeral=True)
    command1 = 'npm run backend:stop'
    command2 = 'npm run update:local'
    await run_shell_command(ctx, command=command1)
    await run_shell_command(ctx, command=command2)


# 🖨️ SHELL COMMAND
async def run_shell_command(ctx: interactions.SlashContext, command):
    import bot_config
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
async def run_local_shell_command(ctx: interactions.SlashContext, command):
    import bot_config
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


client.start()
