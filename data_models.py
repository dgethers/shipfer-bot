from datetime import datetime
from enum import Enum, StrEnum


class ShipmentQuestions(Enum):
    START_DATE = 1
    END_DATE = 2
    RESULT_SIZE = 3
    NONE = 4


class Intents(StrEnum):
    CREATE_SHIPMENTS = 'CreateShipments',
    SEARCH_ALL_SHIPMENTS = 'SearchAllShipments',
    SEARCH_SHIPMENTS = 'SearchShipments',
    SHIPMENT_INFO = 'ShipmentInfo',


class ShipmentConversationalFlow:
    def __init__(self, last_question_asked: ShipmentQuestions = ShipmentQuestions.NONE):
        self.last_question_asked = last_question_asked


class ShipmentQuestionAnswers:
    def __init__(self, start_date: datetime = None, end_date: datetime = None, result_size: int = 0):
        self.start_date = start_date
        self.end_date = end_date
        self.result_size = result_size

    def __str__(self):
        return f'Start Date: {self.start_date}, End Date: {self.end_date}, Result Size: {self.result_size}'
