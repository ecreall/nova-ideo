# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms
# available on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import mimetypes
import datetime
import pytz
import string
import random
import unicodedata
import json
import itertools
import collections
from webob.multidict import MultiDict
from persistent.dict import PersistentDict
from persistent.list import PersistentList
from pyramid import renderers
from babel.core import Locale
from bs4 import BeautifulSoup
from pyramid.threadlocal import get_current_registry, get_current_request

from substanced.util import get_oid

import html_diff_wrapper
from pontus.util import update_resources
from pontus.index import Index
from pontus.file import OBJECT_OID
from pontus.util import merge_dicts, get_view
from dace.objectofcollaboration.principal.util import get_current, has_role
from dace.util import getSite, getAllBusinessAction, getBusinessAction, get_obj, request_memoize
from daceui.interfaces import IDaceUIAPI
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS

from .ical_date_utility import getDatesFromString, set_recurrence
from novaideo.content.ballot import DEFAULT_BALLOT_GROUP
from novaideo.utilities.url_extractor import extract_urls
from novaideo.content.correlation import Correlation, CorrelationType
from novaideo.content.processes import get_states_mapping
from novaideo import _, log
from novaideo.fr_stopdict import _words
from novaideo.core import Node
from novaideo.emojis import DEFAULT_EMOJIS
from novaideo.adapters.stat_adapter import (
    IStat, DEFAULT_STAT_TEMPLATE, DEFAULT_EVALUATION_STAT_TEMPLATE)


try:
    _LETTERS = string.letters
except AttributeError: #pragma NO COVER
    _LETTERS = string.ascii_letters


DATE_FORMAT = {
    'defined_literal': {
        'day_month_year': _('On ${day} ${month} ${year}'),
        'day_month': _('On ${day} ${month}'),
        'month_year': _('In ${month} ${year}'),
        'month': _('In ${month}'),
        'year': _('In ${year}'),
        'day': _('On ${day}'),
        'day_hour_minute_month_year': _("On ${day} ${month} ${year} at ${hour} o'clock and ${minute} minutes"),
        'day_hour_minute_month': _("On ${day} ${month} at ${hour} o'clock and ${minute} minutes"),
        'day_hour_minute': _("On ${day} at ${hour} o'clock and ${minute} minutes"),
        'day_hour_month_year': _("On ${day} ${month} ${year} at ${hour} o'clock"),
        'day_hour_month': _("On ${day} ${month} at ${hour} o'clock"),
        'day_hour': _("On ${day} at ${hour} o'clock")
    },
    'direct_literal': {
        'day_month_year': _('${day} ${month} ${year}'),
        'day_month': _('${day} ${month}'),
        'month_year': _('${month} ${year}'),
        'month': _('${month}'),
        'year': _('${year}'),
        'day': _('${day}'),
        'day_hour_minute_month_year': _("${day} ${month} ${year} at ${hour} o'clock and ${minute} minutes"),
        'day_hour_minute_month': _("${day} ${month} at ${hour} o'clock and ${minute} minutes"),
        'day_hour_minute': _("${day} at ${hour} o'clock and ${minute} minutes"),
        'day_hour_month_year': _("${day} ${month} ${year} at ${hour} o'clock"),
        'day_hour_month': _("${day} ${month} at ${hour} o'clock"),
        'day_hour': _("${day} at ${hour} o'clock")
    },
    'digital': {
        'day_month_year': _('${day}/${month}/${year}'),
        'day_month': _('${day}/${month}'),
        'month_year': _('${month}/${year}'),
        'month': _('${month}'),
        'year': _('${year}'),
        'day': _('${day}'),
        'day_hour_minute_month_year': _('${day}/${month}/${year} ${hour}:${minute}'),
        'day_hour_minute_month': _('${day}/${month} ${hour}:${minute}'),
        'day_hour_minute': _('${day} ${hour}:${minute}'),
        'day_hour_month_year': _('${day}/${month}/${year} ${hour}:00'),
        'day_hour_month': _('${day}/${month} ${hour}:00')
    }
}


MIMETYPES_MANAGER = mimetypes.MimeTypes()


def to_localized_time(
    date, request=None, date_from=None,
    date_only=False, format_id='digital',
    ignore_month=False, ignore_year=False,
    ignore_day=False, add_day_name=False,
    force_ignore=False, translate=False):
    if request is None:
        request = get_current_request()

    if date_from is None:
        date_from = datetime.datetime.now(
            tz=getattr(request, 'get_time_zone', pytz.timezone('Europe/Paris')))

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


