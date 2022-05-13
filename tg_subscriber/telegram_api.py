from telethon import TelegramClient
from telethon.tl.functions.channels import (
    JoinChannelRequest,
    LeaveChannelRequest
)
from telethon.errors.rpcerrorlist import FloodWaitError
from telethon.errors import SessionPasswordNeededError

from tg_subscriber.credentials import (
    get_channels, get_id, get_hash, get_phone
)
from tg_subscriber.popup_windows import (
    show_ok, show_error, enter_code, enter_password, enter_window
)
from tg_subscriber.constants import SESSION_FILE_PATH


async def main(client, channels, follow):
    print('channels', channels)
    for channel in channels:
        if follow is True:
            try:
                await client(JoinChannelRequest(channel))
                show_ok()
            except FloodWaitError:
                show_error()
        else:
            result = await client(LeaveChannelRequest(channel))
            print('relust', result)
            show_ok()


async def follow_channels(follow=True):
    client = TelegramClient(str(SESSION_FILE_PATH), get_id(), get_hash())
    await client.connect()
    if not await client.is_user_authorized():
        print('1111')
        await client.send_code_request(get_phone())
        print('2222')
        #window = enter_window()
        me = await client.sign_in(get_phone(), await enter_code())
        print('3333')
    print('authorized')
    """
    await client.connect()
    authorized = await client.is_user_authorized()
    print('a', authorized)
    if not authorized:
        print('not authorized')
        await client.sign_in(get_phone())
        print('got phone')
        try:
            code = await enter_code()
            print(code)
            await client.sign_in(code=code)
            print('code accepted')
        except SessionPasswordNeededError:
            await client.sign_in(password=enter_password())
    print('authorized')
    """
    await main(client, get_channels(), follow)
    print('final_print')
