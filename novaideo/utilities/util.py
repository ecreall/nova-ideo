# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import random
import string
from pyramid.threadlocal import get_current_request

from dace.util import getSite, find_catalog
from dace.objectofcollaboration.principal.util import get_current

from novaideo.content.correlation import Correlation, CorrelationType
from novaideo.mail import (
    NEWCONTENT_SUBJECT,
    NEWCONTENT_MESSAGE)
from novaideo.content.interface import IPerson
from novaideo.ips.mailer import mailer_send
from novaideo.core import _

try:
    _LETTERS = string.letters
except AttributeError: #pragma NO COVER
    _LETTERS = string.ascii_letters


def gen_random_token():
    length = random.choice(range(10, 16))
    chars = _LETTERS + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def connect(source, 
            targets,
            intention,
            author=None,
            tags=[],
            correlation_type=CorrelationType.weak,
            unique=False):
    """Connect source to targets"""
    root = getSite()
    if author is None:
        author = get_current()

    datas = {'author': author,
             'source': source,
             'comment': intention['comment'],
             'intention': intention['type']}
    if unique:
        datas['targets'] = targets
        correlation = Correlation()
        correlation.set_data(datas)
        correlation.tags.extend(tags)
        correlation.type = correlation_type
        root.addtoproperty('correlations', correlation)
        return correlation
    else:
        correlations = []
        for content in targets:
            correlation = Correlation()
            datas['targets'] = [content]
            correlation.set_data(datas)
            correlation.tags.extend(tags)
            correlation.type = correlation_type
            root.addtoproperty('correlations', correlation)
            correlations.append(correlation)

        return correlations


def disconnect(source, 
            targets,
            tag=None,
            correlation_type=CorrelationType.weak):
    """Disconnect targets from the source"""
    root = getSite()
    correlations = []
    if tag:
        correlations = [c for c in source.source_correlations \
                      if ((c.type==correlation_type) and (tag in c.tags))]
    else:
        correlations = [c for c in source.source_correlations \
                      if (c.type==correlation_type)]

    for content in targets:
        for correlation in correlations:
            if content in correlation.targets:
                if len(correlation.targets) == 1:
                    root.delfromproperty('correlations', correlation)
                    correlation.delfromproperty('source', source)

                correlation.delfromproperty('targets', content)


def get_users_by_keywords(keywords):
    novaideo_catalog = find_catalog('novaideo')
    dace_catalog = find_catalog('dace')
    keywords_index = novaideo_catalog['object_keywords']
    object_provides_index = dace_catalog['object_provides']
    states_index = dace_catalog['object_states']
    #query
    query = keywords_index.any(keywords) & \
            object_provides_index.any(IPerson.__identifier__) & \
            states_index.notany(('deactivated',))
    return query.execute().all()


_CONTENT_TRANSLATION = [_("The proposal"),
                        _("The idea")]


def send_alert_new_content(content):
    keywords = content.keywords
    request = get_current_request()
    users = get_users_by_keywords([k.lower() for k in keywords])
    url = request.resource_url(content, "@@index")
    subject = NEWCONTENT_SUBJECT.format(subject_title=content.title)
    localizer = request.localizer
    for member in users:
        message = NEWCONTENT_MESSAGE.format(
            recipient_title=localizer.translate(_(getattr(member, 
                                                        'user_title',''))),
            recipient_first_name=getattr(member, 'first_name', member.name),
            recipient_last_name=getattr(member, 'last_name',''),
            subject_title=content.title,
            subject_url=url,
            subject_type=localizer.translate(
                           _("The " + content.__class__.__name__.lower())),
            novaideo_title=request.root.title
             )
        mailer_send(subject=subject, 
            recipients=[member.email], 
            body=message)
