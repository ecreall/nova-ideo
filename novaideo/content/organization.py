# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import colander
from zope.interface import implementer

from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer

from dace.util import get_obj
from dace.objectofcollaboration.principal.util import get_users_with_role
from dace.objectofcollaboration.entity import Entity
from dace.descriptors import SharedMultipleProperty, CompositeUniqueProperty
from pontus.core import VisualisableElement, VisualisableElementSchema
from pontus.widget import (
    AjaxSelect2Widget, SimpleMappingWidget, SequenceWidget)
from pontus.file import Image, ObjectData
from pontus.schema import omit, select

from novaideo.core_schema import ContactSchema
from .interface import IOrganization
from novaideo import _
from novaideo.content import get_file_widget


@colander.deferred
def members_choice(node, kw):
    """"""
    context = node.bindings['context']
    request = node.bindings['request']
    values = []

    def title_getter(oid):
        author = None
        try:
            author = get_obj(int(oid))
        except Exception:
            return oid

        title = getattr(author, 'title', author.__name__)
        return title

    ajax_url = request.resource_url(context,
                                    '@@novaideoapi',
                                    query={'op': 'find_user'})
    return AjaxSelect2Widget(
        values=values,
        ajax_url=ajax_url,
        multiple=True,
        title_getter=title_getter)


def context_is_a_organization(context, request):
    return request.registry.content.istype(context, 'organization')


class OrganizationSchema(VisualisableElementSchema):
    """Schema for Organization"""

    name = NameSchemaNode(
        editing=context_is_a_organization,
        )

    logo = colander.SchemaNode(
        ObjectData(Image),
        widget=get_file_widget(),
        required=False,
        missing=None,
        title=_('Logo'),
        )

    contacts = colander.SchemaNode(
        colander.Sequence(),
        omit(select(ContactSchema(name='contact',
                                  widget=SimpleMappingWidget(
                                  css_class='contact-well object-well default-well')),
                    ['title', 'address', 'phone', 'surtax', 'email', 'website', 'fax']),
            ['_csrf_token_']),
        widget=SequenceWidget(
            min_len=1,
            add_subitem_text_template=_('Add a new contact')),
        title='Contacts',
        oid='contacts'
        )

    members = colander.SchemaNode(
        colander.Set(),
        widget=members_choice,
        title=_('Members'),
        )

    managers = colander.SchemaNode(
        colander.Set(),
        widget=members_choice,
        title=_('Managers'),
        )


@content(
    'organization',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IOrganization)
class Organization(VisualisableElement, Entity):
    """Organization class"""

    templates = {
        'default': 'novaideo:views/templates/organization_result.pt'
    }
    icon = 'glyphicon glyphicon-home'
    name = renamer()
    members = SharedMultipleProperty('members', 'organization')
    logo = CompositeUniqueProperty('logo')

    def __init__(self, **kwargs):
        super(Organization, self).__init__(**kwargs)
        self.set_data(kwargs)

    @property
    def managers(self):
        return get_users_with_role(role=('OrganizationResponsible', self))
