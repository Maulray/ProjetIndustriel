# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


from flask import Config

from botbuilder.ai.qna import QnAMaker, QnAMakerEndpoint
from botbuilder.ai.luis import LuisApplication
from botbuilder.core import ActivityHandler, TurnContext, MessageFactory
from botbuilder.schema import ChannelAccount


import json, requests

import windowsresearch
import sharepointResearch



class MyBot(ActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.

    def __init__(self, config: Config):
        self.qna_maker = QnAMaker(
            QnAMakerEndpoint(
                knowledge_base_id=config.QNA_KNOWLEDGEBASE_ID,
                endpoint_key=config.QNA_ENDPOINT_KEY,
                host=config.QNA_ENDPOINT_HOST,
            )
        )

        self.luis_app = LuisApplication(
            application_id = config.LUIS_APP_ID,
            endpoint =  "https://" + config.LUIS_API_HOST_NAME,
            endpoint_key = config.LUIS_API_KEY,
        )




    async def on_message_activity(self, turn_context: TurnContext):

        #Recherche de la question dans la base de connaissances du QnA
        responseQNA = await self.qna_maker.get_answers(turn_context)

        #Récupération de la prédiction de l'intention via Luis, par exemple :

        #{'query': 'où est config?', 'prediction': {'topIntent': 'FileSearching', 'intents': {'FileSearching': {'score': 0.511657357}, 'None': {'score': 0.03619536}, 'Helper': {'score': 0.0359005369}, 'Greeting': {'score': 0.0114977509}, 'Thanks': {'score': 0.01004542}},
        #'entities': {'File': [{'name': ['config'], '$instance': {'name': [{'type': 'name', 'text': 'config', 'startIndex': 7, 'length': 6, 'score': 0.864029646, 'modelTypeId': 1, 'modelType': 'Entity Extractor', 'recognitionSources': ['model']}]}}],
        #'$instance': {'File': [{'type': 'File', 'text': 'config', 'startIndex': 7, 'length': 6, 'score': 0.865803838, 'modelTypeId': 1, 'modelType': 'Entity Extractor', 'recognitionSources': ['model']}]}}}}
        headers = {}
        params ={
            'query' : turn_context.activity.text,
            'timezoneOffset' : '0',
            'verbose' : 'true',
            'show-all-intents': 'true',
            'spellCheck': 'false',
            'staging': 'false',
            'subscription-key': self.luis_app.endpoint_key
        }
        prediction = requests.get(self.luis_app.endpoint+'luis/prediction/v3.0/apps/'+self.luis_app.application_id+'/slots/production/predict',headers = headers, params = params)

        #Isolation de l'intention correspondant le mieux à l'input de l'utilisateur
        topintent = prediction.json().get('prediction').get('topIntent')


        #Ce bloc permet que le QnA ne prenne pas la priorité sur le Luis dans le cas d'une recherche de fichier avec un nom recconu dans une des questions de la base de connaissance
        filesearch = True
        try :
            predic = prediction.json().get('prediction').get("entities").get('File')[0]
        except TypeError :
            filesearch = False

        if responseQNA and len(responseQNA) > 0 and responseQNA[0].score > 0.9 and filesearch==False:
            await turn_context.send_activity(MessageFactory.text(responseQNA[0].answer))

        elif responseQNA and len(responseQNA) > 0 and responseQNA[0].score > 0.6 and responseQNA[0].score <= 0.9 and filesearch==False:
            await turn_context.send_activity("Je n'ai pas réussi à comprendre avec certitude votre question, mais voici la question relative à ce sujet la plus proche à laquelle je peux répondre :")
            await turn_context.send_activity(MessageFactory.text(responseQNA[0].questions[0]))
            await turn_context.send_activity(MessageFactory.text("Et voici sa réponse :"))
            await turn_context.send_activity(MessageFactory.text(responseQNA[0].answer))

        else:

            if topintent=="FileSearching":

                #Récupération du nom du fichier à rechercher
                if filesearch == True :
                    predic = prediction.json().get('prediction').get("entities").get('File')[0]
                    file="" #Dans cette variable on ne mettra que le nom effectif du fichier, par exemple "file.txt"
                    filepath="" #Dans cette variable on mettra tout le chemin potentiellement entré par l'utilisateur, par exemple "./test/file.txt"

                    if 'name' in predic:
                        file = predic.get('name')[0]
                        filepath = file
                        path = file.split('/')
                        if len(path)!=1:
                            file = path[len(path)-1]
                    if 'extension' in predic:
                         file+="."+predic.get('extension')[0]
                         filepath+="."+predic.get('extension')[0]

                    await turn_context.send_activity(f"Recherche de '"+filepath+"' dans les fichiers Windows en cours")
                    filepath=f'.\\'+filepath

                    #Recherche dans les fichiers Windows
                    windowsresearch.rechercheFichiersLocaux(file, ".")


                    if len(windowsresearch.paths)==0:
                        await turn_context.send_activity(f"Aucun fichier correspondant à cette demande n'a été trouvé.")

                    elif len(windowsresearch.paths)==1:
                        await turn_context.send_activity(f"Le fichier a été trouvé à l'endroit suivant : " + windowsresearch.paths[0])
                        #os.startfile(self.paths[0]) #fonctionne uniquement en local

                    elif filepath in windowsresearch.paths:
                        await turn_context.send_activity(f"Le fichier a été trouvé à l'endroit suivant : " + filepath)
                        #os.startfile(filepath) #fonctionne uniquement en local

                    else:
                        await turn_context.send_activity(f"Différents fichiers correspondants ont été trouvés aux endroits suivants :")

                        for p in windowsresearch.paths :
                            await turn_context.send_activity(p)
                        await turn_context.send_activity(str(len(windowsresearch.paths)) + " résultats correspondants ont été trouvés. Vous pouvez toujours tenter une recherche plus précise pour le trouver plus facilement !") #Pour ouvrir votre document, trouvez son nom précis dans la liste ci-dessus, copiez-le et demandez-moi 'Ouvre [nomdufichier]'

                    windowsresearch.paths[:]=[] #on vide la liste des chemins trouvés pour la prochaine utilisation


                    # #Recherche dans les fichiers Sharepoint
                    # try :
                    #     await turn_context.send_activity(f"Recherche de '"+filepath[2:]+"' dans les fichiers Sharepoint en cours")
                    #     sharepointResearch.recherchesharepoint(file,False)
                    #     await turn_context.send_activity(str(len(sharepointResearch.list)) +" fichiers correspondants ont été trouvés aux endroits suivants :")
                    #     for p in sharepointResearch.list :
                    #         await turn_context.send_activity(p)
                    # except ValueError:
                    #     await turn_context.send_activity("L'authentification à double-facteur est activée pour ce compte. Veuillez le désactiver pour pouvoir utiliser le service de recherche dans les fichiers Sharepoint")
                    #
                    # sharepointResearch.list[:]=[] #on vide la liste des chemins trouvés pour la prochaine utilisation
                    #
                    #
                    # #Recherche dans les fichiers Teams
                    # try :
                    #     await turn_context.send_activity(f"Recherche de '"+filepath[2:]+"' dans les fichiers Teams en cours")
                    #     sharepointResearch.recherchesharepoint(file,True)
                    #     await turn_context.send_activity(str(len(sharepointResearch.list)) +" fichiers correspondants ont été trouvés aux endroits suivants :")
                    #     for p in sharepointResearch.list :
                    #         await turn_context.send_activity(p)
                    # except ValueError:
                    #     await turn_context.send_activity("L'authentification à double-facteur est activée pour ce compte. Veuillez le désactiver pour pouvoir utiliser le service de recherche dans les fichiers Teams")
                    #
                    # sharepointResearch.list[:]=[] #on vide la liste des chemins trouvés pour la prochaine utilisation

                else :
                    await turn_context.send_activity(f"Il semblerait que j'ai mal compris votre demande ou que je ne sois pas programmé pour y répondre... N'hésitez pas à me solliciter à nouveau !")
                    await turn_context.send_activity(f"Si vous pensez que je ne peux pas répondre à votre demande, je vous invite à contacter mes collègues humains pour résoudre votre problème :-). Cliquez sur l'icône GLPI sur votre bureau pour créer un ticket de demande d'assistance !")

            elif topintent=="Greeting":
                await turn_context.send_activity(f"Bonjour ! J'espère pouvoir vous être utile aujourd'hui :-)")

            elif topintent=="Helper":
                await turn_context.send_activity(f"Vous pouvez me demander de vous rechercher un fichier en tapant par exemple 'Où est file.txt?'.")
                await turn_context.send_activity(f"Je sais également répondre à quelques questions qui pourraient vous aider au quotidien : valider une demande GLPI, approuver une demande d'achat, qui contacter en cas de problème de sécurité informatique,etc... ")
                await turn_context.send_activity(f"Posez-moi une question ! Si je n'ai pas la réponse, je vous renverrai vers mes collègues humains :-)")

            elif topintent=="Thanks":
                await turn_context.send_activity(f"A votre service ! :-)")

            elif topintent=="None":
                await turn_context.send_activity(f"Il semblerait que j'ai mal compris votre demande ou que je ne sois pas programmé pour y répondre... N'hésitez pas à me solliciter à nouveau !")
                await turn_context.send_activity(f"Si vous pensez que je ne peux pas répondre à votre demande, je vous invite à contacter mes collègues humains pour résoudre votre problème :-). Cliquez sur l'icône GLPI sur votre bureau pour créer un ticket de demande d'assistance !")



    async def on_members_added_activity(
            self,
            members_added: ChannelAccount,
            turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Bienvenue ! Vous entrez en conversation avec un chatbot permettant de trouver des fichiers et de répondre à quelques questions simples vous permettant de vous faciliter votre travail ! :-).")
