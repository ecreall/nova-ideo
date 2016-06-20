# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import colander
from zope.interface import implementer, invariant
from pyramid.threadlocal import get_current_request

from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer

from dace.descriptors import (
    SharedUniqueProperty,
    CompositeUniqueProperty)
from pontus.widget import (
    Select2Widget,
    RichTextWidget)
from pontus.file import ObjectData, File

from .interface import (
    IWebAdvertising,
    IAdvertising)
from novaideo import _
from novaideo.core import (
    SearchableEntitySchema,
    VisualisableElementSchema,
    SearchableEntity,
    ADVERTISING_CONTAINERS)
from novaideo.utilities import french_dates_parser as Parser
from novaideo.utilities.util import dates
from novaideo.views.widget import DateIcalWidget
from novaideo.content import get_file_widget


@colander.deferred
def dates_validator(node, kw):
    def _dates_validator(node, value):
        try:
            if Parser.getDatesFromSeances(value) is None:
                raise colander.Invalid(node, _('Not valid value'))
        except AttributeError as e:
            raise colander.Invalid(node, e.args[0])

    return _dates_validator


class AdvertisingSchema(VisualisableElementSchema, SearchableEntitySchema):
    """Schema for advertising"""

    visibility_dates = colander.SchemaNode(
        colander.String(),
        validator=dates_validator,
        widget=DateIcalWidget(),
        title=_('Dates'),
        )


@implementer(IAdvertising)
class Advertising(SearchableEntity):
    """Advertising class"""

    picture = CompositeUniqueProperty('picture')
    author = SharedUniqueProperty('author')
    visibility_dates = dates('visibility_dates')
    internal_type = True

    def __init__(self, **kwargs):
        super(Advertising, self).__init__(**kwargs)
        self.set_data(kwargs)


def context_is_a_webadvertising(context, request):
    return request.registry.content.istype(context, 'webadvertising')


@colander.deferred
def advertisting_widget(node, kw):
    values = [(ad_id, value['title'])
              for ad_id, value in ADVERTISING_CONTAINERS.items()
              if 'advertisting' in value['tags']]

    values = sorted(values,
                    key=lambda e: ADVERTISING_CONTAINERS[e[0]]['order'])
    return Select2Widget(
        css_class="advertising-positions",
        values=values,
        multiple=True)


class WebAdvertisingSchema(AdvertisingSchema):
    """Schema for Web advertising"""

    name = NameSchemaNode(
        editing=context_is_a_webadvertising,
        )

    picture = colander.SchemaNode(
        ObjectData(File),
        widget=get_file_widget(
            item_css_class="advertising-file-content",
            css_class="file-content",
            file_type=['image', 'flash']),
        title=_('Announcement file'),
        description=_("Only image and flash files are supported."),
        missing=None
        )

    html_content = colander.SchemaNode(
        colander.String(),
        widget=RichTextWidget(item_css_class="advertising-html-content",
                              css_class="html-content-text"),
        title=_("Or HTML content"),
        missing=""
        )

    advertisting_url = colander.SchemaNode(
        colander.String(),
        title=_('URL'),
        missing="#"
        )

    positions = colander.SchemaNode(
        colander.Set(),
        widget=advertisting_widget,
        title=_('Positions')
        )

    @invariant
    def content_invariant(self, appstruct):
        if not(appstruct['html_content'] or appstruct['picture']):
            raise colander.Invalid(self, _
                        ('Content will be defined.'))

    @invariant
    def banner_invariant(self, appstruct):
        positions = appstruct['positions']
        if positions:
            for position in positions:
                ADVERTISING_CONTAINERS[position]['validator'](
                    self.get('picture'),
                    appstruct)


@content(
    'webadvertising',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IWebAdvertising)
class WebAdvertising(Advertising):
    """WebAdvertising class"""

    type_title = _('Announcement')
    icon = 'glyphicon glyphicon-picture'
    templates = {'default': 'novaideo:views/templates/web_advertisting_result.pt',
                 'bloc': 'novaideo:views/templates/web_advertisting_result.pt'}
    name = renamer()

    def __init__(self, **kwargs):
        self.click = 0
        super(WebAdvertising, self).__init__(**kwargs)

    def _extract_content(self):
        if self.picture:
            if self.picture.mimetype.startswith('image'):
                return {'content': self.picture.url,
                        'type': 'img'}

            if self.picture.mimetype.startswith(
                           'application/x-shockwave-flash'):
                return {'content': self.picture.url,
                        'type': 'flash'}

            if self.picture.mimetype.startswith('text/html'):
                blob = self.picture.blob.open()
                blob.seek(0)
                content = blob.read().decode("utf-8")
                blob.seek(0)
                blob.close()
                return {'content': content,
                        'type': 'html'}

        html_content = getattr(self, 'html_content', '')
        if html_content:
            return {'content': html_content,
                    'type': 'html'}

        return {'content': '',
                'type': 'none'}

    def get_positions(self):
        return [ADVERTISING_CONTAINERS[p]['title']
                for p in self.positions]

    def get_content_data(self, request=None):
        if request is None:
            request = get_current_request()

        root = request.root
        data = {'url': request.resource_url(
                root,
                'banner_click',
                query={'ad_oid': getattr(self, '__oid__', 0)}),
                }

        data.update(self._extract_content())
        return data
