# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import datetime
import pytz
import string
import random
import unicodedata
import urllib
import io
import re
import metadata_parser
from urllib.parse import urlparse
from itertools import groupby
from persistent.dict import PersistentDict
from persistent.list import PersistentList
from pyramid import renderers
from babel.core import Locale
from bs4 import BeautifulSoup
from pyramid.threadlocal import get_current_registry, get_current_request

from substanced.util import get_oid

from pontus.file import OBJECT_OID
from pontus.util import merge_dicts
from dace.processinstance.activity import ActionType
from dace.objectofcollaboration.principal.util import get_current
from dace.util import getSite, getAllBusinessAction
from daceui.interfaces import IDaceUIAPI

from .ical_date_utility import getDatesFromString, set_recurrence
from novaideo.content.correlation import Correlation, CorrelationType
from novaideo.content.processes import get_states_mapping
from novaideo.file import Image
from novaideo.core import _
from novaideo.fr_stopdict import _words
from novaideo.core import Node
from novaideo.emojis import DEFAULT_EMOJIS


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


def get_url_domain(url, name_only=False):
    parsed_uri = urlparse(url)
    if not name_only:
        return '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    
    return '{uri.netloc}'.format(uri=parsed_uri)


def extract_twitter_metadata(page):
    result = {}
    soup = BeautifulSoup(page, "lxml")
    twit = soup.find('div', attrs={'class': 'permalink-header'})
    if twit:
        img = twit.find('img', attrs={'class': 'avatar'})
        if img:
            result = {'author_avatar': img['src']}

        username = twit.find('span', attrs={'class': 'username'})
        if username:
            name = username.find('b')
            if name:
                result['author_name'] = '@'+name.text

    return result


def extract_favicon(page, domain):
    result = {}
    soup = BeautifulSoup(page, "lxml")
    links = {
        'href': re.compile("\.ico"),
        'rel': "icon",
        'type': "image/x-icon"
    }
    favicon = None
    for link, value in links.items():
        try:
            favicon = soup.head.find(
                'link', **{link: value})
            if favicon:
                break
        except Exception as error:
            pass

    if favicon:
        href = favicon['href']
        domain_href = get_url_domain(href, True)
        if not domain_href:
            href = domain + href

        result = {'favicon': href}

    return result


DATA_EXTRACTORS = {
    'twitter': extract_twitter_metadata
}


def extract_urls_metadata(urls, save_images=False):
    results = []
    for url in urls:
        page = ''
        try:
            page = urllib.request.urlopen(url).read()
            url_metadata = metadata_parser.MetadataParser(
                html=page, requests_timeout=100)
        except Exception:
            continue
        result = {
            'url': url,
            'title': url_metadata.get_metadata('title'),
            'description': url_metadata.get_metadata('description'),
            'site_name': url_metadata.get_metadata('site_name'),
            'image_url': None,
            'image': None
        }
        if not result.get('site_name'):
            result['site_name'] = get_url_domain(
                url, True).replace('www.', '').replace('.', '-')

        if result['site_name']:
            extractor = DATA_EXTRACTORS.get(result['site_name'].lower(), None)
            if extractor:
                result.update(extractor(page))

        result.update(extract_favicon(page, get_url_domain(url)))
        try:
            image = url_metadata.get_metadata('image')
            if save_images and image:
                buf = io.BytesIO(urllib.request.urlopen(
                    image).read())
                buf.seek(0)
                newimg = Image(fp=buf)
                result['image'] = newimg
            elif image:
                result['image_url'] = image

        except Exception:
            continue

        results.append(result)

    return results


#source: http://dinoblog.tuxfamily.org/?p=40

def factorielle(x):
    if x < 2:
        return 1
    else:
        return x * factorielle(x - 1)


