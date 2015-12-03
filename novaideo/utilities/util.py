# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import math
import calendar
import datetime
import collections
import pytz
import string
import random
import unicodedata
from persistent.dict import PersistentDict
from persistent.list import PersistentList
from pyramid import renderers
from babel.core import Locale
from bs4 import BeautifulSoup
from pyramid.threadlocal import get_current_registry, get_current_request

from dace.processinstance.activity import ActionType
from dace.objectofcollaboration.principal.util import get_current
from dace.util import getSite
from daceui.interfaces import IDaceUIAPI


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


DATE_FORMAT = {
    'defined_literal': {
        'day_month_year': _('On ${month} ${day} ${year}'),
        'day_month': _('On ${month} ${day}'),
        'day': _('On ${day}'),
        'day_hour_minute_month_year': _("On ${month} ${day} ${year} at ${hour} o'clock and ${minute} minutes"),
        'day_hour_minute_month': _("On ${month} ${day} at ${hour} o'clock and ${minute} minutes"),
        'day_hour_minute': _("On ${day} at ${hour} o'clock and ${minute} minutes"),
        'day_hour_month_year': _("On ${month} ${day} ${year} at ${hour} o'clock"),
        'day_hour_month': _("On ${month} ${day} at ${hour} o'clock"),
        'day_hour': _("On ${day} at ${hour} o'clock")
    },
    'direct_literal': {
        'day_month_year': _('${month} ${day} ${year}'),
        'day_month': _('${month} ${day}'),
        'day': _('${day}'),
        'day_hour_minute_month_year': _("${month} ${day} ${year} at ${hour} o'clock and ${minute} minutes"),
        'day_hour_minute_month': _("${month} ${day} at ${hour} o'clock and ${minute} minutes"),
        'day_hour_minute': _("${day} at ${hour} o'clock and ${minute} minutes"),
        'day_hour_month_year': _("${month} ${day} ${year} at ${hour} o'clock"),
        'day_hour_month': _("${month} ${day} at ${hour} o'clock"),
        'day_hour': _("${day} at ${hour} o'clock")
    },
    'digital': {
        'day_month_year': _('${month}/${day}/${year}'),
        'day_month': _('${month}/${day}'),
        'day': _('${day}'),
        'day_hour_minute_month_year': _('${month}/${day}/${year} ${hour}:${minute}'),
        'day_hour_minute_month': _('${month}/${day} ${hour}:${minute}'),
        'day_hour_minute': _('${day} ${hour}:${minute}'),
        'day_hour_month_year': _('${month}/${day}/${year} ${hour}:00'),
        'day_hour_month': _('${month}/${day} ${hour}:00'),
        'day_hour_month': _('${day} ${hour}:00')
    }
}


def to_localized_time(
    date, request=None, date_from=None,
    date_only=False, format_id='digital',
    ignore_month=False, ignore_year=False,
    add_day_name=False, translate=False):
    if request is None:
        request = get_current_request()

    if date_from is None:
        date_from = datetime.datetime.now()

    hour = getattr(date, 'hour', None)
    minute = getattr(date, 'minute', None)
    date_dict = {
        'year': date.year,
        'day': date.day,
        'month': date.month,
        'hour': hour if not date_only else None,
        'minute': minute if not date_only and minute != 0 else None
    }
    if ignore_month:
        month = ((date_from.month != date_dict['month'] or \
                  date_from.year != date_dict['year']) and \
                 date_dict['month']) or None
        date_dict['month'] = month
        if month is None:
            date_dict['year'] = None

    if ignore_year and date_dict['year']:
        year = ((date_from.year != date_dict['year']) and \
                date_dict['year']) or None
        date_dict['year'] = year

    date_dict = {key: value for key, value in date_dict.items() if value}
    if 'minute' in date_dict and date_dict['minute'] < 10:
        date_dict['minute'] = '0' + str(date_dict['minute'])

    localizer = request.localizer
    if format_id.endswith('literal'):
        locale = Locale(localizer.locale_name)
        if 'day' in date_dict:
            if date_dict['day'] == 1:
                date_dict['day'] = localizer.translate(_('1st'))

            if add_day_name:
                weekday = date.weekday()
                day_name = locale.days['format']['wide'][weekday]
                date_dict['day'] = localizer.translate(
                    _('${name} ${day}',
                      mapping={'name': day_name, 'day': date_dict['day']}))

        if 'month' in date_dict:
            date_dict['month'] = locale.months['format']['wide'][date_dict['month']]

    date_format_id = '_'.join(sorted(list(date_dict.keys())))
    format = DATE_FORMAT[format_id].get(date_format_id)
    if translate:
        return localizer.translate(_(format, mapping=date_dict))

    return _(format, mapping=date_dict)


def deepcopy(obj):
    result = None
    if isinstance(obj, (dict, PersistentDict)):
        result = {}
        for key, value in obj.items():
            result[key] = deepcopy(value)

    elif isinstance(obj, (list, tuple, PersistentList)):
        result = [deepcopy(value) for value in obj]
    else:
        result = obj

    return result


