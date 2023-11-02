# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=line-too-long
# pylint: disable=broad-exception-caught
# pylint: disable=import-error

# ⚙️ DOTENV FILE COMMANDS

import os
import importlib
import requests
from interactions import(
    ActionRow,
    Attachment,
    Button,
    ButtonStyle,
    ComponentContext,
    Extension,
    File,
    OptionType,
    SlashContext,
    component_callback,
    slash_command,
    slash_option
)
import bot_config

uploaded_files = {}

class Env(Extension):
    def __init__(self, client):
        self.client = client


    @slash_command(
        name='env',
        description='⚙️ Commands to download/upload/restore the .env file'
        )

    @slash_option(
        name='file',
        description='📄 .env file',
        opt_type=OptionType.ATTACHMENT
        )
    async def env(self, ctx: SlashContext, file: Attachment = None):
        uploaded_files[ctx.author.id] = file

        env_btns = [
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
        await ctx.send("⚙️ .env Commands:", components=env_btns, ephemeral=True)

    # UPLOAD ⏫
    @component_callback("up")
    async def up_callback(self, ctx: ComponentContext):
        importlib.reload(bot_config)
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

                response = requests.get(attachment.url, timeout=5)
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
    async def confirm_upload_callback(self, ctx: ComponentContext):
        importlib.reload(bot_config)
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

            response=requests.get(attachment.url, timeout=5)
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
    async def cancel_upload_callback(self, ctx: ComponentContext):
        await ctx.send("Upload operation cancelled. ❌", ephemeral=True)

    # DOWNLOAD ⏬
    @component_callback("down")
    async def down_callback(self, ctx: ComponentContext):
        importlib.reload(bot_config)
        current_path = bot_config.LIBRECHAT_PATH

        file_name = ".env"
        file_path = os.path.join(current_path, file_name)

        if not os.path.isfile(file_path):
            await ctx.send("The .env file does not exist in the provided directory. 🤔 \n\nUse **/path** if you need to set the LibreChat path", ephemeral=True)
            return

        with open(file_path, "rb") as file:
            await ctx.send(file=File(file, file_name), ephemeral=True)

    # DOWNLOAD .ENV.EXAMPLE 👀
    @component_callback("example")
    async def example_callback(self, ctx: ComponentContext):
        file_name = ".env.example"
        importlib.reload(bot_config)
        current_path = bot_config.LIBRECHAT_PATH
        file_path = os.path.join(current_path, file_name)

        if not os.path.isfile(file_path):
            await ctx.send("The .env.example file does not exist in the provided directory. 🤔 \n\nUse **/path** if you need to set the LibreChat path", ephemeral=True)
            return

        with open(file_path, "rb") as file:
            await ctx.send(file=File(file, file_name), ephemeral=True)

    # RESTORE ⏪
    @component_callback("rest")
    async def rest_callback(self, ctx: ComponentContext):
        importlib.reload(bot_config)
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
    async def confirm_rest_callback(self, ctx: ComponentContext):
        importlib.reload(bot_config)
        current_path = bot_config.LIBRECHAT_PATH

        env_file_path = os.path.join(current_path, ".env")
        env_bak_file_path = os.path.join(current_path, ".env.bak")

        if os.path.isfile(env_file_path):
            os.remove(env_file_path)
        os.rename(env_bak_file_path, env_file_path)
        await ctx.send(".env.bak file restored as .env. ✅ \n\nPlease restart or update LibreChat to apply the changes.", ephemeral=True)

    @component_callback("cancel_rest")
    async def cancel_rest_callback(self, ctx: ComponentContext):
        await ctx.send("Restore operation cancelled. ❌", ephemeral=True)
