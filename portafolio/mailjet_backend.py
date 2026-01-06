from django.core.mail.backends.base import BaseEmailBackend
from mailjet_rest import Client

from django.conf import settings

class MailjetBackend(BaseEmailBackend):
    def send_messages(self, email_messages):
        if not email_messages:
            return 0
        mailjet = Client(auth=(settings.MAILJET_API_KEY, settings.MAILJET_API_SECRET), version='v3.1')
        sent_count = 0

        for message in email_messages:
            data = {
                'Messages': [
                    {
                        "From": {"Email": settings.DEFAULT_FROM_EMAIL},
                        "To": [{"Email": recipient} for recipient in message.to],
                        "Subject": message.subject,
                        "TextPart": message.body,
                    }
                ]
            }
            result = mailjet.send.create(data=data)
            if result.status_code == 200 or result.status_code == 201:
                sent_count += 1
            else:
                if not self.fail_silently:
                    raise Exception(f"Mailjet error {result.status_code}: {result.json()}")
        return sent_count
