# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=line-too-long
# pylint: disable=anomalous-backslash-in-string
# pylint: disable=broad-exception-caught
# pylint: disable=import-error

import logging
from interactions import(
    Client,
    Intents,
    listen,
)
import bot_config

logging.basicConfig()
cls_log = logging.getLogger('MyLogger')
cls_log.setLevel(logging.INFO)

client = Client(
    intents=Intents.ALL,
    token=bot_config.TOKEN,
    sync_interactions=True,
    asyncio_debug=False,
    logger=cls_log,
    send_command_tracebacks=False
)

# 👂
@listen()
async def on_startup():
    print(f'{client.user} connected to discord')
    print('----------------------------------------------------------------------------------------------------------------')
    print(f'Bot invite link: https://discord.com/api/oauth2/authorize?client_id={bot_config.CLIENT_ID}&permissions=551903348736&scope=bot')
    print('----------------------------------------------------------------------------------------------------------------')

client.load_extensions("commands")
client.start()