def date_delta(date, tz=pytz.UTC):
    now = datetime.datetime.now(tz=tz)
    delta = now - date
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    result = {}
    if delta.days > 0:
        result['days'] = delta.days

    if hours > 0:
        result['hours'] = hours

    if minutes > 0:
        result['minutes'] = minutes

    if seconds > 0:
        result['seconds'] = seconds

    return result


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


def add_mimetype_map(mimetype, extension):
    common = MIMETYPES_MANAGER.types_map[0]
    base = MIMETYPES_MANAGER.types_map[1]
    common_inv = MIMETYPES_MANAGER.types_map_inv[0]
    base_inv = MIMETYPES_MANAGER.types_map_inv[1]
    if mimetype not in common and \
       mimetype not in base:
        common['.'+extension] = mimetype
        common_inv[mimetype] = common_inv[mimetype] if \
            mimetype in common_inv else []
        common_inv[mimetype].append('.'+extension)
    elif mimetype in common_inv:
        if extension not in common_inv[mimetype]:
            common_inv[mimetype].append('.'+extension)
    elif mimetype in base_inv:
        if extension not in base_inv[mimetype]:
            base_inv[mimetype].append('.'+extension)


def guess_extension(file_):
    mimetype = getattr(file_, 'mimetype', None)
    if mimetype:
        extensions = MIMETYPES_MANAGER.types_map_inv[1].get(mimetype, [])
        if not extensions:
            extensions = MIMETYPES_MANAGER.types_map_inv[0].get(mimetype, [])

        if extensions:
            return extensions[0][1:]

    return 'file'


def combinaisons(items, nb):
    return itertools.combinations(items, nb)

# end source: http://dinoblog.tuxfamily.org/?p=40


def word_frequencies(content, blacklist):
    """
    Count the number of words in a content, excluding blacklisted terms.
    Return a generator of tuples (count, word) sorted by descending frequency.

    Example::

        >>> song = 'Ob la di ob la da "rla di da" da "da"'
        >>> for count, word in word_frequencies(song, ['di']):
        ...     print "%s %s" % (count, word)
        ...
        4 da
        2 la
        2 ob
        1 rla
    """
    sorted_words = sorted(
        [word for word in content.lower().replace('"', '').split()
         if word not in blacklist])
    return ((len(list(group)), word) for word, group in itertools.groupby(sorted_words))


def extract_keywords(text):
    "TODO"
    result = sorted(
        word_frequencies(text, _words),
        key=lambda e: e[0], reverse=True)
    return [e[1] for e in result]


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
    correlations = []
    if unique:
        datas['targets'] = targets
        correlation = Correlation()
        correlation.set_data(datas)
        correlation.tags.extend(tags)
        correlation.type = correlation_type
        root.addtoproperty('correlations', correlation)
        correlations = [correlation]
    else:
        for content in targets:
            correlation = Correlation()
            datas['targets'] = [content]
            correlation.set_data(datas)
            correlation.tags.extend(tags)
            correlation.type = correlation_type
            root.addtoproperty('correlations', correlation)
            correlations.append(correlation)

    objects = [source]
    objects.extend(targets)
    for obj in objects:
        if isinstance(obj, Node):
            obj.init_graph()
            break

    return correlations


def disconnect(
    source,
    targets,
    tag=None,
    correlation_type=CorrelationType.weak):
    """Disconnect targets from the source"""
    root = getSite()
    correlations = []
    if tag:
        correlations = [c for c in source.source_correlations
                        if ((c.type == correlation_type) and
                            (tag in c.tags))]
    else:
        correlations = [c for c in source.source_correlations
                        if c.type == correlation_type]

    for content in targets:
        for correlation in correlations:
            if content in correlation.targets:
                if len(correlation.targets) == 1:
                    root.delfromproperty('correlations', correlation)
                    correlation.delfromproperty('source', source)

                correlation.delfromproperty('targets', content)

    objects = [source]
    objects.extend(targets)
    calculated = []
    for obj in objects:
        if isinstance(obj, Node):
            oid = obj.get_node_id()
            if oid not in calculated:
                graph, calculated = obj.init_graph(calculated)


def get_files_data(files):
    result = []
    for picture in files:
        if picture:
            if picture.mimetype.startswith('image'):
                result.append({
                    'content': picture.url,
                    'type': 'img'})

            if picture.mimetype.startswith(
                    'application/x-shockwave-flash'):
                result.append({
                    'content': picture.url,
                    'type': 'flash'})

            if picture.mimetype.startswith('text/html'):
                blob = picture.blob.open()
                blob.seek(0)
                content = blob.read().decode("utf-8")
                blob.seek(0)
                blob.close()
                result.append({
                    'content': content,
                    'type': 'html'})

    return result


