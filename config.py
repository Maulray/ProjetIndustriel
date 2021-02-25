#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")


    LUIS_APP_ID = os.environ.get("LuisAppId", "<Luis app ID>")
    LUIS_API_KEY = os.environ.get("LuisAPIKey", "<Luis API key>")
    # LUIS endpoint host name, ie "westus.api.cognitive.microsoft.com"
    LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName", "westus.api.cognitive.microsoft.com/")


    QNA_KNOWLEDGEBASE_ID = os.environ.get("QnAKnowledgebaseId", "<QnA app ID>"")
    QNA_ENDPOINT_KEY = os.environ.get("QnAEndpointKey", "<QnA endpoint key>")
    QNA_ENDPOINT_HOST = os.environ.get("QnAEndpointHostName", "https://qnamakerfigeac2k20.azurewebsites.net/qnamaker")


    SHAREPOINT_USERNAME = os.environ.get("SharapointId","<e-mail du compte de service qui sera utilisé>")
    SHAREPOINT_PASSWORD = os.environ.get("SharepointPassword","<mot de passe du compte de service qui sera utilisé>")
    SHAREPOINT_SERVER_URL = os.environ.get("SharepointServerUrl","https://fga01.sharepoint.com/sites/DSI-FigeacAero-ProjetChatBotavecTelecomNancy/Documents%20partages/Forms/AllItems.aspx")


    TEAMS_SP_URL = os.environ.get("TeamsSharepointUrl","https://fga01.sharepoint.com/sites/DSI-FigeacAero-ProjetChatBotavecTelecomNancy/Documents%20partages/Forms/AllItems.aspx?RootFolder=%2Fsites%2FDSI%2DFigeacAero%2DProjetChatBotavecTelecomNancy%2FDocuments%20partages%2FGeneral&FolderCTID=0x012000F4568026C0FA01449C6DFF3D3934F38B")
