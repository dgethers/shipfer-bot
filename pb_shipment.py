import requests
import datetime
import base64


class PitneyBowesShipmentProcessor:
    shipment_url = 'https://api-sandbox.sendpro360.pitneybowes.com/shipping/api/v1/shipments'
    token_url = "https://api-sandbox.sendpro360.pitneybowes.com/auth/api/v1/token"

    # todo: extract token to central point when more processors are created
    def __init__(self, client_id: str, client_secret: str):
        self.auth_token = None
        self.client_id = client_id
        self.client_secret = client_secret

    # todo: use parameters / split into seperate methods for ease
    def get_shipments(self, start_date: datetime = None, end_date: datetime = None, page: int = None, size: int = None):
        if start_date and end_date and size:
            return "my filtered shipments"
        access_token = self.get_access_token()

        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        response = requests.get(self.shipment_url, headers=headers)
        return response.json().get('data')

    # todo: expire token after 4 hours. possible caching with TTL
    def get_access_token(self):
        if not self.auth_token:
            auth_string = f"{self.client_id}:{self.client_secret}"
            encoded_auth = base64.b64encode(auth_string.encode())

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Basic {encoded_auth.decode()}"
            }

            response = requests.post(self.token_url, headers=headers, auth=(self.client_id, self.client_secret))
            self.auth_token = response.json().get('access_token')
            return self.auth_token
        else:
            return self.auth_token
