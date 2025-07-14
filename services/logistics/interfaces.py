from abc import ABC, abstractmethod
from typing import Dict, Any


class LogisticsInterface(ABC):

    @abstractmethod
    def _authenticate(self) -> None:
        """Authenticate with the Click N Ship API and store the access token."""
        pass

    @abstractmethod
    def _get_headers(self) -> Dict[str, str]:
        """Get headers with authentication token."""
        pass

    @abstractmethod
    def calculate_delivery_fee(self, origin: str, destination: str,
                               weight: float, pickup_type: str = "1") -> Dict[str, Any]:
        """Calculate delivery fee for a shipment."""
        pass

    @abstractmethod
    def create_pickup_request(self, order_details: Dict[str, Any]) -> Dict[str, Any]:
        """Submit a pickup request and generate waybill number."""
        pass

    @abstractmethod
    def initiate_payment(self, waybill_number: str, callback_url: str) -> Dict[str, Any]:
        """Initiate payment through Paystack for a waybill."""
        pass
