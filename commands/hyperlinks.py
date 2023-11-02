# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

# 🌐 USEFUL URLs

from interactions import(
    ActionRow,
    Button,
    ButtonStyle,
    Extension,
    SlashContext,
    slash_command
)

class Hyperlinks(Extension):
    @slash_command(
            name='librechat',
            description='🌐 LibreChat URLs'
            )
    async def librechat(self, ctx: SlashContext):
        components: list[ActionRow] = [
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
        await ctx.send("Useful LibreChat links:", components=components)
