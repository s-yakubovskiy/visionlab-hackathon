#!/usr/bin/python

import logging
import requests
import re
import shutil
from pprint import pprint
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType


WELCOME_MESSAGE = 'Welcome to Machine Can See *_*!\nSend a selfie to begin'
KEYS = ""


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
