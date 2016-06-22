# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi
# -*- coding: utf8 -*-
import os
import datetime
import pytz
import colander
import deform.widget
from persistent.list import PersistentList
from zope.interface import implementer

from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer
from substanced.principal import UserSchema
from substanced.interfaces import IUserLocator
from substanced.principal import DefaultUserLocator

from dace.util import getSite
from dace.objectofcollaboration.entity import Entity
from dace.objectofcollaboration.principal import User
from dace.descriptors import (
    SharedUniqueProperty,
    CompositeMultipleProperty,
    CompositeUniqueProperty,
    SharedMultipleProperty)
from dace.objectofcollaboration.principal.util import (
    get_objects_with_role, has_role, revoke_roles)
from pontus.core import VisualisableElement, VisualisableElementSchema
from pontus.widget import (
    ImageWidget,
    Select2Widget
    )
from pontus.form import FileUploadTempStore
from pontus.file import ObjectData, Object as ObjectType

from novaideo.core import (
    SearchableEntity,
    SearchableEntitySchema,
    keywords_choice,
    CorrelableEntity,
    generate_access_keys)
from .interface import IPerson, IPreregistration
from novaideo import _
from novaideo.file import Image
from novaideo.views.widget import TOUCheckboxWidget, LimitedTextAreaWidget


DEADLINE_PREREGISTRATION = 86400*2  # 2 days

DEFAULT_LOCALE = 'fr'


@colander.deferred
def organization_choice(node, kw):
    context = node.bindings['context']
    values = []
    root = getSite()
    if root is None:
        root = context.__parent__.__parent__

    prop = sorted(root.organizations, key=lambda p: p.title)
    values = [(i, i.title) for i in prop]
    values.insert(0, ('', _('- Select -')))
    return Select2Widget(values=values)


@colander.deferred
def titles_choice(node, kw):
    root = getSite()
    values = [(str(i),  i) for i in root.titles]
    values.insert(0, ('', _('- Select -')))
    return Select2Widget(values=values)


@colander.deferred
def email_validator(node, kw):
    context = node.bindings['context']
    request = node.bindings['request']
    root = getSite()
    adapter = request.registry.queryMultiAdapter(
        (context, request),
        IUserLocator
        )
    if adapter is None:
        adapter = DefaultUserLocator(context, request)
    user = adapter.get_user_by_email(kw)
    if user is context:
        user = None

    invitation = None
    for invit in root.invitations:
        if invit.email == kw and not (context is invit):
            invitation = invit
            break

    if user is not None or invitation is not None:
        raise colander.Invalid(node,
                _('${email} email address already in use',
                  mapping={'email': kw}))

@colander.deferred
def default_contacts(node, kw):
    context = node.bindings['context']
    prop = sorted(context.contacts, key=lambda p: p.name)
    return prop


def get_locales():
    dir_ = os.listdir(os.path.join(os.path.dirname(__file__),
                                   '..', 'locale'))
    return list(filter(lambda x: not x.endswith('.pot'), dir_)) + ['en']


_LOCALES = get_locales()


_LOCALES_TITLES = {'en': 'English',
                   'fr': 'Français'}


@colander.deferred
def locale_widget(node, kw):
    locales = [(l, _LOCALES_TITLES.get(l, l)) for l in _LOCALES]
    sorted_locales = sorted(locales)
    return Select2Widget(values=sorted_locales)


@colander.deferred
def locale_missing(node, kw):
    return kw['request'].locale_name


@colander.deferred
def conditions_widget(node, kw):
    root = getSite()
    terms_of_use = root.get('terms_of_use')
    return TOUCheckboxWidget(tou_file=terms_of_use)


@colander.deferred
def picture_widget(node, kw):
    context = node.bindings['context']
    request = node.bindings['request']
    root = getSite()
    tmpstore = FileUploadTempStore(request)
    source = None
    if context is not root:
        if context.picture:
            source = context.picture

    return ImageWidget(
        tmpstore=tmpstore,
        # max_height=500,
        # max_width=400,
        source=source,
        selection_message=_("Upload image.")
        )


def context_is_a_person(context, request):
    return request.registry.content.istype(context, 'person')


class PersonSchema(VisualisableElementSchema, UserSchema, SearchableEntitySchema):
    """Schema for Person"""

    name = NameSchemaNode(
        editing=context_is_a_person,
        )

    function = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.TextInputWidget(),
        title=_('Function'),
        missing=''
    )

    description = colander.SchemaNode(
        colander.String(),
        widget=LimitedTextAreaWidget(
            rows=5,
            cols=30,
            limit=1200,
            alert_values={'limit': 1200}),
        title=_("Description"),
        missing=""
    )

    keywords = colander.SchemaNode(
        colander.Set(),
        widget=keywords_choice,
        title=_('Preferences'),
        missing=[]
        )

    email = colander.SchemaNode(
        colander.String(),
        validator=colander.All(
            colander.Email(),
            email_validator,
            colander.Length(max=100)
            ),
        title=_('Login (email)')
        )

    picture = colander.SchemaNode(
        ObjectData(Image),
        widget=picture_widget,
        title=_('Picture'),
        description=_('You see a square on the top left of the image if it exceeds the maximum'
                      ' size allowed. Move and enlarge it if necessary, to determine an area of'
                      ' interest. Several images will be generated from this area.'),
        required=False,
        missing=None,
        )

    first_name = colander.SchemaNode(
        colander.String(),
        title=_('First name'),
        )

    last_name = colander.SchemaNode(
        colander.String(),
        title=_('Last name'),
        )

    user_title = colander.SchemaNode(
        colander.String(),
        widget=titles_choice,
        title=_('Title', context='user'),
        )

    locale = colander.SchemaNode(
        colander.String(),
        title=_('Locale'),
        widget=locale_widget,
        missing=locale_missing,
        validator=colander.OneOf(_LOCALES),
    )

    password = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.CheckedPasswordWidget(),
        validator=colander.Length(min=3, max=100),
        title=_("Password")
        )

    organization = colander.SchemaNode(
        ObjectType(),
        widget=organization_choice,
        missing=None,
        title=_('Organization'),
        )

    accept_conditions = colander.SchemaNode(
        colander.Boolean(),
        widget=conditions_widget,
        label=_('I have read and accept the terms and conditions'),
        title='',
        missing=False
    )


