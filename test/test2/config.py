#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")
    LUIS_APP_ID = os.environ.get("LuisAppId", "bad8ebd4-728f-4093-bacc-c6a272b98679")
LUIS_API_KEY = os.environ.get("LuisAPIKey", "6d399ced56fd4afdb137fcb6fe3651a9")
# LUIS endpoint host name, ie "westus.api.cognitive.microsoft.com"
LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName", "westeurope.api.cognitive.microsoft.com")
