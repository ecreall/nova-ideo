# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import transaction
from transaction._transaction import Status

from pyramid_mailer import get_mailer
from pyramid_mailer.message import Attachment, Message
from pyramid.threadlocal import get_current_request


def mailer_send(subject="!",
                sender=None,
                recipients=[],
                body=None,
                html=None,
                attachments=[]):
    try:
        request = get_current_request()
        if sender is None:
            sender = request.registry.settings['mail.default_sender']

        mailer = get_mailer(request)
        message = Message(subject=subject,
                          sender=sender,
                          recipients=recipients,
                          body=body,
                          html=html)
        for attachment in attachments:
            attachment = Attachment(attachment.title,
                                    attachment.mimetype,
                                    attachment)
            message.attach(attachment)

        if transaction.get().status == Status.COMMITTED:
            mailer.send_immediately(message)
        else:
            mailer.send(message)

    except Exception:
        pass
