from typing import Dict, Any, TypedDict
from django.conf import settings

from .mocks import MockLogisticsProvider, ClickNShipLogisticsProvider
from .models import DeliveryFee, LogisticsAssignment
from job.models import RepairJob
from bids.models import Bid
from user.models import Customer, Repairer


class UserDetails(TypedDict):
    Name: str
    City: str
    TownID: str
    Address: str
    Phone: str
    Email: str


class LogisticsService:
    def __init__(self):
        if settings.USE_SERVICE_MOCKS:
            self.provider = MockLogisticsProvider()
        else:
            self.provider = ClickNShipLogisticsProvider(
                username=settings.CLICKNSHIP_USERNAME,
                password=settings.CLICKNSHIP_PASSWORD
            )

    def calculate_delivery_fee(self, origin_address: str, destination_address: str,
                               weight: float, pickup_type: str = "1") -> DeliveryFee:
        response = self.provider.calculate_delivery_fee(
            origin=origin_address,
            destination=destination_address,
            weight=weight,
            pickup_type=pickup_type
        )
        return DeliveryFee.objects.create(
            delivery_fee=response["DeliveryFee"],
            vat_amount=response["VatAmount"],
            total_amount=response["TotalAmount"]
        )

    def create_pickup_request_for_customer(self, job_id: str) -> LogisticsAssignment:
        job_details = self._get_job_details(job_id)
        sender = self._format_customer_details(job_details["customer"], "pickup")
        recipient = self._format_repairer_details(job_details["repairer"])
        return self._create_pickup_request(job_id, sender, recipient)

    def create_pickup_request_for_repairer(self, job_id: str) -> LogisticsAssignment:
        job_details = self._get_job_details(job_id)
        sender = self._format_repairer_details(job_details["repairer"])
        recipient = self._format_customer_details(job_details["customer"], "delivery")
        return self._create_pickup_request(job_id, sender, recipient)

    def _get_job_details(self, job_id: str) -> Dict[str, Any]:
        job = RepairJob.objects.get(id=job_id)
        bid = Bid.objects.get(id=job.selected_bid.id)
        return {
            "job": job,
            "bid": bid,
            "repairer": Repairer.objects.get(id=bid.repairer.id),
            "customer": Customer.objects.get(id=job.customer.id)
        }

    def _format_address(self, address: str, town: str, city: str) -> str:
        return f"{address}, {town}, {city}"

    def _format_customer_details(self, customer: Customer, address_type: str) -> UserDetails:
        address = getattr(customer, f"{address_type}_address")
        town = getattr(customer, f"{address_type}_town")
        city = getattr(customer, f"{address_type}_city")
        return {
            "Name": f"{customer.first_name} {customer.last_name}",
            "City": city,
            "TownID": town,
            "Address": address,
            "Phone": customer.phone,
            "Email": customer.email
        }

    def _format_repairer_details(self, repairer: Repairer) -> UserDetails:
        return {
            "Name": f"{repairer.first_name} {repairer.last_name}",
            "City": repairer.work_city,
            "TownID": repairer.work_town,
            "Address": repairer.work_address,
            "Phone": repairer.phone,
            "Email": repairer.email
        }

    def _create_pickup_request(self, job_id: str,
                               sender: UserDetails,
                               recipient: UserDetails) -> LogisticsAssignment:
        job_details = self._get_job_details(job_id)
        job = job_details["job"]

        request_data = {
            "OrderNo": job_id,
            "Description": f"{job.device_brand} {job.device_model} for repair",
            "Weight": 0.20,
            "SenderName": sender["Name"],
            "SenderCity": sender["City"],
            "SenderTownID": sender["TownID"],
            "SenderAddress": sender["Address"],
            "SenderPhone": sender["Phone"],
            "SenderEmail": sender["Email"],
            "RecipientName": recipient["Name"],
            "RecipientCity": recipient["City"],
            "RecipientTownID": recipient["TownID"],
            "RecipientAddress": recipient["Address"],
            "RecipientPhone": recipient["Phone"],
            "RecipientEmail": recipient["Email"],
            "PaymentType": "Prepaid",
            "DeliveryType": "Normal Delivery",
            "PickupType": "1",
            "ShipmentItems": [{
                "ItemName": f"{job.device_brand} {job.device_model}",
                "ItemUnitCost": job.device_value,
                "ItemQuantity": 1,
                "ItemColour": "BLACK",
                "ItemSize": ".25kg"
            }]
        }

        response = self.provider.create_pickup_request(request_data)

        return LogisticsAssignment.objects.create(
            job_id=job_id,
            courier_id=self.provider.get_courier_id(),
            waybill_number=response["waybill_number"],
            pick_up_address=self._format_address(request_data["SenderAddress"],
                                                 request_data["SenderTownID"],
                                                 request_data["SenderCity"]),
            drop_off_address=self._format_address(request_data["RecipientAddress"],
                                                  request_data["RecipientTownID"],
                                                  request_data["RecipientCity"]),
            tracking_url=self.provider.get_tracking_url(response["waybill_number"]),
            status="ASSIGNED",
            delivery_fee=response["delivery_fee"],
            vat_amount=response["vat_amount"],
            total_amount=response["total_amount"]
        )

    def initiate_payment(self, waybill_number: str, callback_url: str) -> Dict[str, Any]:
        return self.provider.initiate_payment(waybill_number=waybill_number,
                                              callback_url=callback_url)

    def get_pickup_request_status(self, waybill_number: str) -> list[dict[str, str]]:
        return self.provider.get_pickup_request_status(waybill_number=waybill_number)
