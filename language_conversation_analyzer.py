# import libraries
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.conversations import ConversationAnalysisClient
from dotenv import load_dotenv


# get secrets
# todo: get secrets from config file
# clu_endpoint = os.environ["LS_CONVERSATIONS_ENDPOINT"]
# clu_key = os.environ["LS_CONVERSATIONS_KEY"]


# project_name = os.environ["AZURE_CONVERSATIONS_PROJECT_NAME"]
# deployment_name = os.environ["AZURE_CONVERSATIONS_DEPLOYMENT_NAME"]

class LanguageConversationAnalyzer:
    def __init__(self, language_service_endpoint: str, language_service_key: str):
        print(f'langeuage_service_endpoint -> {language_service_endpoint}')
        print(f'language_service_key -> {language_service_key}')
        self.languageServiceClient = ConversationAnalysisClient(language_service_endpoint, AzureKeyCredential(language_service_key))

    # todo: create enum for intent types
    def get_intent(self, text: str) -> str:
        with self.languageServiceClient:
            result = self.languageServiceClient.analyze_conversation(
                task={
                    "kind": "Conversation",
                    "analysisInput": {
                        "conversationItem": {
                            "participantId": "1",
                            "id": "1",
                            "modality": "text",
                            "language": "en",
                            "text": text
                        },
                        "isLoggingEnabled": False
                    },
                    "parameters": {
                        "projectName": "Shipfer-bot-language",
                        "deploymentName": "v0.6",
                        "verbose": True
                    }
                }
            )

        print("query: {}".format(result["result"]["query"]))
        # print("project kind: {}\n".format(result["result"]["prediction"]["projectKind"]))

        print("top intent: {}".format(result["result"]["prediction"]["topIntent"]))
        # print("category: {}".format(result["result"]["prediction"]["intents"][0]["category"]))
        print("confidence score: {}\n".format(result["result"]["prediction"]["intents"][0]["confidenceScore"]))

        return result["result"]["prediction"]["topIntent"]

        # print("entities:")
        # for entity in result["result"]["prediction"]["entities"]:
        #     print("\ncategory: {}".format(entity["category"]))
        #     print("text: {}".format(entity["text"]))
        #     print("confidence score: {}".format(entity["confidenceScore"]))
        #     if "resolutions" in entity:
        #         print("resolutions")
        #         for resolution in entity["resolutions"]:
        #             print("kind: {}".format(resolution["resolutionKind"]))
        #             print("value: {}".format(resolution["value"]))
        #     if "extraInformation" in entity:
        #         print("extra info")
        #         for data in entity["extraInformation"]:
        #             print("kind: {}".format(data["extraInformationKind"]))
        #             if data["extraInformationKind"] == "ListKey":
        #                 print("key: {}".format(data["key"]))
        #             if data["extraInformationKind"] == "EntitySubtype":
        #                 print("value: {}".format(data["value"]))