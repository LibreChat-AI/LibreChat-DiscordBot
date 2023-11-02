# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=line-too-long
# pylint: disable=broad-exception-caught
# pylint: disable=import-error

# 🐳 DOCKER

from interactions import(
    ActionRow,
    Button,
    ButtonStyle,
    ComponentContext,
    Extension,
    SlashContext,
    component_callback,
    slash_command
)
from utils.utils import(
    run_shell_command,
)


class Docker(Extension):
    @slash_command(name='docker', description='🐳 Docker Commands')
    async def docker(self, ctx: SlashContext):
        docker_btns = [
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
        await ctx.send("🐳 Docker Commands:", components=docker_btns, ephemeral=True)

    @component_callback("start")
    async def start_callback(self, ctx: ComponentContext):
        command = 'docker-compose up -d'
        await ctx.send("▶️ Starting the docker container...", ephemeral=True)
        await run_shell_command(ctx, command)

    @component_callback("stop")
    async def stop_callback(self, ctx: ComponentContext):
        command = 'docker-compose stop'
        await ctx.send("🛑 Stopping the docker container...", ephemeral=True)
        await run_shell_command(ctx, command)

    @component_callback("update")
    async def update_callback(self, ctx: ComponentContext):
        command = 'npm run update:docker'
        await ctx.send("Update in progress... This might take a couple of minutes... ⌛", ephemeral=True)
        await run_shell_command(ctx, command)

    @component_callback("status")
    async def status_callback(self, ctx: ComponentContext):
        command = 'docker ps -a'
        await ctx.send("👀 Docker Status", ephemeral=True)
        await run_shell_command(ctx, command)
