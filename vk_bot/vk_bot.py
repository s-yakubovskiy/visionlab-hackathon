#!/usr/bin/python

import logging
import requests
import re
import shutil
from pprint import pprint
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType


WELCOME_MESSAGE = 'Welcome to Machine Can See *_*!\nSend a selfie to begin'
KEYS = "95e00fddd8887f27bce737d4b90630b641d9c25b67f457ff0da194f8dd2df017d79af8d677ff0f33ffe11"


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)