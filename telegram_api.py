from telethon import TelegramClient
from telethon.tl.functions.channels import (JoinChannelRequest,
                                            LeaveChannelRequest)
from telethon.errors.rpcerrorlist import FloodWaitError


def get_api_keys():
    print('2')
    with open('~/.telegram_subscribe_app/user.txt', 'r') as f:
        api_id, api_hash = f.read().split(', ')
    print('3')
    client = TelegramClient('anon', api_id, api_hash)
    print('4')
    with open('~/.telegram_subscribe_app/channels.txt', 'r') as f:
        channels = f.read().split(', ')
    print('5')
    return client, channels


async def main(client, channels, follow):
    print('7')
    for channel in channels:
        print('8', channel)
        if follow is True:
            try:
                await client(JoinChannelRequest(channel))
            except FloodWaitError:
                
        else:
            await client(LeaveChannelRequest(channel))


def follow_channels(follow=True):
    print('1')
    client, channels = get_api_keys()
    print('6', client, channels)
    with client:
        client.loop.run_until_complete(main(client, channels, follow))