def add_file_data(container, attr):
    file_ = container.get(attr, None)
    if file_ and hasattr(file_, 'get_data'):
        container[attr] = file_.get_data(None)
        container[attr][OBJECT_OID] = str(get_oid(file_))

    return container


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


def render_urls(urls, request):
    url_results = []
    for url, url_metadata in urls.items():
        value = renderers.render(
            'novaideo:views/templates/text_url.pt',
            url_metadata, request)
        url_results.append(value)

    formatted_urls = '<div>' + ''.join(url_results) + '</div>'
    urls = extract_urls(html_to_text(formatted_urls))
    for url in urls:
        formatted_urls = formatted_urls.replace(
            url, '<a  target="_blank" href="'+url+'">'+url+'</a>')

    return formatted_urls


def truncate_text(text, nb, ellipsis='...'):
    truncated_text = text[:nb]
    urls = extract_urls(text)
    if urls:
        sorted_urls = sorted(
            urls,
            key=lambda url: len(url),
            reverse=True)
        truncated_urls = extract_urls(truncated_text)
        for index, url in enumerate(truncated_urls):
            truncated_text = truncated_text.replace(
                url, '<@url'+str(index)+'>', 1)

        for url in sorted_urls:
            index = urls.index(url)
            urls[index] = None
            truncated_text = truncated_text.replace(
                '<@url'+str(index)+'>',
                '<a  target="_blank" href="'+url+'">'+url+'</a>')

    if len(text) > nb:
        truncated_text += ellipsis

    return truncated_text


def get_debatescore_data(context, request):
    from .alerts_utility import get_user_data
    accessible_to_anonymous = request.accessible_to_anonymous
    author = getattr(context, 'author', None)
    author_data = get_user_data(author, 'author', request)
    organization = getattr(author, 'organization', None)
    published_at = getattr(context, 'published_at', None)
    p_at_str = published_at.strftime("%Y-%m-%d") if published_at else ''
    working_group = getattr(context, 'working_group', None)
    members = getattr(working_group, 'members', [])
    status = 'en-cours'
    if request.examine_ideas and 'submitted_support' in context.state:
        status = 'examen'

    result = MultiDict({
        'dc.title': context.title,
        'dc.identifier': getattr(context, '__oid__', None),
        'dc.description.abstract': context.presentation_text(),
        'dc.subject': ', '.join(context.keywords),
        'vp.status': status,
        'dc.date.Issued': p_at_str,
        'dc.date.Submitted': p_at_str,
        'dc.date.Accepted': p_at_str,
        'dc.type': 'interactive ressource',
        'vp.participationMode': 'en ligne',
        'dc.audience': 'tout public' if accessible_to_anonymous else \
                       'représentants',
        'dc.creator.corporateName': organization.title if organization else \
                                    '',
        'dc.creator.personnalName': author_data['author_first_name'] + ' ' + \
                                    author_data['author_last_name'],
        'dc.publisher': request.root.title,
        'vp.relation.websitedebate': request.resource_url(
            context, '@@index'),
        'dc.rights': 'licence libre d’utilisation' if \
                     accessible_to_anonymous else 'licence propriétaire',
        'dc.language': 'fr',
        'dc.format': 'text/html'
    })
    result['dc.type'] = 'débat public'
    for member in members:
        member_data = get_user_data(author, 'member', request)
        title = member_data['member_first_name'] + ' ' + \
            member_data['member_last_name']
        result.add('dc.contributor.personalName', title)

    return result


ALL_DESCRIMINATORS = ['text-action',
                      'global-action',
                      'lateral-action',
                      'access-action',
                      'primary-action',
                      'listing-primary-action',
                      'admin-action',
                      'wg-action',
                      'listing-wg-action',
                      'plus-action',
                      'body-action',
                      'communication-action',
                      'communication-body-action',
                      'support-action']

DEFAUL_LISTING_FOOTER_ACTIONS_TEMPLATE = 'novaideo:views/templates/listing_footer_actions.pt'

DEFAUL_WG_LISTING_ACTIONS_TEMPLATE = 'novaideo:views/templates/wg_listing_actions.pt'

DEFAUL_LISTING_PRIMARY_ACTIONS_TEMPLATE = 'novaideo:views/templates/listing_object_primary_actions.pt'

DEFAUL_LISTING_ACTIONS_TEMPLATE = 'novaideo:views/templates/listing_object_actions.pt'

DEFAUL_NAVBAR_TEMPLATE = 'novaideo:views/templates/navbar_actions.pt'

FOOTER_NAVBAR_TEMPLATE = 'novaideo:views/templates/footer_navbar_actions.pt'

DEFAULT_MENU_TEMPLATE = 'novaideo:views/templates/navbar_actions.pt'

