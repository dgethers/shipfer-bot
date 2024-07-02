import json
from datetime import datetime
from typing import Protocol


class ShipmentProcessor(Protocol):
    def get_shipments(self, start_date: datetime = None, end_date: datetime = None):
        pass


class FakeShipmentProcessor(ShipmentProcessor):

    def __init__(self, filename: str):
        self.shipments = self._load_shipments_from_file(filename)

    @staticmethod
    def _load_shipments_from_file(filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            return data['shipments']

    def get_shipments(self, start_date: datetime = None, end_date: datetime = None):
        return self.shipments
