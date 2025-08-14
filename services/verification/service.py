from django.conf import settings
from .models import VerificationRecord
from .interfaces import VerificationProviderInterface
from .mocks import MockVerificationProvider, InterSwitchMarketPlaceVerificationProvider


class VerificationService:
    def __init__(self):
        if settings.USE_SERVICE_MOCKS:
            self.provider = MockVerificationProvider()
        else:
            # Real implementation would go here
            self.provider = InterSwitchMarketPlaceVerificationProvider()

    def verify_nin(self, user_id: int, nin: str) -> VerificationRecord:
        user_verification = VerificationRecord.objects.get(user_id=user_id)
        result = self.provider.verify_nin(nin)
        if result:
            user_verification.nin_status = 'VERIFIED'
            user_verification.save()
            return user_verification

        else:
            user_verification.nin_status = 'FAILED'
            user_verification.save()
            return user_verification

    def verify_bank_account(self, user_id: int, account_number: str, bank_code: str) -> VerificationRecord:
        user_verification = VerificationRecord.objects.get(user_id=user_id)
        result = self.provider.verify_bank_account(account_number, bank_code)
        if result:
            user_verification.bank_account_status = 'VERIFIED'
            user_verification.save()
            return user_verification
        else:
            user_verification.bank_account_status = 'FAILED'
            user_verification.save()
            return user_verification

    def verify_work_address(self, user_id: int, address: dict[str, str]) -> VerificationRecord:
        user_verification = VerificationRecord.objects.get(user_id=user_id)
        if not user_verification:
            reference_id: str = self.provider.verify_address(address)
            user_verification = VerificationRecord.objects.create(
                user_id=user_id,
                work_address_status='PENDING',
                nin_status='PENDING',
                bank_account_status='PENDING',
                reference_id=reference_id,
            )
            user_verification.save()
            return user_verification
        else:
            reference_id: str = user_verification.work_address_verification_reference_id
            is_verified: bool = (self.provider
            .get_physical_address_verification_response(
                reference_id=reference_id))
            if is_verified:
                user_verification.work_address_status = 'VERIFIED'
                user_verification.save()
                return user_verification
            return user_verification
