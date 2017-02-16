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
from dace.objectofcollaboration.entity import Entity
from dace.objectofcollaboration.principal import Group
from dace.descriptors import SharedMultipleProperty, CompositeUniqueProperty
from dace.objectofcollaboration.principal.util import (
    get_users_with_role, grant_roles, revoke_roles)

from pontus.core import VisualisableElement, VisualisableElementSchema
from pontus.widget import (
    AjaxSelect2Widget, SimpleMappingWidget, SequenceWidget)
from pontus.file import Image, ObjectData
from pontus.schema import omit, select

from novaideo.core_schema import ContactSchema
from .interface import IOrganization
from novaideo import _
from novaideo.content import get_file_widget


def managers():
    """Return a property. The getter of the property returns the
    ``_tree`` attribute of the instance on which it's defined. The setter
    of the property calls ``synchronize_tree()``.

      class SomeContentType(Persistent):
          tree = synchronize_tree()
    """
    def _get(self):
        return get_users_with_role(role=('OrganizationResponsible', self))

    def _set(self, new_managers):
        old_managers = self.managers
        managers_toadd = [u for u in new_managers
                          if u not in old_managers]
        managers_todel = [u for u in old_managers
                          if u not in new_managers]

        for manager in managers_todel:
            revoke_roles(manager, (('OrganizationResponsible',
                                    self),))

        for manager in managers_toadd:
            for current_org in manager.managed_organization:
                revoke_roles(manager, (('OrganizationResponsible',
                             current_org),))

            grant_roles(user=manager,
                        roles=(('OrganizationResponsible',
                                self),))

    return property(_get, _set)


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


@colander.deferred
def managers_choice(node, kw):
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
                                    query={'op': 'find_organization_user'})
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
        missing=[]
        )

    managers = colander.SchemaNode(
        colander.Set(),
        widget=managers_choice,
        title=_('The managers'),
        missing=[]
        )


@content(
    'organization',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IOrganization)
class Organization(VisualisableElement, Group):
    """Organization class"""

    templates = {
        'default': 'novaideo:views/templates/organization_result.pt',
        'popover': 'novaideo:views/templates/organization_popover.pt',
        'small': 'novaideo:views/templates/small_organization_result.pt'
    }
    icon = 'glyphicon glyphicon-home'
    name = renamer()
    managers = managers()
    members = SharedMultipleProperty('members', 'organization')
    logo = CompositeUniqueProperty('logo')

    def __init__(self, **kwargs):
        super(Organization, self).__init__(**kwargs)
        self.set_data(kwargs)
