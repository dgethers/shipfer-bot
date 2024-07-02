# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount
import logging

from botbuilder.core import (
    ActivityHandler,
    ConversationState,
    TurnContext,
    UserState,
    MessageFactory,
)

from data_models import ShipmentQuestions, ShipmentQuestionAnswers, ShipmentConversationalFlow, Intents

import config
from language_conversation_analyzer import LanguageConversationAnalyzer
from pb_shipment import PitneyBowesShipmentProcessor

logging.basicConfig(level=logging.DEBUG)


class ShipmentInfoBot(ActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.

    def __init__(self, user_state: UserState, conversation_state: ConversationState,
                 language_conversation_analyzer: LanguageConversationAnalyzer,
                 shipment_processor: PitneyBowesShipmentProcessor):

        if conversation_state is None:
            raise TypeError(
                "[CustomPromptBot]: Missing parameter. conversation_state is required but None was given"
            )
        if user_state is None:
            raise TypeError(
                "[CustomPromptBot]: Missing parameter. user_state is required but None was given"
            )

        self.user_state = user_state
        self.conversation_state = conversation_state

        self.language_conversation_analyzer = language_conversation_analyzer
        self.shipment_processor = shipment_processor

        self.flow_accessor = conversation_state.create_property("ConversationFlow")
        self.user_shipment_question_accessor = user_state.create_property('ShipmentQuestionFlow')
        self.logger = logging.getLogger(__name__)

    # todo: create larger workflow with multi-turn conversation
    async def on_message_activity(self, turn_context: TurnContext):

        # flow = await self.flow_accessor.get(turn_context, ShipmentConversationalFlow)
        # user_shipment_questions = await self.user_shipment_question_accessor.get(turn_context, ShipmentQuestionAnswers)

        intent, entities = self.language_conversation_analyzer.get_intent_and_entities(turn_context.activity.text)
        self.logger.debug(f'Intent: {intent}')

        # todo: determine if this is needed
        # await self.conversation_state.save_changes(turn_context)
        # await self.user_state.save_changes(turn_context)

        if intent == Intents.SEARCH_ALL_SHIPMENTS:
            # shipments = self.shipment_processor.get_shipments()
            shipments = []
            self.logger.debug(f'returned shipments: {shipments}')
            self.logger.debug(f'entities: {entities}')
            await turn_context.send_activity(MessageFactory.text(str(shipments)))
        elif intent == Intents.SEARCH_SHIPMENTS:
            # print(f'user_shipment_questions -> {str(user_shipment_questions)}')
            await turn_context.send_activity(MessageFactory.text("filtered shipments"))
            self.logger.debug(f'entities: {entities}')

    async def on_members_added_activity(
            self,
            members_added: ChannelAccount,
            turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")
