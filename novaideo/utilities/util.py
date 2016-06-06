# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import datetime
import pytz
import string
import random
import unicodedata
import re
from persistent.dict import PersistentDict
from persistent.list import PersistentList
from pyramid import renderers
from babel.core import Locale
from bs4 import BeautifulSoup
from pyramid.threadlocal import get_current_registry, get_current_request

from pontus.util import merge_dicts
from dace.processinstance.activity import ActionType
from dace.objectofcollaboration.principal.util import get_current
from dace.util import getSite, getAllBusinessAction
from daceui.interfaces import IDaceUIAPI

from .ical_date_utility import getDatesFromString, set_recurrence
from novaideo.content.correlation import Correlation, CorrelationType
from novaideo.content.processes import get_states_mapping
from novaideo.core import _

try:
    _LETTERS = string.letters
except AttributeError: #pragma NO COVER
    _LETTERS = string.ascii_letters


DATE_FORMAT = {
    'defined_literal': {
        'day_month_year': _('On ${month} ${day} ${year}'),
        'day_month': _('On ${month} ${day}'),
        'month_year': _('On ${month} ${year}'),
        'month': _('On ${month}'),
        'year': _('On ${year}'),
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
        'month_year': _('${month} ${year}'),
        'month': _('${month}'),
        'year': _('${year}'),
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
        'month_year': _('${month}/${year}'),
        'month': _('${month}'),
        'year': _('${year}'),
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
    ignore_day=False, add_day_name=False,
    force_ignore=False, translate=False):
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
        if force_ignore:
            date_dict.pop('month')
        else:
            month = ((date_from.month != date_dict['month'] or \
                      date_from.year != date_dict['year']) and \
                     date_dict['month']) or None
            date_dict['month'] = month
            if month is None:
                date_dict['year'] = None

    if ignore_year and date_dict['year']:
        if force_ignore:
            date_dict.pop('year')
        else:
            year = ((date_from.year != date_dict['year']) and \
                    date_dict['year']) or None
            date_dict['year'] = year

    date_dict = {key: value for key, value in date_dict.items()
                 if value is not None}
    if 'minute' in date_dict and date_dict['minute'] < 10:
        date_dict['minute'] = '0' + str(date_dict['minute'])

    if ignore_day:
        date_dict.pop('day')

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


def dates(propertyname):
    """Return a dates property.
    """
    def _get(self):
        return getattr(self, propertyname + '_dates_str', '')

    def _set(self, dates_str):
        """Set _dates_str, start_date, end_date and recurrence attributes
        """
        setattr(self, propertyname + '_dates_str', dates_str)
        dates = getDatesFromString(self, dates_str)
        # Set start and end dates from dates (list of list representing datetime)
        if not dates:
            setattr(self, propertyname + '_start_date', None)
            setattr(self, propertyname + '_end_date', None)
            setattr(self, propertyname + '_recurrence', '')
            return

        now = datetime.datetime.now(tz=pytz.UTC)
        if dates[0]:
            setattr(self, propertyname + '_start_date',
                    datetime.datetime(
                        dates[0][0], dates[0][1],
                        dates[0][2], tzinfo=pytz.UTC))
            setattr(self, propertyname + '_end_date',
                    datetime.datetime(
                        dates[0][0], dates[0][1],
                        dates[0][2], 23, 59, 59, tzinfo=pytz.UTC))
        else:
            setattr(self, propertyname + '_start_date', now)
            setattr(self, propertyname + '_end_date',
                    datetime.datetime(
                        now.year, now.month,
                        now.day, 23, 59, 59, tzinfo=pytz.UTC))

        setattr(self, propertyname + '_recurrence',
                set_recurrence(dates, dates_str))

    return property(_get, _set)


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

ALL_DESCRIMINATORS = ['global-action',
                      'text-action',
                      'admin-action',
                      'wg-action',
                      'plus-action',
                      'text-comm-action',
                      'body-action',
                      'communication-action']

DEFAUL_LISTING_FOOTER_ACTIONS_TEMPLATE = 'novaideo:views/templates/listing_footer_actions.pt'

DEFAUL_LISTING_ACTIONS_TEMPLATE= 'novaideo:views/templates/listing_object_actions.pt'

DEFAUL_NAVBAR_TEMPLATE = 'novaideo:views/templates/navbar_actions.pt'

FOOTER_NAVBAR_TEMPLATE = 'novaideo:views/templates/footer_navbar_actions.pt'

DEFAULT_MENU_TEMPLATE = 'novaideo:views/templates/navbar_actions.pt'

FOOTER_BLOCK_TEMPLATE = 'novaideo:views/templates/footer_entity_actions.pt'


def render_listing_objs(request, objs, user, **kw):
    result_body = []
    resources = {'css_links': [], 'js_links': []}
    for obj in objs:
        try:
            navbars = generate_listing_menu(
                request, obj,
                template=DEFAUL_LISTING_ACTIONS_TEMPLATE,
                footer_template=DEFAUL_LISTING_FOOTER_ACTIONS_TEMPLATE)
        except ObjectRemovedException:
            continue

        resources = merge_dicts(navbars['resources'], resources)
        object_values = {
            'object': obj,
            'current_user': user,
            'menu_body': navbars['menu_body'],
            'footer_body': navbars['footer_body'],
            'state': get_states_mapping(user, obj,
                getattr(obj, 'state_or_none', [None])[0])}
        object_values.update(kw)
        body = renderers.render(
            obj.templates.get('default'),
            object_values,
            request)
        result_body.append(body)

    return result_body, resources


def update_modal_actions(actions, context, request):
    dace_ui_api = get_current_registry().getUtility(
        IDaceUIAPI, 'dace_ui_api')
    actions = [(context, a) for a in actions]
    action_updated, messages, \
    resources, actions = dace_ui_api.update_actions(
        request, actions)
    return action_updated, messages, resources, actions


def get_actions_navbar(
    actions_getter, context, request, descriminators):
    result = {}
    actions = []
    isactive = True
    update_nb = 0
    while isactive and update_nb < 2:
        actions = actions_getter()
        modal_actions = [a for a in actions
                         if getattr(a, 'style_interaction', '') ==
                         'modal-action']
        isactive, messages, \
        resources, modal_actions = update_modal_actions(
            modal_actions, context, request)
        update_nb += 1

    modal_actions = [(a['action'], a) for a in modal_actions]
    result['modal-action'] = {'isactive': isactive,
                              'messages': messages,
                              'resources': resources,
                              'actions': modal_actions
                              }
    actions = sorted(
        actions, key=lambda a: getattr(a, 'style_order', 0))
    result.update({descriminator: [] for descriminator in descriminators})
    for action in actions:
        descriminator = getattr(action, 'style_descriminator', 'None')
        if descriminator in result:
            result[descriminator].insert(
                getattr(action, 'style_order', 0), action)

    return result


def render_navbar_body(
    request, context,
    actions_navbar,
    template=None,
    keys=['global-action', 'text-action', 'plus-action']):
    actions = {key.replace('-', '_'): actions_navbar.get(key, [])
               for key in keys}
    modal_actions = actions_navbar['modal-action']['actions']
    template = template if template else DEFAUL_NAVBAR_TEMPLATE
    actions['modal_actions'] = dict(modal_actions)
    actions['obj'] = context
    return renderers.render(template, actions, request)


class ObjectRemovedException(Exception):
    pass


def generate_navbars(request, context, **args):
    def actions_getter():
        return getAllBusinessAction(
                context, process_discriminator='Application')

    actions_navbar = get_actions_navbar(
        actions_getter, context, request, list(ALL_DESCRIMINATORS))
    if getattr(context, '__parent__', None) is None:
        raise ObjectRemovedException("Object removed")

    actions_navbar['global-action'].extend(
        actions_navbar.pop('admin-action'))
    actions_navbar['global-action'].extend(
        args.get('global_action', []))
    actions_navbar['text-action'].extend(
        actions_navbar.pop('text-comm-action'))
    actions_navbar['text-action'].extend(
        args.get('text_action', []))
    actions_navbar['plus-action'].extend(
        args.get('plus_action', []))
    actions_navbar['body-action'].extend(
        args.get('body_action', []))

    actions_bodies = []
    for action in actions_navbar['body-action']:
        object_values = {'action': action}
        body = renderers.render(
            action.action.template, object_values, request)
        actions_bodies.append(body)

    isactive = actions_navbar['modal-action']['isactive']
    messages = actions_navbar['modal-action']['messages']
    resources = actions_navbar['modal-action']['resources']
    return {'isactive': isactive,
            'messages': messages,
            'resources': resources,
            'all_actions': actions_navbar,
            'navbar_body': render_navbar_body(
                request, context, actions_navbar, args.get('template', None)),
            'footer_body': render_navbar_body(
                request, context, actions_navbar,
                DEFAUL_LISTING_FOOTER_ACTIONS_TEMPLATE, ['communication-action'])
                if 'communication-action' in actions_navbar else None,
            'body_actions': actions_bodies}


def generate_listing_menu(request, context, **args):
    def actions_getter():
        return getAllBusinessAction(
            context, process_discriminator='Application')

    descriminators = args.get(
        'descriminators',
        list(ALL_DESCRIMINATORS))
    actions_navbar = get_actions_navbar(
        actions_getter, context, request, descriminators)
    if getattr(context, '__parent__', None) is None and \
       context is not request.root:
        raise ObjectRemovedException("Object removed")

    actions_navbar['actions'] = []
    tomerge = descriminators
    if 'communication-action' in tomerge and \
       'text-comm-action' in tomerge:
        actions_navbar['communication-action'].extend(
            actions_navbar.pop('text-comm-action'))
        tomerge.remove('communication-action')

    for descriminator in tomerge:
        if descriminator in actions_navbar:
            actions_navbar['actions'].extend(
                actions_navbar.pop(descriminator))

    isactive = actions_navbar['modal-action']['isactive']
    messages = actions_navbar['modal-action']['messages']
    resources = actions_navbar['modal-action']['resources']
    return {'isactive': isactive,
            'messages': messages,
            'resources': resources,
            'menu_body': render_navbar_body(
                request, context, actions_navbar,
                args.get('template', None), ['actions']),
            'footer_body':  render_navbar_body(
                request, context, actions_navbar,
                args.get('footer_template', None), ['communication-action'])
            if 'communication-action' in actions_navbar else None
            }
