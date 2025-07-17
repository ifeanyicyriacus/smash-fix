from abc import ABC, abstractmethod


class VerificationProviderInterface(ABC):
    @abstractmethod
    def verify_nin(self, nin: str) -> bool:
        pass

    @abstractmethod
    def verify_bank_account(self, account_number: str, bank_code: str) -> bool:
        pass

    @abstractmethod
    def verify_address(self, address_detail: dict[str,str]) -> str:
        pass

    @abstractmethod
    def get_physical_address_verification_response(self, reference: str) -> bool:
        # same as above
        pass