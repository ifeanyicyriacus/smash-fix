from dataclasses import dataclass
from typing import Dict, Optional
import requests
from services.verification.interfaces import KYCProviderInterface


@dataclass
class KYCConfig:
    """Configuration for KYC API."""
    base_url: str
    client_id: str
    client_secret: str


class MockInterfaceImpl(KYCProviderInterface):
    """Mock implementation of KYC provider interface."""

    AUTH_ENDPOINT = "passport/oauth/token"
    NIN_ENDPOINT = "marketplace-routing/api/v1/verify/identity/nin/verify"
    BANK_LIST_ENDPOINT = "marketplace-routing/api/v1/verify/identity/account-number/bank-list"
    BANK_VERIFY_ENDPOINT = "marketplace-routing/api/v1/verify/identity/account-number/resolve"
    ADDRESS_ENDPOINT = "marketplace-routing/api/v1/addresses"

    def __init__(self, config: Optional[KYCConfig] = None):
        self.config = config or KYCConfig(
            base_url="https://api-marketplace-routing.k8.isw.la",
            client_id="mock_client_id",
            client_secret="mock_client_secret"
        )
        self.api_key: Optional[str] = None
        self._authenticate()

    def _authenticate(self) -> None:
        """Authenticate with the KYC service and obtain API key."""
        try:
            payload = 'scope=profile&grant_type=client_credentials'
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f'Basic {self.config.client_id}:{self.config.client_secret}'
            }
            auth_response = requests.post(
                f"{self.config.base_url}/{self.AUTH_ENDPOINT}",
                headers=headers,
                data=payload
            )
            auth_response.raise_for_status()
            self.api_key = auth_response.json().get("access_token")
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to authenticate with KYC service: {e}")

    def _make_request(self, endpoint: str, payload: Dict) -> Dict:
        """Make authenticated request to KYC service.

        Args:
            endpoint: API endpoint to call
            payload: Request payload

        Returns:
            Dict containing API response

        Raises:
            ConnectionError: If request fails
        """
        if not self.api_key:
            raise ValueError("Not authenticated")

        try:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f"Bearer {self.api_key}"
            }
            response = requests.post(
                f"{self.config.base_url}/{endpoint}",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise ConnectionError(f"KYC service request failed: {e}")

    def verify_nin(self, nin: str) -> bool:
        """Verify National Identification Number."""
        response = self._make_request(self.NIN_ENDPOINT, {"id": nin})
        return response.get("is_valid", False)

    def verify_bank_account(self, bank_code: str, bank_account: str) -> bool:
        """Verify bank account details."""
        response = self._make_request(self.BANK_VERIFY_ENDPOINT, {
            "accountNumber": bank_account,
            "bankCode": bank_code
        })
        return response.get("is_valid", False)

    def verify_physical_address(self, physical_address: str) -> bool:
        """Verify physical address."""
        response = self._make_request(self.ADDRESS_ENDPOINT, {
            "customerReference": "adrsdts",
            "street": physical_address,
            "stateName": "Lagos",
            "lgaName": "mushin",
            "landmark": "mushin",
            "city": "mushin",
            "applicant": {
                "firstname": "Kolade",
                "lastname": "Alade",
                "middlename": "toyosi",
                "gender": "FEMALE",
                "dob": "2022-09-14",
                "phone": "+2349012345678"
            }
        })
        return response.get("is_valid", False)

    def get_physical_address_verification_response(self, reference_id: str) -> Dict:
        """Get full physical address verification response.
        
        Args:
            reference_id: Reference ID of the address to verify
            
        Returns:
            Dict containing full address verification response
        """
        try:
            headers = {
                'Authorization': f"Bearer {self.api_key}"
            }
            response = requests.get(
                f"{self.config.base_url}/{self.ADDRESS_ENDPOINT}",
                headers=headers,
                params={"reference": reference_id}
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise ConnectionError(f"Address verification request failed: {e}")
