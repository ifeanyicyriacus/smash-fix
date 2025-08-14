from abc import ABC, abstractmethod
from typing import Dict, Any


class LogisticsProviderInterface(ABC):
    @abstractmethod
    def get_courier_id(self):
        pass

    @abstractmethod
    def get_tracking_url(self, waybill_number: str):
        pass

    @abstractmethod
    def calculate_delivery_fee(self, origin: str, destination: str,
                               weight: float, pickup_type: str = "1") -> Dict[str, Any]:
        """Calculate delivery fee for a shipment."""
        pass

    @abstractmethod#assign_courier
    def create_pickup_request(self, order_details: Dict[str, Any]) -> Dict[str, Any]:
        """Submit a pickup request and generate waybill number."""
        pass

    @abstractmethod
    def initiate_payment(self, waybill_number: str, callback_url: str) -> Dict[str, Any]:
        """Initiate payment through Paystack for a waybill."""
        pass

    @abstractmethod
    def get_pickup_request_status(self, waybill_number: str) -> list[dict[str, str]]:
        """Get status of a pickup request."""
        pass
