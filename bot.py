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

from data_models import ShipmentQuestions, ShipmentQuestionAnswers, ShipmentConversationalFlow, Intents

import config
from language_conversation_analyzer import LanguageConversationAnalyzer
from pb_shipment import PitneyBowesShipmentProcessor


# todo: rename bot
class MyBot(ActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.

    def __init__(self, user_state: UserState, conversation_state: ConversationState,
                 language_conversation_analyzer: LanguageConversationAnalyzer,
                 shipment_processor: PitneyBowesShipmentProcessor):

        self.question_ask_flow = None
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

    # todo: create larger workflow with multi-turn conversation
    async def on_message_activity(self, turn_context: TurnContext):

        flow = await self.flow_accessor.get(turn_context, ShipmentConversationalFlow)
        user_shipment_questions = await self.user_shipment_question_accessor.get(turn_context, ShipmentQuestionAnswers)

        if not self.question_ask_flow:
            intent = self.language_conversation_analyzer.get_intent(turn_context.activity.text)
            print(f'Intent: {intent}')

            if intent == Intents.SEARCH_ALL_SHIPMENTS:
                shipments = self.shipment_processor.get_shipments()
                print(f'shipments -> {shipments}')
                await turn_context.send_activity(str(shipments))
            elif intent == Intents.SEARCH_SHIPMENTS:
                self.question_ask_flow = True
                await self._ask_shipment_questions(flow, user_shipment_questions, turn_context)
                print(f'user_shipment_questions -> {str(user_shipment_questions)}')
        else:
            await self._ask_shipment_questions(flow, user_shipment_questions, turn_context)

        await self.conversation_state.save_changes(turn_context)
        await self.user_state.save_changes(turn_context)

    # todo: add types
    async def _ask_shipment_questions(self, flow: ShipmentConversationalFlow, shipment_question_answers: ShipmentQuestionAnswers, turn_context: TurnContext):
        # asking questions

        user_input = turn_context.activity.text.strip()

        if flow.last_question_asked == ShipmentQuestions.NONE:
            await turn_context.send_activity(MessageFactory.text(
                "What is start date (format YYYY-MM-DD) do you want to search for?"))
            flow.last_question_asked = ShipmentQuestions.START_DATE
            self.question_ask_flow = True

        elif flow.last_question_asked == ShipmentQuestions.START_DATE:
            shipment_question_answers.start_date = user_input
            await turn_context.send_activity(MessageFactory.text(
                "What is the end date (format YYYY-MM-DD do you want to search for"))
            flow.last_question_asked = ShipmentQuestions.END_DATE

        elif flow.last_question_asked == ShipmentQuestions.END_DATE:
            shipment_question_answers.end_date = user_input
            await turn_context.send_activity(MessageFactory.text("How many results do you want?"))
            flow.last_question_asked = ShipmentQuestions.RESULT_SIZE

        elif flow.last_question_asked == ShipmentQuestions.RESULT_SIZE:
            shipment_question_answers.result_size = int(user_input)
            filtered_shipments = self.shipment_processor.get_shipments(shipment_question_answers.start_date,
                                                                       shipment_question_answers.end_date, None, shipment_question_answers.result_size)
            await turn_context.send_activity(MessageFactory.text(filtered_shipments))
            flow.last_question_asked = ShipmentQuestions.NONE
            self.question_ask_flow = False

        async def on_members_added_activity(
                self,
                members_added: ChannelAccount,
                turn_context: TurnContext
        ):
            for member_added in members_added:
                if member_added.id != turn_context.activity.recipient.id:
                    await turn_context.send_activity("Hello and welcome!")
