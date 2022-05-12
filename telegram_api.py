from telethon import TelegramClient
from telethon.tl.functions.channels import (
    JoinChannelRequest,
    LeaveChannelRequest
)
from telethon.errors.rpcerrorlist import FloodWaitError
from telethon.errors import SessionPasswordNeededError

from credentials import (
    get_channels, get_id, get_hash, get_phone
)
from popup_windows import (
    show_ok, show_error, enter_code, enter_password
)
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


async def follow_channels(follow=True):
    client = TelegramClient(str(SESSION_FILE_PATH), get_id(), get_hash())
    await client.connect()
    authorized = await client.is_user_authorized()
    if not authorized:
        await client.sign_in(get_phone())
        try:
            await client.sign_in(code=input('Enter code: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=input('Enter password: '))
    #client.start(get_phone, get_password, code_callback=enter_code)
    #client.loop.run_until_complete(main(client, get_channels(), follow))
