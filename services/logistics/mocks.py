import json
import uuid

import requests
from typing import Dict, Any

from .interfaces import LogisticsProviderInterface


class MockLogisticsProvider(LogisticsProviderInterface):
    def get_courier_id(self):
        return 'MockLogisticsProvider'

    def get_tracking_url(self, waybill_number: str):
        return f'https://MockLogisticsProvider.com/{waybill_number}'

    def calculate_delivery_fee(self, origin: str, destination: str, weight: float, pickup_type: str = "1") -> Dict[
        str, Any]:
        return {
            "DeliveryFee": 8761,
            "VatAmount": 657.075,
            "TotalAmount": 9418.075
        }

    def create_pickup_request(self, order_details: Dict[str, Any]) -> Dict[str, Any]:
        job_id: str = order_details.get("job_id")
        return {
            "TransStatus": "Successful",
            "TransStatusDetails": "Shipment Pickup Request Created Successfully",
            "OrderNo": job_id,
            "WaybillNumber": "SA02364035",
            "DeliveryFee": "3,747.00",
            "VatAmount": "0.00",
            "TotalAmount": "3,747.00"
        }

    def initiate_payment(self, waybill_number: str, callback_url: str) -> Dict[str, Any]:
        return {
            "ResponseCode": "00",
            "ResponseDescription": "Payment Request Successful",
            "CheckoutURL": "https://checkout.paystack.com/eec1yth5n23igsq",
            "PaymentRef": "SA00625667_2020-12-23_151150"
        }

    def get_pickup_request_status(self, waybill_number: str) -> list[dict[str, str]]:
        return [
            {
                "OrderNo": "9993219",
                "WaybillNumber": "SA00000786",
                "StatusCode": "477",
                "StatusDescription": "Pending For Pickup",
                "StatusDate": "2018-08-27T10:14:42.337"
            },
            {
                "OrderNo": "9993219",
                "WaybillNumber": "SA00000786",
                "StatusCode": "06",
                "StatusDescription": "Shipment Picked Up",
                "StatusDate": "2018-08-28T06:18:16.39"
            }
        ]


class ClickNShipLogisticsProvider(LogisticsProviderInterface):
    BASE_URL = "https://api.clicknship.com.ng"
    AUTH_ENDPOINT = "/Token"
    DELIVERY_FEE_ENDPOINT = "/clicknship/Operations/DeliveryFee"
    PICKUP_REQUEST_ENDPOINT = "/clicknship/Operations/PickupRequest"
    PAYMENT_ENDPOINT = "/ClicknShip/NotifyMe/PayWithPayStack"
    TRACK_SHIPMENT_ENDPOINT = "/clicknship/Operations/TrackShipment"

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.access_token = None
        self._authenticate()

    def _authenticate(self) -> None:
        """Authenticate with the Click N Ship API and store the access token."""
        payload = f'username={self.username}&password={self.password}&grant_type=password'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        response = requests.post(f"{self.BASE_URL}{self.AUTH_ENDPOINT}",
                                 headers=headers,
                                 data=payload)
        response.raise_for_status()
        self.access_token = response.json().get('access_token')

    def _get_headers(self) -> Dict[str, str]:
        """Get headers with authentication token."""
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}'
        }

    def get_courier_id(self):
        return 'ClickNShipLogisticsProvider'

    def get_tracking_url(self, waybill_number: str):
        return "coming-soon: our own url (to our page)"

    def calculate_delivery_fee(self, origin: str, destination: str,
                               weight: float, pickup_type: str = "1") -> Dict[str, Any]:
        """Calculate delivery fee for a shipment."""
        payload = json.dumps({
            "Origin": origin,
            "Destination": destination,
            "Weight": str(weight),
            "PickupType": pickup_type
        })

        response = requests.post(f"{self.BASE_URL}{self.DELIVERY_FEE_ENDPOINT}",
                                 headers=self._get_headers(),
                                 data=payload)
        response.raise_for_status()
        return response.json()

    def create_pickup_request(self, order_details: Dict[str, Any]) -> Dict[str, Any]:
        """Submit a pickup request and generate waybill number."""
        response = requests.post(f"{self.BASE_URL}{self.PICKUP_REQUEST_ENDPOINT}",
                                 headers=self._get_headers(),
                                 data=json.dumps(order_details))
        response.raise_for_status()
        return response.json()

    def initiate_payment(self, waybill_number: str, callback_url: str) -> Dict[str, Any]:
        """Initiate payment through Paystack for a waybill."""
        payload = json.dumps({
            "WaybillNumber": waybill_number,
            "CallBackURL": callback_url
        })

        response = requests.post(f"{self.BASE_URL}{self.PAYMENT_ENDPOINT}",
                                 headers=self._get_headers(),
                                 data=payload)
        response.raise_for_status()
        return response.json()

    def get_pickup_request_status(self, waybill_number: str) -> list[dict[str, str]]:
        """Get status of a pickup request."""
        payload = json.dumps({})
        response = requests.get(f"{self.BASE_URL}{self.TRACK_SHIPMENT_ENDPOINT}?waybillno={waybill_number}",
                                headers=self._get_headers(),
                                data=payload)
        response.raise_for_status()
        return response.json()