FOOTER_BLOCK_TEMPLATE = 'novaideo:views/templates/footer_entity_actions.pt'

EMOJI_TEMPLATE = 'novaideo:views/templates/emoji_selector.pt'

DEFAUL_ACCESS_LISTING_ACTIONS_TEMPLATE = 'novaideo:views/templates/listing_access_actions.pt'

FILE_TEMPLATE = 'novaideo:views/templates/up_file_result.pt'

FILES_SLIDER_TEMPLATE = 'novaideo:views/templates/files_slider.pt'

VOTE_TEMPLATE = 'novaideo:views/templates/vote_actions.pt'

DEFAULT_SUPPORT_TEMPLATE = 'novaideo:views/templates/support_entity_actions.pt'


@request_memoize
def get_object_stat(context, request, adapter=None):
    result = {}
    if adapter is None:
        adapter = get_current_registry().queryAdapter(
            context, IStat)

    if adapter is not None:
        result = adapter.get_content_stat(request)

    return result


def render_object_stat(context, request, template=DEFAULT_STAT_TEMPLATE):
    adapter = get_current_registry().queryAdapter(
        context, IStat)
    if adapter is not None:
        data = get_object_stat(context, request, adapter)
        return adapter.render_stat(request, data=data)

    return None


@request_memoize
def get_object_evaluation_stat(context, request, adapter=None):
    result = {}
    if adapter is None:
        adapter = get_current_registry().queryAdapter(
            context, IStat)

    if adapter is not None:
        result = adapter.get_evaluation_stat(request)

    return result


def render_object_evaluation_stat(context, request, template=DEFAULT_EVALUATION_STAT_TEMPLATE):
    adapter = get_current_registry().queryAdapter(
        context, IStat)
    if adapter is not None:
        data = get_object_evaluation_stat(context, request, adapter)
        return adapter.render_evaluation_stat(request, data=data)

    return None


@request_memoize
def get_object_examination_stat(context, request, adapter=None):
    result = {}
    if adapter is None:
        adapter = get_current_registry().queryAdapter(
            context, IStat)

    if adapter is not None:
        result = adapter.get_examination_stat(request)

    return result


def render_object_examination_stat(context, request, template=DEFAULT_EVALUATION_STAT_TEMPLATE):
    adapter = get_current_registry().queryAdapter(
        context, IStat)
    if adapter is not None:
        data = get_object_examination_stat(context, request, adapter)
        return adapter.render_examination_stat(request, data=data)

    return None


def render_object_header(context, request, **kw):
    active_folder_id = None
    active_folder = None
    if request.GET:
        active_folder_id = dict(request.GET._items).get('folderid', None)

    try:
        if active_folder_id:
            active_folder = get_obj(int(active_folder_id))
    except (TypeError, ValueError):
        active_folder = None

    context = active_folder or context
    header_template = getattr(context, 'templates', {}).get('header', None)
    body = ''
    if header_template:
        data = {
            'object': context,
            'is_portal_manager': has_role(role=('PortalManager',))}
        data.update(kw)
        body = renderers.render(
            header_template,
            data,
            request)

    return body


def render_small_listing_objs(
    request, objs, user,
    view_type='default', **kw):
    result_body = []
    for obj in objs:
        object_values = {
            'object': obj,
            'current_user': user,
            'state': get_states_mapping(user, obj,
                getattr(obj, 'state_or_none', [None])[0])}
        body = renderers.render(
            obj.templates.get('small'),
            object_values,
            request)
        result_body.append(body)

    return result_body


def render_listing_obj(
    request, obj, user,
    view_type='default', **kw):
    display_state = kw.get('display_state', True)
    try:
        args = {}
        if view_type in ('bloc', 'card'):
            args['tounmerge'] = [
                'communication-action',
                'access-action',
                'support-action']

        navbars = generate_listing_menu(
            request, obj, view_type=view_type, **args)
    except ObjectRemovedException:
        return ''

    object_values = {
        'object': obj,
        'current_user': user,
        'primary_menu_body': navbars['primary_menu_body'],
        'menu_body': navbars['menu_body'],
        'footer_body': navbars['footer_body'],
        'wg_body': navbars['wg_body'],
        'footer_actions_body': navbars['footer_actions_body'],
        'support_actions_body': navbars['support_actions_body'],
        'access_body': navbars['access_body'],
        'state': get_states_mapping(
            user, obj,
            getattr(obj, 'state_or_none', [None])[0]) if display_state else None}
    object_values.update(kw)
    return renderers.render(
        obj.templates.get(view_type),
        object_values,
        request)