@content(
    'person',
    icon='icon glyphicon glyphicon-user',
    )
@implementer(IPerson)
class Person(User, SearchableEntity, CorrelableEntity):
    """Person class"""

    type_title = _('Person')
    icon = 'icon glyphicon glyphicon-user' #'icon novaideo-icon icon-user'
    templates = {'default': 'novaideo:views/templates/person_result.pt',
                 'bloc': 'novaideo:views/templates/person_result.pt',
                 'small': 'novaideo:views/templates/small_person_result.pt'}
    name = renamer()
    tokens = CompositeMultipleProperty('tokens')
    tokens_ref = SharedMultipleProperty('tokens_ref')
    organization = SharedUniqueProperty('organization', 'members')
    picture = CompositeUniqueProperty('picture')
    ideas = SharedMultipleProperty('ideas', 'author')
    selections = SharedMultipleProperty('selections')
    working_groups = SharedMultipleProperty('working_groups', 'members')
    alerts = SharedMultipleProperty('alerts', 'users_to_alert')
    old_alerts = SharedMultipleProperty('old_alerts', 'alerted_users')
    following_channels = SharedMultipleProperty('following_channels', 'members')

    def __init__(self, **kwargs):
        if 'locale' not in kwargs:
            kwargs['locale'] = DEFAULT_LOCALE

        super(Person, self).__init__(**kwargs)
        kwargs.pop('password')
        self.set_data(kwargs)
        self.set_title()
        self.last_connection = datetime.datetime.now(tz=pytz.UTC)

    def get_channel(self, user):
        all_channels = list(self.channels)
        all_channels.extend(list(getattr(user, 'channels', [])))
        for channel in all_channels:
            if user in channel.members and self in channel.members:
                return channel

        return None

    def addtoproperty(self, name, value, moving=None):
        super(Person, self).addtoproperty(name, value, moving)
        if name == 'selections':
            value.len_selections = getattr(value, 'len_selections', 0)
            value.len_selections += 1

    def delfromproperty(self, name, value, moving=None):
        super(Person, self).delfromproperty(name, value, moving)
        if name == 'selections':
            value.len_selections = getattr(value, 'len_selections', 0)
            if value.len_selections > 0:
                value.len_selections -= 1

    def set_title(self):
        self.title = getattr(self, 'first_name', '') + ' ' + \
                     getattr(self, 'last_name', '')

    @property
    def proposals(self):
        return [wg.proposal for wg in self.working_groups]

    @property
    def contacts(self):
        return [s for s in self.selections if isinstance(s, Person)]

    @property
    def participations(self):
        result = [p for p in list(self.proposals)
                  if any(s in p.state for s
                         in ['amendable',
                             'open to a working group',
                             'votes for publishing',
                             'votes for amendments'])]
        return result

    @property
    def contents(self):
        result = [i for i in list(self.ideas) if i is i.current_version]
        result.extend(self.proposals)
        return result

    @property
    def supports(self):
        result = [t.__parent__ for t in self.tokens_ref
                  if not(t.__parent__ is self)]
        return list(set(result))

    @property
    def active_working_groups(self):
        return [p.working_group for p in self.participations]

    @property
    def is_published(self):
        return 'active' in self.state

    @property
    def managed_organization(self):
        return get_objects_with_role(user=self, role='OrganizationResponsible')

    def reindex(self):
        super(Person, self).reindex()
        root = getSite()
        self.__access_keys__ = PersistentList(generate_access_keys(
            self, root))

    def get_picture_url(self, kind, default):
        if self.picture:
            img = getattr(self.picture, kind, None)
            if img:
                return img.url

        return default

    def get_more_contents_criteria(self):
        "return specific query, filter values"
        return None, None

    def set_organization(self, organization):
        if organization:
            current_organization = self.organization
            if current_organization is not organization:
                is_manager = has_role(
                    self, (('AgencyResponsible', current_organization),))
                if current_organization and is_manager:
                    revoke_roles(
                        self, (('AgencyResponsible', current_organization),))

                self.setproperty('organization', organization)


@content(
    'preregistration',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IPreregistration)
class Preregistration(VisualisableElement, Entity):
    """Preregistration class"""
    icon = 'typcn typcn-user-add'
    templates = {'default': 'novaideo:views/templates/preregistration_result.pt',
                 'bloc': 'novaideo:views/templates/preregistration_result.pt'}
    name = renamer()
    structure = CompositeUniqueProperty('structure')

    def __init__(self, **kwargs):
        super(Preregistration, self).__init__(**kwargs)
        self.set_data(kwargs)
        self.title = self.first_name + ' ' + \
                     self.last_name

    def init_deadline(self, date):
        self.deadline_date = date\
            + datetime.timedelta(seconds=DEADLINE_PREREGISTRATION)
        return self.deadline_date

    def get_deadline_date(self):
        if getattr(self, 'deadline_date', None) is not None:
            return self.deadline_date

        self.deadline_date = self.created_at\
            + datetime.timedelta(seconds=DEADLINE_PREREGISTRATION)
        return self.deadline_date

    @property
    def is_expired(self):
        return datetime.datetime.now(tz=pytz.UTC) > self.get_deadline_date()
