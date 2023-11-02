# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=line-too-long
# pylint: disable=anomalous-backslash-in-string
# pylint: disable=broad-exception-caught
# pylint: disable=import-error

# 📂 SET LIBRECHAT DIR

import importlib
from interactions import(
    Extension,
    Modal,
    ShortText,
    SlashContext,
    slash_command,
)
import bot_config

class Path(Extension):

    @slash_command(
        name="path",
        description="📂 Configure the LibreChat path"
    )
    async def set_path(self, ctx: SlashContext):
        importlib.reload(bot_config)
        current_path = bot_config.LIBRECHAT_PATH

        path = await self.send_path_modal(ctx)
        new_path = await self.handle_path_response(ctx, path, current_path)

        if new_path is not None:
            bot_config.LIBRECHAT_PATH = new_path


    async def send_path_modal(self, ctx):
        path = Modal(
            ShortText(
                label="📂 Enter the LibreChat folder path",
                custom_id="new_path",
                value=f"{bot_config.LIBRECHAT_PATH}",
            ),
            title="LibreChat Path",
        )
        await ctx.send_modal(modal=path)
        return path

    async def handle_path_response(self, ctx: SlashContext, path, current_path):
        old_path = current_path
        modal_ctx = await ctx.bot.wait_for_modal(path)  # Pass the custom_id as the path parameter
        new_path = modal_ctx.responses["new_path"]

        try: # try to open and write to the file
            with open("bot_config.py", "r", encoding="utf-8") as file: # open the file in read mode
                lines = file.readlines() # store the lines in a variable

            for i, line in enumerate(lines):
                if line.startswith("LIBRECHAT_PATH"):
                    lines[i] = f'LIBRECHAT_PATH = "{new_path}"\n'
                    break

            with open("bot_config.py", "w", encoding="utf-8") as file: # open the file again in write mode
                file.writelines(lines) # write the modified lines to the file

            await modal_ctx.send(f"Path updated successfully! ✅ \n\n📂 Path changed from **{old_path}** to **{new_path}**", ephemeral=True)

            return new_path

        except Exception as e: # catch any errors or exceptions
            await ctx.send(f"Oops, something went wrong. 😢 \nThe error message is: {e}", ephemeral=True)
            return current_path
