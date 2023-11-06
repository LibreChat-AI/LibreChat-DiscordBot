# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=import-error

# 🙆 ADD USER

from interactions import(
    Extension,
    Modal,
    ModalContext,
    ShortText,
    SlashContext,
    modal_callback,
    slash_command,
)
from utils.utils import run_shell_command

class AddUser(Extension):
    @slash_command(name="add-user", description="🙆 Add User")
    async def adduser_modal(self, ctx: SlashContext):
        balance = Modal(
            ShortText(
                label="📧 Email",
                custom_id="email",
                required=True,
                min_length=6,
                max_length=64,
                placeholder="example@example.com",
            ),
            ShortText(
                label="🖊️ Name",
                custom_id="name",
                min_length=3,
                required=True,
                placeholder="Name",
            ),
            ShortText(
                label="✏️ Username",
                custom_id="username",
                min_length=2,
                required=True,
                placeholder="Username",
            ),
            ShortText(
                label="🔐 Password",
                custom_id="password",
                required=True,
                min_length=8,
                max_length=128,
                placeholder="1234567890",
            ),
            title="🙆 Add User",
            custom_id="add-user",
        )
        await ctx.send_modal(modal=balance)

    @modal_callback("add-user")
    async def on_modal_answer(
        self, ctx: ModalContext,
        email: str,
        name: str,
        username: str,
        password: str
        ):
        command = f'npm run add-user "{email}" "{name}" "{username}" "{password}"'
        await ctx.send(f"{command}", ephemeral=True)
        await run_shell_command(ctx, command)