def combinaisons(L, N, k):
    h = 0
    i = 0
    j = 0

    n = [0] * (N - 1)

    G = []
    s = ""

    if len(L) < N:
        return G
    elif N == 1:
        return L
    elif len(L) == N:
        while i < len(L):
            s = s + L[i]
            i = i + 1

        G.append(s)
    elif len(L) > N:
        l = factorielle(len(L) - 1)/(factorielle(N - 1)
             * factorielle((len(L) - 1) - (N - 1)));

        while i < l:
            s = L[len(L) - 1]

            while h < len(n):
                if j > 0 and j < len(n):
                    n[j] = n[j - 1] + 1

                s = s + L[n[h]]
                h = h + 1
                j = j + 1

            G.append(s)

            h = 0
            j = 0

            while j < len(n) and n[j] != j + k:
                j = j + 1

            if j > 0:
                n[j - 1] = n[j - 1] + 1

            i = i + 1

        L.pop()
        G = G + combinaisons(L, N, k - 1)

    return G

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
    return ((len(list(group)), word) for word, group in groupby(sorted_words))


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
        oid = obj.get_node_id()
        if isinstance(obj, Node) and oid not in calculated:
            graph, calculated = obj.init_graph(calculated)


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

ALL_DESCRIMINATORS = ['global-action',
                      'text-action',
                      'lateral-action',
                      'primary-action',
                      'listing-primary-action',
                      'admin-action',
                      'wg-action',
                      'plus-action',
                      'body-action',
                      'communication-action',
                      'communication-body-action']

DEFAUL_LISTING_FOOTER_ACTIONS_TEMPLATE = 'novaideo:views/templates/listing_footer_actions.pt'

DEFAUL_WG_LISTING_ACTIONS_TEMPLATE = 'novaideo:views/templates/wg_listing_actions.pt'

DEFAUL_LISTING_ACTIONS_TEMPLATE = 'novaideo:views/templates/listing_object_actions.pt'

DEFAUL_NAVBAR_TEMPLATE = 'novaideo:views/templates/navbar_actions.pt'

FOOTER_NAVBAR_TEMPLATE = 'novaideo:views/templates/footer_navbar_actions.pt'

DEFAULT_MENU_TEMPLATE = 'novaideo:views/templates/navbar_actions.pt'

FOOTER_BLOCK_TEMPLATE = 'novaideo:views/templates/footer_entity_actions.pt'

EMOJI_TEMPLATE = 'novaideo:views/templates/emoji_selector.pt'


def render_small_listing_objs(request, objs, user, **kw):
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


def render_listing_objs(request, objs, user, **kw):
    result_body = []
    resources = {'css_links': [], 'js_links': []}
    for obj in objs:
        try:
            navbars = generate_listing_menu(
                request, obj,
                template=DEFAUL_LISTING_ACTIONS_TEMPLATE,
                footer_template=DEFAUL_LISTING_FOOTER_ACTIONS_TEMPLATE,
                wg_template=DEFAUL_WG_LISTING_ACTIONS_TEMPLATE)
        except ObjectRemovedException:
            continue

        resources = merge_dicts(navbars['resources'], resources)
        object_values = {
            'object': obj,
            'current_user': user,
            'menu_body': navbars['menu_body'],
            'footer_body': navbars['footer_body'],
            'wg_body': navbars['wg_body'],
            'footer_actions_body': navbars['footer_actions_body'],
            'state': get_states_mapping(user, obj,
                getattr(obj, 'state_or_none', [None])[0])}
        object_values.update(kw)
        body = renderers.render(
            obj.templates.get('default'),
            object_values,
            request)
        result_body.append(body)

    return result_body, resources


def update_ajax_actions(actions, context, request):
    dace_ui_api = get_current_registry().getUtility(
        IDaceUIAPI, 'dace_ui_api')
    actions = [(context, a) for a in actions]
    action_updated, messages, \
    resources, actions = dace_ui_api.update_actions(
        request, actions)
    return action_updated, messages, resources, actions


def update_ajax_action(
    context, request,
    process_id, node_id):
    seemembers_actions = getBusinessAction(
        context, request,
        process_id, node_id)
    if seemembers_actions:
        isactive, messages, \
        resources, ajax_actions = update_ajax_actions(
            seemembers_actions, context, request)
        return ajax_actions, resources

    return [], {}


