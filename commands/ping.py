# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

# ☎️ PING

from interactions import(
    Extension,
    SlashContext,
    slash_command
)


class Ping(Extension):
    def __init__(self, client):
        self.client = client

    @slash_command(name="ping", description="☎️ Ping")
    async def ping(self, ctx: SlashContext):
        latency_ms = round(self.client.latency * 1000, 2)
        await ctx.send(f"Ping: {latency_ms}ms", ephemeral=True)