def render_index_obj(request, obj, user, **kw):
    body = ''
    try:
        view_instance = Index(obj, request)
        view_result = view_instance()
        if isinstance(view_result, dict) and 'coordinates' in view_result:
            body = view_instance.render_item(
                view_result['coordinates'][view_instance.coordinates][0],
                view_instance.coordinates, None)
    except Exception as error:
        log.warning(error)

    return body


def render_view_obj(request, obj, view, **kw):
    body = ''
    try:
        view = get_view(obj, request, view)
        if view:
            view = view.__original_view__
            view_instance = view(obj, request)
            view_result = view_instance()
            if isinstance(view_result, dict) and 'coordinates' in view_result:
                body = view_instance.render_item(
                    view_result['coordinates'][view_instance.coordinates][0],
                    view_instance.coordinates, None)

    except Exception as error:
        log.warning(error)

    return body


def render_view_comment(request, comment, **kw):
    from novaideo.views.idea_management.comment_idea import (
        CommentsView)
    body = ''
    try:
        context = comment.channel.subject
        context = context if context else request.root
        result_view = CommentsView(context, request)
        result_view.comments = [comment]
        body = result_view.update()['coordinates'][result_view.coordinates][0]['body']
    except Exception as error:
        log.warning(error)

    return body


def render_listing_objs(
    request, objs, user,
    view_type='default', **kw):
    result_body = []
    display_state = kw.get('display_state', True)
    resources = {'css_links': [], 'js_links': []}
    args = {}
    if view_type in ('bloc', 'card'):
        args['tounmerge'] = [
            'communication-action',
            'access-action',
            'support-action']

    for obj in objs:
        try:
            navbars = generate_listing_menu(
                request, obj, view_type=view_type, **args)
        except ObjectRemovedException:
            continue

        resources = merge_dicts(navbars['resources'], resources)
        object_values = {
            'object': obj,
            'current_user': user,
            'primary_menu_body': navbars['primary_menu_body'],
            'menu_body': navbars['menu_body'],
            'footer_body': navbars['footer_body'],
            'wg_body': navbars['wg_body'],
            'footer_actions_body': navbars['footer_actions_body'],
            'support_actions_body': navbars['support_actions_body'],
            'access_body': navbars['access_body'],
            'state': get_states_mapping(user, obj,
                getattr(obj, 'state_or_none', [None])[0]) if display_state else None}
        object_values.update(kw)
        body = renderers.render(
            obj.templates.get(view_type),
            object_values,
            request)
        result_body.append(body)

    return result_body, resources


def update_ajax_actions(
    actions, context, request,
    include_resources=False):
    dace_ui_api = get_current_registry().getUtility(
        IDaceUIAPI, 'dace_ui_api')
    actions = [(context, a) for a in actions]
    action_updated, messages, \
    resources, actions = dace_ui_api.update_actions(
        request, actions,
        include_resources=include_resources)
    return action_updated, messages, resources, actions


def update_ajax_action(
    context, request,
    process_id, node_id,
    include_resources=False):
    actions = getBusinessAction(
        context, request,
        process_id, node_id)
    if actions:
        isactive, messages, \
            resources, ajax_actions = update_ajax_actions(
                actions, context, request,
                include_resources)
        return ajax_actions, resources

    return [], {}


def update_all_ajax_action(
    context, request,
    node_id, process_id=None,
    include_resources=False):
    actions = getAllBusinessAction(
        context, request, node_id=node_id,
        process_id=process_id,
        process_discriminator='Application')
    if actions:
        isactive, messages, \
            resources, ajax_actions = update_ajax_actions(
                actions, context, request,
                include_resources)
        return ajax_actions, resources

    return [], {}


def get_actions_navbar(
    actions_getter, context, request, descriminators):
    result = {}
    actions = []
    isactive = True
    update_nb = 0
    while isactive and update_nb < 2:
        actions = actions_getter()
        ajax_actions = [a for a in actions
                        if getattr(a, 'style_interaction', '') ==
                        'ajax-action']
        isactive, messages, \
            resources, ajax_actions = update_ajax_actions(
                ajax_actions, context, request)
        update_nb += 1
        if isactive:
            request.invalidate_cache = True

    ajax_actions = [(a['action'], a) for a in ajax_actions]
    result['ajax-action'] = {
        'isactive': isactive,
        'messages': messages,
        'resources': resources,
        'actions': ajax_actions
    }
    actions = sorted(
        actions, key=lambda a: getattr(a, 'style_order', 0))
    result['all_actions'] = actions
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
    keys=['global-action', 'text-action', 'plus-action'],
    view_type='default'):
    values = {key.replace('-', '_'): actions_navbar.get(key, [])
               for key in keys if actions_navbar.get(key, [])}
    if values:
        ajax_actions = actions_navbar['ajax-action']['actions']
        template = template if template else DEFAUL_NAVBAR_TEMPLATE
        values['ajax_actions'] = dict(ajax_actions)
        values['obj'] = context
        values['view_type'] = view_type
        return renderers.render(template, values, request)

    return None


