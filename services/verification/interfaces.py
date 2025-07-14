
from abc import ABC, abstractmethod

class KYCProviderInterface(ABC):
    @abstractmethod
    def verifyNIN(self, nin: str) -> bool:
        # pass control to someone will both verify and store in a detabase
        pass

    @abstractmethod
    def verifyBankAccount(self, bank_code: str, bank_account: str) -> bool:
        # pass control to some response bank accouunt name and above argument to db
        pass

    @abstractmethod
    def verifyPhysicalAddress(self, physical_address: str) -> bool:
        # same as above
        pass

    @abstractmethod
    def get_physical_address_verification_response(self, physical_address: str) -> bool:
        # same as above
        pass