def update_all_ajax_action(
    context, request,
    node_id, process_id=None):
    seemembers_actions = getAllBusinessAction(
        context, request, node_id=node_id,
        process_id=process_id,
        process_discriminator='Application')
    if seemembers_actions:
        isactive, messages, \
        resources, ajax_actions = update_ajax_actions(
            seemembers_actions, context, request)
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
    result['ajax-action'] = {'isactive': isactive,
                              'messages': messages,
                              'resources': resources,
                              'actions': ajax_actions
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
               for key in keys if actions_navbar.get(key, [])}
    if actions:
        ajax_actions = actions_navbar['ajax-action']['actions']
        template = template if template else DEFAUL_NAVBAR_TEMPLATE
        actions['ajax_actions'] = dict(ajax_actions)
        actions['obj'] = context
        return renderers.render(template, actions, request)

    return None


class ObjectRemovedException(Exception):
    pass


def generate_navbars(request, context, **args):
    def actions_getter():
        return getAllBusinessAction(
            context, request, process_discriminator='Application')

    actions_navbar = get_actions_navbar(
        actions_getter, context, request, list(ALL_DESCRIMINATORS))
    if getattr(context, '__parent__', None) is None:
        raise ObjectRemovedException("Object removed")

    actions_navbar['global-action'].extend(
        actions_navbar.pop('admin-action'))
    actions_navbar['global-action'].extend(
        args.get('global_action', []))
    actions_navbar['global-action'].extend(
        actions_navbar.pop('primary-action'))
    actions_navbar['text-action'].extend(
        args.get('text_action', []))
    actions_navbar['plus-action'].extend(
        actions_navbar.pop('listing-primary-action'))
    actions_navbar['plus-action'].extend(
        args.get('plus_action', []))
    actions_navbar['body-action'].extend(
        args.get('body_action', []))
    actions_navbar['communication-body-action'].extend(
        args.get('communication-body-action', []))

    actions_bodies = []
    for action in actions_navbar['body-action']:
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
            'footer_actions_body': communication_actions_bodies,
            'navbar_body': render_navbar_body(
                request, context, actions_navbar, args.get('template', None)),
            'footer_body': render_navbar_body(
                request, context, actions_navbar,
                DEFAUL_LISTING_FOOTER_ACTIONS_TEMPLATE, ['communication-action'])
                if 'communication-action' in actions_navbar else None,
            }


def generate_listing_menu(request, context, **args):
    def actions_getter():
        return getAllBusinessAction(
            context, request, process_discriminator='Application')

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
    if 'primary-action' in actions_navbar:
        actions_navbar['primary-action'].extend(
            actions_navbar.pop('listing-primary-action'))

    tounmerge = [
        'communication-action', 'wg-action', 'primary-action',
        'communication-body-action']
    tomerge = [d for d in descriminators
               if d not in tounmerge and d in actions_navbar]
    for descriminator in tomerge:
        actions_navbar['actions'].extend(
            actions_navbar.pop(descriminator))

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
            'footer_actions_body': communication_actions_bodies,
            'menu_body': render_navbar_body(
                request, context, actions_navbar,
                args.get('template', None), ['actions', 'primary-action']),
            'footer_body':  render_navbar_body(
                request, context, actions_navbar,
                args.get('footer_template', None), ['communication-action'])
            if 'communication-action' in actions_navbar else None,
            'wg_body':  render_navbar_body(
                request, context, actions_navbar,
                args.get('wg_template', None), ['wg-action'])
            if 'wg-action' in actions_navbar else None
            }


def get_emoji_form(
    request, template=EMOJI_TEMPLATE, emoji_class='',
    groups=DEFAULT_EMOJIS, items=[], is_grouped=True, add_preview=True):
    return renderers.render(
        template,
        {'is_grouped': is_grouped,
         'add_preview': add_preview,
         'emoji_class': emoji_class,
         'groups': groups,
         'items': items},
        request)
