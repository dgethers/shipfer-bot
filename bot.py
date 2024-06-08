# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount

import config
from language_conversation_analyzer import LanguageConversationAnalyzer
from pb_shipment import PitneyBowesShipmentProcessor


class MyBot(ActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.

    # todo: create larger workflow with multi-turn conversation
    async def on_message_activity(self, turn_context: TurnContext):
        # todo: redo dependency
        lca = LanguageConversationAnalyzer(config.DefaultConfig.LS_CONVERSATIONS_ENDPOINT,
                                           config.DefaultConfig.LS_CONVERSATIONS_KEY)
        pbs = PitneyBowesShipmentProcessor(config.DefaultConfig.PB_CLIENT_ID, config.DefaultConfig.PB_CLIENT_SECRET)
        intent = lca.get_intent(turn_context.activity.text)
        print(f'Intent: {intent}')
        shipments = None

        if intent == 'ListShipments':
            shipments = pbs.get_shipments()
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
