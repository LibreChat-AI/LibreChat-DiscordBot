# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=line-too-long
# pylint: disable=anomalous-backslash-in-string

# 🙋 HELP

from interactions import(
    Embed,
    Extension,
    SlashContext,
    slash_command,
)

class Help(Extension):
    @slash_command(
            name="help",
            description="Show a list of available commands"
        )
    async def help_command(self, ctx: SlashContext):
        embed = Embed(
            title="LibreChat Updater",
            description="Here is a list of available commands:",
            color=0x8000ff,
            url="https://github.com/Berry-13/LibreChat-DiscordBot"
        )
        # Add fields for each command
        embed.add_field(
            name="/ping",
            value=
            "☎️ Ping the bot \n"
            "- ping the bot, returns the latency in milliseconds"
        )
        embed.add_field(
            name="/librechat",
            value=
            "🌐 Explore LibreChat URLs \n"
            "- Quick access to LibreChat **GitHub**, **Documentation**, **Discord** and **YouTube**"
        )
        embed.add_field(
            name="/path",
            value=
            "📂 Configure the LibreChat path\n"
            "- Set the path of the LibreChat folder.\n"
            "- Use either the absolute path format\n"
            "Example: `C:\LibreChat`\n"
            "- or the relative path format (relative to the bot folder).\n"
            "Example: `../LibreChat`"
        )
        embed.add_field(
            name="/env",
            value=
            "⚙️ Manage the .env file\n"
            "- **Download**: Download a copy of the .env file from the LibreChat folder.\n"
            "- **Upload**: Upload a new `.env` file to replace the current one (You must include the `.env` file when calling **/env**) This command will also backup your current `.env` file before replacing it with the uploaded file \n"
            "- **Restore**: Restore the `.env` file backup and __**delete**__ the current .env file \n"
            "- **Example**: Download the `.env.example` from the LibreChat folder"
        )
        embed.add_field(
            name="/docker",
            value=
            "🐳 Regular Docker commands\n"
            "- **Start**: Start the docker container\n"
            "- **Stop**: Stop the docker container\n"
            "- **Update**: Update LibreChat (this may take several minutes).\n"
            "- **Status**: Display the status of all Docker containers."
        )
        embed.add_field(
            name="/docker-single",
            value=
            "🐳 Docker commands for `single-compose.yml`\n"
            "- **Start**: Start the docker container\n"
            "- **Stop**: Stop the docker container\n"
            "- **Update**: Update LibreChat (this may take several minutes).\n"
            "- **Status**: Display the status of all Docker containers."
        )
        embed.add_field(
            name="/local",
            value=
            "💻 Commands for local LibreChat install\n"
            "- **Start**: start LibreChat\n"
            "- **Stop**: Stop LibreChat\n"
            "- **Update**: Update LibreChat (this may take several minutes)."
        )
        embed.add_field(
            name="/balance",
            value=
            "💸 Set credit balance for a user\n"
            "- user email is required\n"
            "- Set the following .env variable to enable this `CHECK_BALANCE=true`\n"
            "- 1000 credits = $0.001"
        )
        embed.add_field(
            name="/ban",
            value=
            "🔨 Ban a user\n"
            "- User's email is required\n Enter the duration in minutes, hours, days\n"
        )
        embed.add_field(
            name="---",
            value="\n"
        )
        embed.add_field(
            name="Visit our GitHub page for the latest updates, additional information or to report any problems",
            value="**[GitHub](https://github.com/Berry-13/LibreChat-DiscordBot)**"
        )

        await ctx.send(embed=embed, ephemeral=True)
