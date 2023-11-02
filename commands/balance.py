# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=import-error

# 💸 ADD BALANCE

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
    @slash_command(
            name="balance",
            description="💸 Add credit to user’s balance"
            )
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
                label="💰 Credit quantity - 1000 credits = $0.001",
                custom_id="credit_amount",
                required=True,
                min_length=4,
                max_length=12,
                placeholder="Enter a number between 1000 and 999999999999",
            ),
            title="💸 Set Balance",
            custom_id="balance",
        )
        await ctx.send_modal(modal=balance)

    @modal_callback("balance")
    async def on_modal_answer(self, ctx: ModalContext, email: str, credit_amount: str):
        command = f"npm run add-balance {email} {credit_amount}"
        await ctx.send(f"{command}", ephemeral=True)
        await run_shell_command(ctx, command)
