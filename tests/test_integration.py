from nameko.testing.utils import get_container
from nameko.testing.services import entrypoint_hook, replace_dependencies

from email_sender_service import EmailSender



PAYLOAD = {
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


def test_email_successful(runner_factory, rabbit_config):
    config = {
        'AMQP_URI': 'pyamqp://guest:guest@localhost',
        'api_key': 'key-9e3925925d8652ea483d1f99c470650f',
        'sandbox': 'sandboxa335ce01177d450eafe21b96efc07255.mailgun.org'
    }

    runner = runner_factory(rabbit_config, EmailSender)

    container = get_container(runner, EmailSender)
    replace_dependencies(container, config=config)
    container.start()

    with entrypoint_hook(container, "send_email") as entrypoint:
        assert entrypoint(PAYLOAD) == 200

    container.stop()


def test_email_failed(runner_factory, rabbit_config):
    config = {
        'AMQP_URI': 'pyamqp://guest:guest@localhost',
        'api_key': None,
        'sandbox': None
    }

    runner = runner_factory(rabbit_config, EmailSender)

    container = get_container(runner, EmailSender)
    replace_dependencies(container, config=config)
    container.start()

    with entrypoint_hook(container, "send_email") as entrypoint:
        assert entrypoint(PAYLOAD) == 401

    container.stop()
