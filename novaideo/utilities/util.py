# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import random
import string
from pyramid import renderers
from pyramid.threadlocal import get_current_request
from pyramid.threadlocal import get_current_registry

from daceui.interfaces import IDaceUIAPI
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


def get_modal_actions(actions, request):
    dace_ui_api = get_current_registry().getUtility(IDaceUIAPI,
                                                   'dace_ui_api')
    actions = [(a.context, a.action) for a in actions]
    action_updated, messages, \
    resources, actions = dace_ui_api.update_actions(request,
                                                    actions)
    return action_updated, messages, resources, actions


def get_actions_navbar(actions_getter, request, descriminators):
    result = {}
    actions = actions_getter()
    isactive = True
    update_nb = 0
    while isactive and update_nb < 2:
        actions = actions_getter()
        modal_actions = [a for a in  actions \
                        if getattr(a.action, 'style_interaction', '') == \
                           'modal-action']
        isactive, messages, \
        resources, modal_actions = get_modal_actions(modal_actions, request)
        update_nb += 1

    modal_actions = [(a['action'], a) for a in modal_actions]
    result['modal-action'] = {'isactive': isactive,
                              'messages': messages ,
                              'resources': resources,
                              'actions': modal_actions
                              }
    for descriminator in descriminators:
        descriminator_actions = [a for a in actions \
                    if getattr(a.action, 'style_descriminator','') == \
                       descriminator]
        descriminator_actions = sorted(descriminator_actions, 
                       key=lambda e: getattr(e.action, 'style_order', 0))
        result[descriminator] = descriminator_actions

    return  result


def default_navbar_body(view, actions_navbar):
    global_actions = actions_navbar['global-action']
    text_actions = actions_navbar['text-action']
    modal_actions = actions_navbar['modal-action']['actions']
    template = 'novaideo:views/templates/navbar_actions.pt'
    result = {
        'global_actions': global_actions,
        'modal_actions': dict(modal_actions),
        'text_actions': text_actions,
       }
    body = renderers.render(template, result, view.request)
    return body


navbar_body_getter = default_navbar_body