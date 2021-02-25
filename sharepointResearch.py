'''Cette fonctionnalité n'a pas pu être testée faute d'accès à un sharepoint sans double-authentification, mais voici une base qui devrait donner un resultat satisfaisant'''

from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext
from config import DefaultConfig

import re

config = DefaultConfig()

url_sharepoint=config.SHAREPOINT_SERVER_URL
url_teams=config.TEAMS_SP_URL
username=config.SHAREPOINT_USERNAME
password=config.SHAREPOINT_PASSWORD

list=[]

def recherchesharepoint(fichier,teams):

    if teams : #recherche dans les fichiers Teams
        url = url_teams
    else : #recherche dans le serveur Sharepoint
        url = url_sharepoint

    #accès au sharepoint
    user_credentials = UserCredential(username,password)
    ctx = ClientContext(url).with_credentials(user_credentials)

    lists = ctx.web.lists
    lists_name = lists.get_by_title(lists)
    items = lists_name.get_items()
    ctx.load(items)
    ctx.execute_query()

    for item in items:
        if re.search(fichier.lower(),item.properties['Title'].lower()):
            list.append(item)
