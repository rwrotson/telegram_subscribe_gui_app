from constants import USER_FILE_PATH, CHANNEL_FILE_PATH


def get_credentials():
    with open(USER_FILE_PATH, 'r') as f:
        api_id, api_hash, phone = f.read().split(', ')
    return api_id, api_hash, phone


def get_id():
    return get_credentials()[0]


def get_hash():
    return get_credentials()[1]


def get_phone():
    return get_credentials()[2]


def get_channels():
    with open(CHANNEL_FILE_PATH, 'r') as f:
        channels = f.read().split(', ')
    return channels
