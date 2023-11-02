# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=import-error

# 🔨 BAN USER

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

class Balance(Extension):
    @slash_command(name="ban", description="🔨 Ban User")
    async def balance_modal(self, ctx: SlashContext):
        balance = Modal(
            ShortText(
                label="📧 User's email",
                custom_id="email",
                required=True,
                min_length=6,
                max_length=64,
                placeholder="example@example.com",
            ),
            title="🔨 Ban User",
            custom_id="ban",
        )
        await ctx.send_modal(modal=balance)

    @modal_callback("ban")
    async def on_modal_answer(self, ctx: ModalContext, email: str):
        command = f"npm run ban-user {email}"
        await ctx.send(f"{command}", ephemeral=True)
        await run_shell_command(ctx, command)
