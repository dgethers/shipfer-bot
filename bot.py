# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.schema import ChannelAccount, TextFormatTypes
from activity_formatters import ShipmentFormatter
import logging

from botbuilder.core import (
    ActivityHandler,
    TurnContext,
    MessageFactory,
)

from data_models import Intents, Entities

from fake_shipment_processor import ShipmentProcessor
from shipping_converation_recognizer import ShippingRecognizer

logging.basicConfig(level=logging.DEBUG)


class ShipmentInfoBot(ActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.

    def __init__(self, language_conversation_analyzer: ShippingRecognizer, shipment_processor: ShipmentProcessor):

        self.language_conversation_analyzer = language_conversation_analyzer
        self.shipment_processor = shipment_processor

        self.logger = logging.getLogger(__name__)

    async def on_message_activity(self, turn_context: TurnContext):

        intent, entities = self.language_conversation_analyzer.get_intent_and_entities(turn_context.activity.text)
        self.logger.debug(f'Intent: {intent}')

        if intent == Intents.SEARCH_ALL_SHIPMENTS:
            shipments = self.shipment_processor.get_shipments()
            self.logger.debug(f'returned shipments: {shipments}')
            self.logger.debug(f'entities: {entities}')
            text = MessageFactory.text(ShipmentFormatter.format_shipments_to_markdown(shipments))
            text.text_format = TextFormatTypes.markdown
            await turn_context.send_activity(text)
        elif intent == Intents.SEARCH_SHIPMENTS:
            self.logger.debug(f'entities: {entities}')
            shipments = self.shipment_processor.get_shipments(entities[Entities.START_DATE],
                                                              entities[Entities.END_DATE])
            filter_text = MessageFactory.text(ShipmentFormatter.format_shipments_to_markdown(shipments))
            filter_text.text_format = TextFormatTypes.markdown
            await turn_context.send_activity(filter_text)

    async def on_members_added_activity(
            self,
            members_added: ChannelAccount,
            turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")
