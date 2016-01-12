# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import colander
import datetime
import pytz
from PIL import Image
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from pontus.view import BasicView
from dace.objectofcollaboration.entity import Entity
from dace.util import get_obj, find_catalog

from novaideo.ips.hexagonit.swfheader import parse
from novaideo import _
from novaideo.core import advertising_banner_config
from novaideo.views.filter import find_entities
from novaideo.content.interface import (
    IWebAdvertising)
from novaideo import log


def validate_file_content(node, appstruct, width, height):
    if appstruct['picture']:
        mimetype = appstruct['picture']['mimetype']
        file_value = getattr(appstruct['picture']['fp'], 'raw',
                             appstruct['picture']['fp'])
        if mimetype.startswith('image'):
            try:
                file_value.seek(0)
            except Exception as e:
                log.warning(e)

            img = Image.open(file_value)
            img_width = img.size[0]
            img_height = img.size[1]
            file_value.seek(0)
            if img_width > width or img_height > height:
                raise colander.Invalid(node, _
                    (_('The image size is not valid: the allowed size is ${width} x ${height} px.',
                         mapping={'width': width,
                                   'height': height})))

        if mimetype.startswith('application/x-shockwave-flash'):
            try:
                file_value.seek(0)
            except Exception as e:
                log.warning(e)

            header = parse(file_value)
            file_value.seek(0)
            flash_width = header['width']
            flash_height = header['height']
            if flash_width > width or flash_height > height:
                raise colander.Invalid(node, _
                    (_('The flash animation size is not valid: the allowed size is ${width} x ${height} px.',
                         mapping={'width': width,
                                   'height': height})))


@view_config(
    name='banner_click',
    renderer='pontus:templates/views_templates/grid.pt',
    )
class BannerClick(BasicView):
    title = ''
    name = 'banner_click'
    viewid = 'banner_click'

    def update(self):
        ad_oid = self.params('ad_oid')
        if not ad_oid:
            return HTTPFound(self.request.resource_url(self.request.root, ''))

        advertisting = get_obj(int(ad_oid))
        if advertisting:
            setattr(advertisting, 'click',
                    (getattr(advertisting, 'click', 0)+1))
            url = getattr(advertisting, 'advertisting_url',
                   self.request.resource_url(self.request.root))
            return HTTPFound(url)

        return HTTPFound(self.request.resource_url(self.request.root, ''))


def default_validator(node, appstruct):
    return True


class AdvertistingBanner(object):

    title = _('Banner')
    description = _('Banner for announcements')
    tags = ['advertisting']
    name = 'banner'
    order = -1
    validator = default_validator

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def find_advertistings(self):
        #TODO frequence
        novaideo_catalog = find_catalog('novaideo')
        start_date = end_date = datetime.datetime.now()
        start_date = datetime.datetime.combine(
            start_date,
            datetime.time(0, 0, 0, tzinfo=pytz.UTC))
        end_date = datetime.datetime.combine(
            end_date,
            datetime.time(23, 59, 59, tzinfo=pytz.UTC))
        start_date_index = novaideo_catalog['publication_start_date']
        query = start_date_index.inrange_with_not_indexed(
            start_date, end_date)

        advertisings = find_entities(
            interfaces=[IWebAdvertising],
            metadata_filter={'states': ['published']},
            add_query=query)
        advertisings = [a for a in advertisings
                        if self.name in getattr(a, 'positions', [])]
        return advertisings

    def __call__(self):
        advertistings = self.find_advertistings()
        advertistings_data = [ad.get_content_data(self.request)
                              for ad in advertistings]
        return {'sources': advertistings_data}


@advertising_banner_config(
    name='advertisting_right_1',
    context=Entity,
    renderer='templates/panels/advertisting/advertisting_right_1.pt'
    )
class BannerRight1(AdvertistingBanner):

    title = _('First on the right')
    description = _('First on the right banner')
    name = 'advertisting_right_1'
    order = 2


@advertising_banner_config(
    name='advertisting_right_2',
    context=Entity,
    renderer='templates/panels/advertisting/advertisting_right_2.pt'
    )
class BannerRight2(AdvertistingBanner):

    title = _('Second on the right')
    description = _('Second on the right banner')
    name = 'advertisting_right_2'
    order = 3


@advertising_banner_config(
    name='advertisting_right_3',
    context=Entity,
    renderer='templates/panels/advertisting/advertisting_right_3.pt'
    )
class BannerRight3(AdvertistingBanner):

    title = _('Third on the right')
    description = _('Third on the right banner')
    name = 'advertisting_right_3'
    order = 4


@advertising_banner_config(
    name='advertisting_right_5',
    context=Entity,
    renderer='templates/panels/advertisting/advertisting_right_5.pt'
    )
class BannerRight5(AdvertistingBanner):

    title = _('Fourth on the right')
    description = _('Fourth on the right banner')
    name = 'advertisting_right_5'
    order = 5


@advertising_banner_config(
    name='advertisting_right_6',
    context=Entity,
    renderer='templates/panels/advertisting/advertisting_right_6.pt'
    )
class BannerRight6(AdvertistingBanner):

    title = _('Fifth on the right')
    description = _('Fifth on the right banner')
    name = 'advertisting_right_6'
    order = 6


@advertising_banner_config(
    name='advertisting_right_7',
    context=Entity,
    renderer='templates/panels/advertisting/advertisting_right_7.pt'
    )
class BannerRight7(AdvertistingBanner):

    title = _('Sixth on the right')
    description = _('Sixth on the right banner')
    name = 'advertisting_right_7'
    order = 7


@advertising_banner_config(
    name='advertisting_right_8',
    context=Entity,
    renderer='templates/panels/advertisting/advertisting_right_8.pt'
    )
class BannerRight8(AdvertistingBanner):

    title = _('Seventh on the right')
    description = _('Seventh on the right banner')
    name = 'advertisting_right_8'
    order = 8


@advertising_banner_config(
    name='advertisting_right_9',
    context=Entity,
    renderer='templates/panels/advertisting/advertisting_right_9.pt'
    )
class BannerRight9(AdvertistingBanner):

    title = _('Eighth on the right')
    description = _('Eighth on the right banner')
    name = 'advertisting_right_9'
    order = 9


@advertising_banner_config(
    name='advertisting_right_10',
    context=Entity,
    renderer='templates/panels/advertisting/advertisting_right_10.pt'
    )
class BannerRight10(AdvertistingBanner):

    title = _('Ninth on the right')
    description = _('Ninth on the right banner')
    name = 'advertisting_right_10'
    order = 10


@advertising_banner_config(
    name='advertisting_right_11',
    context=Entity,
    renderer='templates/panels/advertisting/advertisting_right_11.pt'
    )
class BannerRight11(AdvertistingBanner):

    title = _('Tenth on the right')
    description = _('Tenth on the right banner')
    name = 'advertisting_right_11'
    order = 11
