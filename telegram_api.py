from telethon import TelegramClient
from telethon.tl.functions.channels import (
    JoinChannelRequest,
    LeaveChannelRequest
)
from telethon.errors.rpcerrorlist import FloodWaitError

from credentials import (
    get_channels, get_id, get_hash, get_phone, get_password
)
from popup_windows import show_ok, show_error, enter_code
from constants import SESSION_FILE_PATH


async def main(client, channels, follow):
    for channel in channels:
        if follow is True:
            try:
                await client(JoinChannelRequest(channel))
                show_ok()
            except FloodWaitError:
                show_error()
        else:
            await client(LeaveChannelRequest(channel))
            show_ok()


def follow_channels(follow=True):
    client = TelegramClient(str(SESSION_FILE_PATH), get_id(), get_hash())
    client.start(get_phone, get_password, code_callback=enter_code())
    client.loop.run_until_complete(main(client, get_channels(), follow))
