from pyramid_mailer import get_mailer
from pyramid_mailer.message import Attachment, Message
from pyramid.threadlocal import get_current_request


def mailer_send(subject="!",
                sender=None,
                recipients=[],
                body="",
                attachments=[]):

    request = get_current_request()
    if sender is None:
        sender = request.registry.settings['novaideo.admin_email']

    mailer = get_mailer(request)
    message = Message(subject=subject,
                      sender=sender,
                      recipients=recipients,
                      body=body)
    for attachment in attachments:
        attachment = Attachment(attachment.title, attachment.mimetype,
                                attachment)
        message.attach(attachment)

    mailer.send(message)
