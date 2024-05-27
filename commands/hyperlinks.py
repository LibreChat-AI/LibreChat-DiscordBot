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
                    label="LibreChat.ai",
                    url="https://librechat.ai"
                ),
                Button(
                    style=ButtonStyle.URL,
                    label="Docs",
                    url="https://www.librechat.ai/docs"
                ),
                Button(
                    style=ButtonStyle.URL,
                    label="Discord",
                    url="https://discord.librechat.ai"
                ),
                Button(
                    style=ButtonStyle.URL,
                    label="Github",
                    url="https://github.librechat.ai"
                ),
                Button(
                    style=ButtonStyle.URL,
                    label="Youtube",
                    url="https://www.youtube.com/@LibreChat"
                ),
                Button(
                    style=ButtonStyle.URL,
                    label="Twitter",
                    url="https://twitter.com/LibreChatAI"
                ),
                Button(
                    style=ButtonStyle.URL,
                    label="Linkedin",
                    url="https://www.linkedin.com/company/100468026"
                )
            )
        ]
        await ctx.send("Useful LibreChat links:", components=components)
