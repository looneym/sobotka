import os 
import datetime

import pytz

from aws import KeyPairManager


def has_sudo():
    if os.getuid() == 0:
        return True
    else:
        print("This operation requires elevated privelages, please try again with sudo")
        exit(126)   


def utcnow():
    # An ISO 8601 string represention of the current time _including_ timezone (UTC)
    return datetime.datetime.now(tz=pytz.utc).isoformat()        

def create_key_pair(overwrite):
    kpm = KeyPairManager()
    kpm.create_key_pair(overwrite)    