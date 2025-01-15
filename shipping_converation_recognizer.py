# import libraries
from __future__ import annotations

import logging
import re
from datetime import datetime
from typing import Dict

from azure.ai.language.conversations import ConversationAnalysisClient
from azure.core.credentials import AzureKeyCredential

logging.basicConfig(level=logging.DEBUG)


class ShippingRecognizer:
    def __init__(self, language_service_endpoint: str, language_service_key: str):
        self.languageServiceClient = ConversationAnalysisClient(language_service_endpoint,
                                                                AzureKeyCredential(language_service_key))
        self.logger = logging.getLogger(__name__)

    # todo: create env property for deploymentName, and projectName
    def get_intent_and_entities(self, text: str) -> (str, dict[str: str]):
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
                    "deploymentName": "v.04",
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

    @staticmethod
    def _get_entities(analysis_result) -> Dict[str, str | datetime]:
        entities = {}
        date_format = '%Y-%m-%d'
        date_pattern = r"\b\d{4}-\d{2}-\d{2}\b"

        for entity in analysis_result["result"]["prediction"]["entities"]:
            key = entity["category"]
            value = ''
            entity_type = entity["extraInformation"][0]["value"]
            date_string = entity["text"]

            if entity_type == 'datetime.daterange':
                match = re.search(date_pattern, date_string)

                if match:
                    found = match.group()
                    value = datetime.strptime(found, date_format)
            elif entity_type == 'datetime.date':
                value = datetime.strptime(date_string, date_format)

            entities[key] = value

        return entities

    @staticmethod
    def _get_top_intent(result) -> str | None:
        confidence_score = result["result"]["prediction"]["intents"][0]["confidenceScore"]
        if confidence_score >= .90:
            return result["result"]["prediction"]["topIntent"]
        else:
            return None
