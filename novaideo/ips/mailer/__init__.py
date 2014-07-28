import transaction

from pyramid_mailer import get_mailer
from pyramid_mailer.mailer import Mailer
from pyramid_mailer.message import Message
from pyramid.threadlocal import get_current_request


def mailer_send(subject="!",
                sender=None,
                recipients=[],
                body="",
                attachments=[]):

    if sender is None:
        sender = get_current_request().registry.settings['novaideo.admin_email']    

    mailer = get_mailer(get_current_request())
    message = Message(subject=subject,
                  sender=sender,
                  recipients=recipients,
                  body=body)
    for attachment in attachments:
        attachment = Attachment(attachment.title, attachment.mimetype, attachment)
        message.attach(attachment)

    mailer.send(message)
