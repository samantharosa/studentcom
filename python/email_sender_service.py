import logging
import requests

from nameko.dependency_providers import Config
from nameko.events import event_handler



class EmailSender(object):
    name = "email_sender"

    config = Config()

    @event_handler("payments", "payment_received")
    def send_email(self, payload):
        """Send an email to a client to inform them they have received a payment."""
        email_text = self.create_email(payload)

        key = self.config.get('api_key')
        sandbox = self.config.get('sandbox')

        recipient = '{0} <{1}>'.format(payload['payee']['name'], payload['payee']['email'])

        request_url = 'https://api.mailgun.net/v3/{0}/messages'.format(sandbox)
        request = requests.post(request_url, auth=('api', key), data={
            'from': 'Mailgun Sandbox <mailgun@{}>'.format(sandbox),
            'to': recipient,
            'subject': 'Payment received',
            'text': email_text
        })

        status_code = request.status_code
        if status_code == 200:
            logging.info("Sent the following email:\n%s", email_text)
        else:
            logging.critical(
                "Request Status Code: %s. Failed to send the following email:\n%s",
                status_code, email_text
            )

        return status_code

    @staticmethod
    def create_email(payload):
        """Generate body of the email to send."""
        payee = payload['payee']['name']
        amount = payload['payment']['amount']
        currency = payload['payment']['currency']
        client = payload['client']['name']
        email = payload['client']['email']

        email_text = "Dear {payee},\n\n\
You have received a payment of {amount} {currency} from {client} ({email}).\n\
\n\
Yours,\n\
student.com\n".format(
            payee=payee,
            amount=amount,
            currency=currency,
            client=client,
            email=email,
        )

        return email_text
