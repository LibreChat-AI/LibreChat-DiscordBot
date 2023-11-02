# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=line-too-long
# pylint: disable=broad-exception-caught
# pylint: disable=import-error

# 🐳 SINGLE-DOCKER

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


class Single(Extension):
    @slash_command(
            name='docker-single',
            description='🐳 Docker Commands for single-compose.yml'
            )
    async def single(self, ctx: SlashContext):
        single_btns = [
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
        await ctx.send("🐳 'single-compose' Docker Commands:", components=single_btns, ephemeral=True)

    @component_callback("start-s")
    async def start_s_callback(self, ctx: ComponentContext):
        command = 'docker-compose -f ./docs/dev/single-compose.yml up -d'
        await ctx.send("▶️ Starting the docker container...", ephemeral=True)
        await run_shell_command(ctx, command)

    @component_callback("stop-s")
    async def stop_s_callback(self, ctx: ComponentContext):
        command = 'docker-compose -f ./docs/dev/single-compose.yml stop'
        await ctx.send("🛑 Stopping the docker container...", ephemeral=True)
        await run_shell_command(ctx, command)

    @component_callback("update-s")
    async def update_s_callback(self, ctx: ComponentContext):
        command = 'npm run update:single'
        await ctx.send("Update in progress... This might take a couple of minutes... ⌛", ephemeral=True)
        await run_shell_command(ctx, command)