class ObjectRemovedException(Exception):
    pass


def generate_navbars(request, context, view_type='default', **args):
    def actions_getter():
        return getAllBusinessAction(
            context, request,
            process_id=args.get('process_id', None),
            node_id=args.get('node_id', None),
            process_discriminator='Application')

    root = request.root
    descriminators = args.get(
        'descriminators',
        list(ALL_DESCRIMINATORS))
    actions_navbar = get_actions_navbar(
        actions_getter, context, request, descriminators)
    if context is not root and getattr(context, '__parent__', None) is None:
        raise ObjectRemovedException("Object removed")

    if 'global-action' in actions_navbar:
        actions_navbar['global-action'].extend(
            actions_navbar.pop('admin-action', []))
        actions_navbar['global-action'].extend(
            args.get('global_action', []))
        actions_navbar['global-action'].extend(
            actions_navbar.pop('primary-action', []))

    actions_navbar.setdefault('text-action', [])
    actions_navbar['text-action'].extend(
        args.get('text_action', []))

    if 'plus-action' in actions_navbar:
        actions_navbar['plus-action'].extend(
            actions_navbar.pop('listing-primary-action', []))
        actions_navbar['plus-action'].extend(
            args.get('plus_action', []))
        if args.get('flatten', False):
            actions_navbar['global-action'] = actions_navbar.get(
                'global-action', [])
            actions_navbar['global-action'].extend(
                actions_navbar.pop('plus-action'))

    if 'body-action' in actions_navbar:
        actions_navbar['body-action'].extend(
            args.get('body_action', []))

    if 'communication-body-action' in actions_navbar:
        actions_navbar['communication-body-action'].extend(
            args.get('communication-body-action', []))

    actions_bodies = []
    for action in actions_navbar.get('body-action', []):
        object_values = {
            'action': action,
            'context': context,
            'request': request,
            'ajax_actions': dict(actions_navbar['ajax-action']['actions'])}
        body = renderers.render(
            action.template, object_values, request)
        actions_bodies.append(body)

    communication_actions_bodies = []
    for action in actions_navbar.get(
        'communication-body-action', []):
        object_values = {
            'action': action,
            'context': context,
            'request': request,
            'ajax_actions': dict(actions_navbar['ajax-action']['actions'])}
        body = renderers.render(
            action.template, object_values, request)
        communication_actions_bodies.append(body)

    isactive = actions_navbar['ajax-action']['isactive']
    messages = actions_navbar['ajax-action']['messages']
    resources = actions_navbar['ajax-action']['resources']
    return {'isactive': isactive,
            'messages': messages,
            'resources': resources,
            'all_actions': actions_navbar,
            'body_actions': actions_bodies,
            'context_actions': actions_navbar['all_actions'],
            'footer_actions_body': communication_actions_bodies,
            'navbar_body': render_navbar_body(
                request, context, actions_navbar, args.get('template', None),
                view_type=view_type),
            'footer_body': render_navbar_body(
                request, context, actions_navbar,
                DEFAUL_LISTING_FOOTER_ACTIONS_TEMPLATE,
                ['communication-action'], view_type=view_type)
            if 'communication-action' in actions_navbar else None,
            'wg_body':  render_navbar_body(
                request, context, actions_navbar,
                args.get('wg_template', DEFAUL_WG_LISTING_ACTIONS_TEMPLATE),
                ['wg-action'], view_type=view_type)
            if 'wg-action' in actions_navbar else None,
           'support_actions_body': render_navbar_body(
                request, context, actions_navbar,
                DEFAULT_SUPPORT_TEMPLATE,
                ['support-action'], view_type=view_type)
            if 'support-action' in actions_navbar else None,
            }


