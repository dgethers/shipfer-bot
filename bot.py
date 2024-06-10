# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount

from botbuilder.core import (
    ActivityHandler,
    ConversationState,
    TurnContext,
    UserState,
    MessageFactory,
)

from data_models import ShipmentQuestions, ShipmentQuestionAnswers

import config
from language_conversation_analyzer import LanguageConversationAnalyzer
from pb_shipment import PitneyBowesShipmentProcessor

# todo: rename bot
class MyBot(ActivityHandler):
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


    # todo: create larger workflow with multi-turn conversation
    async def on_message_activity(self, turn_context: TurnContext):
        intent = self.language_conversation_analyzer.get_intent(turn_context.activity.text)
        print(f'Intent: {intent}')
        shipments = None

        if intent == 'ListShipments':
            shipments = self.shipment_processor.get_shipments()
        print(f'shipments -> {shipments}')

        await turn_context.send_activity(str(shipments))

    async def on_members_added_activity(
            self,
            members_added: ChannelAccount,
            turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")
