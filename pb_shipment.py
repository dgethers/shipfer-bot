from typing import Protocol

import requests
import datetime
import base64
import cachetools.func
import logging

from fake_shipment_processor import ShipmentProcessor

logging.basicConfig(level=logging.DEBUG)


class PitneyBowesShipmentProcessor(ShipmentProcessor):
    shipment_url = 'https://api-sandbox.sendpro360.pitneybowes.com/shipping/api/v1/shipments'
    token_url = "https://api-sandbox.sendpro360.pitneybowes.com/auth/api/v1/token"

    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.logger = logging.getLogger(__name__)

    def get_shipments(self, start_date: datetime = None, end_date: datetime = None):
        access_token = self._get_access_token()
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        response = None
        if start_date and end_date:
            start_date_string = str(start_date.date())
            end_date_string = str(end_date.date())
            self.logger.debug(f'start_date and end_date have the values: '
                              f'start_date -> {start_date_string} and end_date -> {end_date_string}')
            params = {'startDate': start_date_string, 'endDate': end_date_string}
            response = requests.get(self.shipment_url, headers=headers, params=params)
        else:
            response = requests.get(self.shipment_url, headers=headers)

        return response.json().get('data')

    @cachetools.func.ttl_cache(ttl=60 * 60 * 3)
    def _get_access_token(self):
        self.logger.info("Getting fresh access token")
        auth_string = f"{self.client_id}:{self.client_secret}"
        encoded_auth = base64.b64encode(auth_string.encode())

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {encoded_auth.decode()}"
        }

        response = requests.post(self.token_url, headers=headers, auth=(self.client_id, self.client_secret))
        return response.json().get('access_token')