def generate_listing_menu(request, context, view_type='default', **args):
    def actions_getter():
        return getAllBusinessAction(
            context, request,
            process_id=args.get('process_id', None),
            node_id=args.get('node_id', None),
            process_discriminator='Application')

    #find actions descriminated by descriminators
    descriminators = args.get(
        'descriminators',
        list(ALL_DESCRIMINATORS))
    actions_navbar = get_actions_navbar(
        actions_getter, context, request, descriminators)
    if getattr(context, '__parent__', None) is None and \
       context is not request.root:
        raise ObjectRemovedException("Object removed")

    #for listing navbars merge actions (not actions to unmerge)
    actions_navbar['actions'] = []
    if 'primary-action' in actions_navbar and \
       'listing-primary-action' in actions_navbar:
        actions_navbar['primary-action'].extend(
            actions_navbar.pop('listing-primary-action', []))

    if 'wg-action' in actions_navbar and \
       'listing-wg-action' in actions_navbar:
        actions_navbar['wg-action'].extend(
            actions_navbar.pop('listing-wg-action', []))

    tounmerge = [
        'communication-action', 'wg-action',
        'primary-action', 'communication-body-action',
        'access-action', 'support-action']
    tounmerge = args.get('tounmerge', tounmerge)
    tomerge = [d for d in descriminators
               if d not in tounmerge and d in actions_navbar]
    for descriminator in tomerge:
        actions_navbar['actions'].extend(
            actions_navbar.pop(descriminator, []))

    communication_actions_bodies = []
    for action in actions_navbar.get(
            'communication-body-action', []):
        object_values = {
            'action': action,
            'context': context,
            'request': request,
            'ajax_actions': dict(actions_navbar['ajax-action']['actions'])}
        body = renderers.render(
            action.template, object_values, request)
        communication_actions_bodies.append(body)

    return {'isactive': actions_navbar['ajax-action']['isactive'],
            'messages': actions_navbar['ajax-action']['messages'],
            'resources': actions_navbar['ajax-action']['resources'],
            'all_actions': actions_navbar,
            'context_actions': actions_navbar['all_actions'],
            'footer_actions_body': communication_actions_bodies,
            'menu_body': render_navbar_body(
                request, context, actions_navbar,
                args.get('template', DEFAUL_LISTING_ACTIONS_TEMPLATE),
                ['actions'], view_type=view_type),
            'primary_menu_body': render_navbar_body(
                request, context, actions_navbar,
                args.get('primary_template', DEFAUL_LISTING_PRIMARY_ACTIONS_TEMPLATE),
                ['primary-action'], view_type=view_type),
            'footer_body':  render_navbar_body(
                request, context, actions_navbar,
                args.get('footer_template',
                         DEFAUL_LISTING_FOOTER_ACTIONS_TEMPLATE),
                ['communication-action'], view_type=view_type)
            if 'communication-action' in actions_navbar else None,
            'access_body':  render_navbar_body(
                request, context, actions_navbar,
                args.get('access_template',
                         DEFAUL_ACCESS_LISTING_ACTIONS_TEMPLATE),
                ['access-action'], view_type=view_type)
            if 'access-action' in actions_navbar else None,
            'wg_body':  render_navbar_body(
                request, context, actions_navbar,
                args.get('wg_template', DEFAUL_WG_LISTING_ACTIONS_TEMPLATE),
                ['wg-action'], view_type=view_type)
            if 'wg-action' in actions_navbar else None,
            'support_actions_body': render_navbar_body(
                request, context, actions_navbar,
                DEFAULT_SUPPORT_TEMPLATE,
                ['support-action'], view_type=view_type)
            if 'support-action' in actions_navbar else None,
            }


def render_files(files, request, template=FILE_TEMPLATE, navbar=False):
    bodies = []
    for file_ in files:
        navbars = {}
        if navbar:
            try:
                navbars = generate_listing_menu(
                    request, file_,
                    template=DEFAUL_LISTING_ACTIONS_TEMPLATE,)
            except ObjectRemovedException:
                pass

        extension = guess_extension(file_)
        object_values = {
            'extension': extension,
            'file': file_,
            'primary_menu_body': navbars.get('primary_menu_body', None),
            'menu_body': navbars.get('menu_body', None)
        }
        bodies.append(renderers.render(
            template,
            object_values,
            request))

    return bodies


def render_files_slider(slider_id, files, request, deferred=False, template=FILES_SLIDER_TEMPLATE):
    return renderers.render(
        template,
        {
            'files_data': get_files_data(files),
            'id': slider_id,
            'deferred': deferred,
            'json': json
        },
        request)


def get_vote_actions(
    context, request, ballot_ids=[],
    process_discriminator='Vote process'):
    dace_ui_api = get_current_registry().getUtility(
        IDaceUIAPI, 'dace_ui_api')
    vote_actions = dace_ui_api.get_actions(
        [context], request,
        process_discriminator=process_discriminator)
    if ballot_ids:
        vote_actions = [(va_context, va) for (va_context, va) in vote_actions
                        if getattr(va.process.ballot, 'group', {}).get('group_id', None) in
                        ballot_ids]

    action_updated, messages, \
        resources, actions = dace_ui_api.update_actions(
            request, vote_actions, True, True, False)
    for action in list(actions):
        action['body'], action_resources = dace_ui_api.get_action_body(
            context, request, action['action'],
            True, False, True)
        if not action['body']:
            actions.remove(action)

    return actions, resources, messages, action_updated


