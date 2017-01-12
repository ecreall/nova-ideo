# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import re
import deform
import colander
from zope.interface import invariant

from pontus.schema import Schema
from pontus.widget import TextInputWidget

from novaideo import _

from novaideo.views.widget import EmailInputWidget


PHONE_PATTERN = re.compile(r'^(0|\+([0-9]{2,3})[-. ]?|00([0-9]{2,3})[-. ]?)[1-9]?([-. ]?([0-9]{2})){4}$')


@colander.deferred
def phone_fax_validator(node, kw):
    if not PHONE_PATTERN.match(kw):
        raise colander.Invalid(node,
                _('${phone} phone number not valid',
                  mapping={'phone': kw}))


@colander.deferred
def default_title(node, kw):
    request = node.bindings['request']
    return request.localizer.translate(_('Administration service'))


class ContactSchema(Schema):

    title = colander.SchemaNode(
        colander.String(),
        title=_('Title', context='contact'),
        default=default_title
        )

    address = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.TextAreaWidget(rows=4, cols=60),
        title=_('Address'),
        missing=""
        )

    email = colander.SchemaNode(
        colander.String(),
        widget=EmailInputWidget(),
        missing="",
        validator=colander.All(
            colander.Email(),
            colander.Length(max=100)
            ),
        )

    phone = colander.SchemaNode(
        colander.String(),
        validator=colander.All(phone_fax_validator),
        missing="",
        widget=TextInputWidget(css_class="contact-phone"),
        title=_('Phone'),
        )

    surtax = colander.SchemaNode(
        colander.String(),
        missing="0",
        widget=TextInputWidget(item_css_class="hide-bloc"),
        default="0",
        title=_('Surcharge'),
        description=_('Indicate the amount of the surcharge (for the premium-rate number).'),
        )

    fax = colander.SchemaNode(
        colander.String(),
        missing="",
        title=_('Fax'),
        )

    website = colander.SchemaNode(
        colander.String(),
        missing="",
        title=_('Website'),
        )

    @invariant
    def contact_invariant(self, appstruct):
        appstruct_copy = appstruct.copy()
        appstruct_copy.pop('surtax')
        if 'title' in appstruct_copy:
            appstruct_copy.pop('title')

        if not any(v != "" and v != colander.null
                   for v in list(appstruct_copy.values())):
            raise colander.Invalid(self,
                                   _('One value must be entered.'))

        if 'phone' in appstruct and appstruct['phone'] and \
            ('surtax' not in appstruct or \
             'surtax' in appstruct and not appstruct['surtax']):
            raise colander.Invalid(self,
                                   _('Surcharge field must be filled in.'))
