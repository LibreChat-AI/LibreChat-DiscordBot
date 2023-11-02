# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=line-too-long
# pylint: disable=broad-exception-caught
# pylint: disable=import-error

# 💻 LOCAL INSTALLATION COMMANDS

from interactions import(
    ActionRow,
    Button,
    ButtonStyle,
    ComponentContext,
    Extension,
    SlashContext,
    component_callback,
    slash_command,
)
from utils.utils import(
    run_shell_command,
    run_local_shell_command
)

class Local(Extension):
    @slash_command(
            name='local',
            description='💻 Commands for "local" LibreChat install'
            )
    async def local(self, ctx: SlashContext):
        local_btns = [
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
        await ctx.send("💻 Local Commands:", components=local_btns, ephemeral=True)

    @component_callback("start-l")
    async def start_l_callback(self, ctx: ComponentContext):
        command = 'npm run backend'
        await ctx.send("▶️ Starting the local instance of LibreChat...", ephemeral=True)
        await run_local_shell_command(ctx, command)

    @component_callback("stop-l")
    async def stop_l_callback(self, ctx: ComponentContext):
        command = 'npm run backend:stop'
        await ctx.send("🛑 Stopping the local instance of LibreChat...", ephemeral=True)
        await run_shell_command(ctx, command)

    @component_callback("update-l")
    async def update_l_callback(self, ctx: ComponentContext):
        await ctx.send("This will first stop the services, then proceed with the update.", ephemeral=True)
        command1 = 'npm run backend:stop'
        command2 = 'npm run update:local'
        await run_shell_command(ctx, command=command1)
        await ctx.send("Update in progress...\nThis might take a couple of minutes... ⌛", ephemeral=True)
        await run_shell_command(ctx, command=command2)