def get_vote_actions_body(
    context, request,
    ballot_ids=[],
    process_discriminator='Vote process'):
    actions, resources, messages, action_updated = get_vote_actions(
        context, request, ballot_ids, process_discriminator)
    avions_by_ballot = {}
    groups = {}
    for action in actions:
        ballot = getattr(
            getattr(action['action'], 'process', None),
            'ballot', None)
        if ballot:
            ballot_group = getattr(ballot, 'group', DEFAULT_BALLOT_GROUP)
            group_id = ballot_group.get('group_id')
            groups.setdefault(group_id, ballot_group)
            avions_by_ballot.setdefault(group_id, [])
            avions_by_ballot[group_id].append(action)

    bodies = ''
    activators = []
    oid = str(get_oid(context))
    for group_id, ballot_actions in avions_by_ballot.items():
        ballot_group = groups[group_id]
        group_title = ballot_group.get('group_title')
        group_activate = ballot_group.get('group_activate')
        body = renderers.render(
            VOTE_TEMPLATE,
            {
                'vote_actions': ballot_actions,
                'group_id': group_id+'_'+oid,
                'activate': group_activate,
                'context': context,
                'title': group_title,
                'json': json
            },
            request)
        bodies += body
        activators.append({
            'title': ballot_group.get('group_activator_title'),
            'action_id': group_id+'_'+oid,
            'class_css': ballot_group.get(
                'group_activator_class_css'),
            'style_picto': ballot_group.get(
                'group_activator_style_picto'),
            'order': ballot_group.get('group_activator_order')
        })

    activators = sorted(activators, key=lambda e: e['order'])
    return {
        'body': bodies,
        'activators': activators,
        'actions': actions,
        'resources': resources,
        'messages': messages,
        'isactive': action_updated
    }


def get_emoji_form(
    request, template=EMOJI_TEMPLATE, emoji_class='',
    groups=DEFAULT_EMOJIS, items=[], selected_items=[],
    is_grouped=True, add_preview=True):
    return renderers.render(
        template,
        {'is_grouped': is_grouped,
         'add_preview': add_preview,
         'emoji_class': emoji_class,
         'groups': groups,
         'items': items,
         'selected_items': selected_items},
        request)


def diff_analytics(context, version, attrs):
    ins_ = 0
    del_ = 0
    diff = 0
    for attr in attrs:
        soup, diff_text = html_diff_wrapper.render_html_diff(
            getattr(context, attr, ''),
            getattr(version, attr, ''),
            "analytics_diff")
        ins_ += len(soup.find_all('ins'))
        del_ += len(soup.find_all('del'))
        diff += len(soup.find_all('span', {'id': "analytics_diff"}))

    return {
        'diff': diff,
        'ins': ins_,
        'del': del_
    }


def get_action_view(process_id, action_id, request):
    root = getSite()
    actions = getBusinessAction(root, request, process_id, action_id)
    action = None
    action_view = None
    if actions is not None:
        action = actions[0]
        if action.__class__ in DEFAULTMAPPING_ACTIONS_VIEWS:
            action_view = DEFAULTMAPPING_ACTIONS_VIEWS[action.__class__]

    return action, action_view


def get_home_actions_bodies(process_id, action_id, form_id, request, context):
    result = {
        'form': None,
        'action': None,
        'css_links': [],
        'js_links': []}

    resources = deepcopy(getattr(
        request, 'resources', {'js_links': [], 'css_links': []}))
    add_content_action, add_content_view = get_action_view(
        process_id, action_id, request)
    if add_content_view:
        add_content_view_instance = add_content_view(
            context, request, behaviors=[add_content_action])
        add_content_view_instance.setviewid(form_id)
        add_content_view_instance.is_home_form = True
        add_content_view_result = add_content_view_instance()
        add_content_body = ''
        if isinstance(add_content_view_result, dict) and \
           'coordinates' in add_content_view_result:
            add_content_body = add_content_view_result['coordinates'][add_content_view_instance.coordinates][0]['body']
            result['css_links'] = [c for c in add_content_view_result.get('css_links', [])
                                   if c not in resources['css_links']]
            result['js_links'] = [c for c in add_content_view_result.get('js_links', [])
                                  if c not in resources['js_links']]

        update_resources(request, result)
        result['form'] = add_content_body
        result['action'] = add_content_action

    return result


def update(source, values):
    """Recursive dict update"""
    for k, v in values.items():
        if k in source:
            if isinstance(source[k], dict) and isinstance(v, collections.Mapping):
                update(source[k], v)
            else:
                source[k] = v

    return source
#add unrecognized mimetype

add_mimetype_map('audio/mp3', 'mp3')
