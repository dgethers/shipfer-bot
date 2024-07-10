from datetime import datetime
from enum import Enum, StrEnum


class Entities(StrEnum):
    START_DATE = 'StartDate'
    END_DATE = 'EndDate'


class Intents(StrEnum):
    CREATE_SHIPMENTS = 'CreateShipments',
    SEARCH_ALL_SHIPMENTS = 'ViewAllShipments',
    SEARCH_SHIPMENTS = 'SearchShipments',
    SHIPMENT_INFO = 'ShipmentInfo'
