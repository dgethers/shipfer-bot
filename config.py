#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

from dotenv import load_dotenv


class DefaultConfig:
    """ Bot Configuration """

    load_dotenv()

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")
    LS_CONVERSATIONS_ENDPOINT = os.environ.get("LS_CONVERSATIONS_ENDPOINT", "")
    LS_CONVERSATIONS_KEY = os.environ.get("LS_CONVERSATIONS_KEY", "")
    LS_REGION = os.environ.get("LS_REGION", "")
    PB_CLIENT_ID = os.environ.get("PB_CLIENT_ID", "")
    PB_CLIENT_SECRET = os.environ.get("PB_CLIENT_SECRET", "")


