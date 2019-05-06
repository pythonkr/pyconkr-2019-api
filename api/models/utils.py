import hashlib
from functools import partial
from slacker import Slacker
from constance import config


def hash_file(file, block_size=65536):
    hasher = hashlib.md5()
    for buf in iter(partial(file.read, block_size), b''):
        hasher.update(buf)

    return hasher.hexdigest()


def notify_slack(channel, message):
    if not config.SLACK_TOKEN:
        return False
    try:
        slack = Slacker(config.SLACK_TOKEN)
        slack.chat.post_message(channel, text=message)
        # TODO need to logging more
    except:
        return False
    return True