def normalize_title(obj_title):
    obj_title = unicodedata.normalize(
        'NFKD', obj_title).encode('ascii',
                                  'ignore').decode().lower()
    obj_title = obj_title.replace('(', '').replace(')', '')
    return obj_title


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


def html_to_text(html):
    soup = BeautifulSoup(html, "lxml")
    element = soup.body
    if element is None:
        return ''

    text = ' '.join(element.stripped_strings)
    return text


def html_article_to_text(html):
    soup = BeautifulSoup(html, "lxml")
    articles = soup.find_all('div', 'article-body')
    if articles:
        article = articles[0]
        text = ' '.join(article.stripped_strings)
        return text

    return ''


def get_modal_actions(actions, request):
    dace_ui_api = get_current_registry().getUtility(
        IDaceUIAPI, 'dace_ui_api')
    actions = [(a.context, a.action) for a in actions]
    action_updated, messages, \
    resources, actions = dace_ui_api.update_actions(
        request, actions)
    return action_updated, messages, resources, actions


def get_actions_navbar(actions_getter, request, descriminators):
    result = {}
    actions = []
    isactive = True
    update_nb = 0
    while isactive and update_nb < 2:
        actions = actions_getter()
        modal_actions = [a for a in actions
                         if getattr(a.action, 'style_interaction', '') ==
                         'modal-action']
        isactive, messages, \
        resources, modal_actions = get_modal_actions(modal_actions, request)
        update_nb += 1

    modal_actions = [(a['action'], a) for a in modal_actions]
    result['modal-action'] = {'isactive': isactive,
                              'messages': messages,
                              'resources': resources,
                              'actions': modal_actions
                              }
    for descriminator in descriminators:
        descriminator_actions = [a for a in actions
                                 if getattr(a.action,
                                            'style_descriminator', '') ==
                                 descriminator]
        descriminator_actions = sorted(
            descriminator_actions,
            key=lambda e: getattr(e.action, 'style_order', 0))
        result[descriminator] = descriminator_actions

    return result


def default_navbar_body(view, context, actions_navbar):
    global_actions = actions_navbar['global-action']
    text_actions = actions_navbar['text-action']
    modal_actions = actions_navbar['modal-action']['actions']
    template = 'novaideo:views/templates/navbar_actions.pt'
    result = {
        'global_actions': global_actions,
        'modal_actions': dict(modal_actions),
        'text_actions': text_actions,
    }
    return renderers.render(template, result, view.request)


def footer_navbar_body(view, context, actions_navbar):
    global_actions = actions_navbar['footer-action']
    modal_actions = actions_navbar['modal-action']['actions']
    template = 'novaideo:views/templates/footer_navbar_actions.pt'
    result = {
        'footer_actions': global_actions,
        'modal_actions': dict(modal_actions)
    }
    return renderers.render(template, result, view.request)


navbar_body_getter = default_navbar_body


def footer_block_body(view, context, actions_navbar):
    footer_actions = actions_navbar['footer-entity-action']
    modal_actions = actions_navbar['modal-action']['actions']
    template = 'novaideo:views/templates/footer_entity_actions.pt'
    result = {
        'footer_actions': footer_actions,
        'modal_actions': dict(modal_actions)
    }
    return renderers.render(template, result, view.request)


class ObjectRemovedException(Exception):
    pass


def generate_navbars(view, context, request, **args):
    def actions_getter():
        return [a for a in context.actions
                if a.action.actionType != ActionType.automatic]

    all_actions = {}
    footer_navbar = get_actions_navbar(
        actions_getter, request, ['footer-entity-action'])
    actions_navbar = get_actions_navbar(
        actions_getter, request, ['global-action',
                                  'text-action',
                                  'admin-action',
                                  'wg-action'])
    actions_navbar['global-action'].extend(
        actions_navbar.pop('admin-action'))
    actions_body = get_actions_navbar(
        actions_getter, request, ['body-action'])

    actions_navbar['global-action'].extend(args.get('global_action', []))
    actions_navbar['text-action'].extend(args.get('text_action', []))
    footer_navbar['footer-entity-action'].extend(
        args.get('footer_entity_action', []))
    actions_body['body-action'].extend(args.get('body_action', []))
    all_actions.update(footer_navbar)
    all_actions.update(actions_navbar)
    all_actions.update(actions_body)
    if getattr(context, '__parent__', None) is None:
        raise ObjectRemovedException("Object removed")

    actions_bodies = []
    for action in actions_body['body-action']:
        object_values = {'action': action}
        body = view.content(args=object_values,
                            template=action.action.template)['body']
        actions_bodies.append(body)

    isactive = actions_navbar['modal-action']['isactive']
    messages = actions_navbar['modal-action']['messages']
    resources = actions_navbar['modal-action']['resources']
    return {'isactive': isactive,
            'messages': messages,
            'resources': resources,
            'all_actions': all_actions,
            'navbar_body': navbar_body_getter(view, context, actions_navbar),
            'footer_body': footer_block_body(view, context, footer_navbar),
            'body_actions': actions_bodies}
