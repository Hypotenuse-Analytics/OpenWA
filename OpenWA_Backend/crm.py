import logging
import requests
import phonenumbers
from phonenumbers import region_code_for_number

from config import TWENTY_BASE_URL, TWENTY_API_KEY

logger = logging.getLogger(__name__)

HEADERS = {
    "Authorization": f"Bearer {TWENTY_API_KEY}",
    "Content-Type": "application/json",
}


def build_phone(phone: str):
    """
    Convert a WhatsApp number (e.g. 919876543210)
    into Twenty CRM Phone field format.
    """

    try:
        number = phonenumbers.parse("+" + phone)

        return {
            "primaryPhoneNumber": str(number.national_number),
            "primaryPhoneCallingCode": f"+{number.country_code}",
            "primaryPhoneCountryCode": region_code_for_number(number),
            "additionalPhones": [],
        }

    except Exception:
        logger.warning("Unable to parse phone number: %s", phone)

        return {
            "primaryPhoneNumber": phone,
            "primaryPhoneCallingCode": "",
            "primaryPhoneCountryCode": "",
            "additionalPhones": [],
        }


class TwentyCRM:

    def __init__(self):
        self.base_url = TWENTY_BASE_URL.rstrip("/")

    def find_by_chat(self, chat_id):
        url = f"{self.base_url}/whatsappLeads"

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=15,
        )
        response.raise_for_status()

        leads = response.json().get("data", {}).get("whatsappLeads", [])

        for lead in leads:
            if lead.get("chatId") == chat_id:
                return lead
        return None
    

    def create_lead(self, name, phone, chat_id):

        url = f"{self.base_url}/whatsappLeads"

        payload = {
            "name": name,
            "chatId": chat_id,
            "phoneNumber": build_phone(phone),
        }

        response = requests.post(
            url,
            headers=HEADERS,
            json=payload,
            timeout=15,
        )

        if not response.ok:
            logger.error(response.text)

        response.raise_for_status()

        logger.info("Created CRM Lead : %s", phone)

        return response.json()

    def update_lead(self, lead_id, name, phone, chat_id):

        url = f"{self.base_url}/whatsappLeads/{lead_id}"

        payload = {
            "name": name,
            "chatId": chat_id,
            "phoneNumber": build_phone(phone),
        }

        response = requests.patch(
            url,
            headers=HEADERS,
            json=payload,
            timeout=15,
        )

        if not response.ok:
            logger.error(response.text)

        response.raise_for_status()

        logger.info("Updated CRM Lead : %s", phone)

        return response.json()

    def sync_contact(self, name, phone, chat_id):

        try:

            lead = self.find_by_chat(chat_id)

            if lead is None:
                logger.info("Lead not found. Creating...")

                return self.create_lead(
                    name=name,
                    phone=phone,
                    chat_id=chat_id,
                )

            logger.info("Lead exists. Updating...")

            return self.update_lead(
                lead_id=lead["id"],
                name=name,
                phone=phone,
                chat_id=chat_id,
            )

        except Exception:
            logger.exception("CRM Sync Failed")
            return None