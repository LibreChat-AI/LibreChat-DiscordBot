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
            ShortText(
                label="⌛ Duration in minutes",
                custom_id="minutes",
                required=False,
                placeholder="0",
            ),
            ShortText(
                label="⌛ Duration in hours",
                custom_id="hours",
                required=False,
                placeholder="0",
            ),
            ShortText(
                label="⌛ Duration in days",
                custom_id="days",
                required=False,
                placeholder="0",
            ),
            title="🔨 Ban User",
            custom_id="ban",
        )
        await ctx.send_modal(modal=balance)


    @modal_callback("ban")
    async def on_modal_answer(
        self,
        ctx: ModalContext,
        email: str,
        minutes: str,
        hours: str,
        days: str
        ):

        minutes = int(minutes) * 60000 if minutes else 0 # Convert to milliseconds
        hours = int(hours) * 3600000  if hours else 0 # Convert to milliseconds
        days = int(days) * 86400000  if days else 0 # Convert to milliseconds

        total_duration_in_ms = minutes + hours + days  # Add all durations together

        command = f"npm run ban-user {email} {total_duration_in_ms}"

        await ctx.send(f"{command}", ephemeral=True)
        await run_shell_command(ctx, command)
