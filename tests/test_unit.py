from mock import MagicMock, patch
import pytest
import requests

from nameko.testing.services import worker_factory

from email_sender_service import EmailSender



class TestEmaiSender(object):

    def test_send_email(self):
        service = worker_factory(EmailSender)

        payload = {
            'client': {
                'name': 'John',
                'email': 'john@example.com'
            },
            'payee': {
                'name': 'Ben',
                'email': 'ben@example.com'
            },
            'payment': {
                'amount': 198,
                'currency': "GBP"
            }
        }

        fake_request = MagicMock()
        fake_request.status_code = 200

        with patch('email_sender_service.EmailSender.create_email') as create_email:
            with patch('requests.post') as fake_post:
                create_email.return_value = 'EMAIL TESTING'
                fake_post.return_value = fake_request

                assert service.send_email(payload) == 200


    def test_create_email(self):
        service = worker_factory(EmailSender)

        payload = {
            'client': {
                'name': 'John',
                'email': 'john@example.com'
            },
            'payee': {
                'name': 'Ben'
            },
            'payment': {
                'amount': 198,
                'currency': "GBP"
            }
        }
        expected_email = "Dear Ben,\n\n\
You have received a payment of 198 GBP from John (john@example.com).\n\
\n\
Yours,\n\
student.com\n"

        actual_email = service.create_email(payload)

        assert actual_email == expected_email
