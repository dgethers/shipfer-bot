# import libraries
import os
from typing import Dict

from azure.core.credentials import AzureKeyCredential
from azure.ai.language.conversations import ConversationAnalysisClient
import logging

logging.basicConfig(level=logging.DEBUG)


class LanguageConversationAnalyzer:
    def __init__(self, language_service_endpoint: str, language_service_key: str):
        self.languageServiceClient = ConversationAnalysisClient(language_service_endpoint,
                                                                AzureKeyCredential(language_service_key))
        self.logger = logging.getLogger(__name__)

    # todo: create env property for deploymentName, and projectName
    # todo: set threshold for confidence
    # todo: rename function
    def get_intent(self, text: str) -> (str, dict[str: str]):
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
                        "projectName": "shipfer-language-cognition",
                        "deploymentName": "v.03",
                        "verbose": True
                    }
                }
            )

        self.logger.debug(f'top intent: {result["result"]["prediction"]["topIntent"]}')
        self.logger.debug(f'confidence score of the top intent: '
                          f'{result["result"]["prediction"]["intents"][0]["confidenceScore"]}')

        entities = self._get_entities(result)
        top_intent = self._get_top_intent(result)

        return top_intent, entities

    # todo: provide type for result
    @staticmethod
    def _get_entities(analysis_result) -> Dict[str, str]:
        entities = {}

        for entity in analysis_result["result"]["prediction"]["entities"]:
            category = entity["category"]
            text = ''
            resolution = entity["resolutions"][0]

            if resolution["resolutionKind"] == 'TemporalSpanResolution':
                text = resolution["timex"]

            entities[category] = text

        return entities

    @staticmethod
    def _get_top_intent(result) -> str:
        return result["result"]["prediction"]["topIntent"]
