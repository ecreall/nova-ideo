# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi
# -*- coding: utf8 -*-
import os
import datetime
import pytz
from BTrees.OOBTree import OOBTree
import colander
import deform.widget
from persistent.list import PersistentList
from persistent.dict import PersistentDict
from zope.interface import implementer

from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer, get_oid
from substanced.principal import UserSchema

from dace.util import getSite, find_catalog
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
    generate_access_keys,
    Debatable)
from .interface import (
    IPerson, IPreregistration, IAlert, IProposal, Iidea)
from novaideo import _
from novaideo.file import Image
from novaideo.views.widget import (
    TOUCheckboxWidget, LimitedTextAreaWidget, EmailInputWidget)


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
    values = [(str(i), i) for i in root.titles]
    values.insert(0, ('', _('- Select -')))
    return Select2Widget(values=values)


@colander.deferred
def email_validator(node, kw):
    context = node.bindings['context']
    novaideo_catalog = find_catalog('novaideo')
    identifier_index = novaideo_catalog['identifier']
    query = identifier_index.any([kw])
    users = list(query.execute().all())
    if context in users:
        users.remove(context)

    if users:
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
        title=_('Topics of interest'),
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
        description=_('Please do not select anything if you do not want to communicate this information.'),
        missing=''
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
class Person(User, SearchableEntity, CorrelableEntity, Debatable):
    """Person class"""

    type_title = _('Person')
    icon = 'icon glyphicon glyphicon-user' #'icon novaideo-icon icon-user'
    templates = {'default': 'novaideo:views/templates/person_result.pt',
                 'bloc': 'novaideo:views/templates/person_bloc.pt',
                 'small': 'novaideo:views/templates/small_person_result.pt',
                 'popover': 'novaideo:views/templates/person_popover.pt'}
    name = renamer()
    tokens = CompositeMultipleProperty('tokens')
    tokens_ref = SharedMultipleProperty('tokens_ref')
    organization = SharedUniqueProperty('organization', 'members')
    picture = CompositeUniqueProperty('picture')
    ideas = SharedMultipleProperty('ideas', 'author')
    selections = SharedMultipleProperty('selections')
    working_groups = SharedMultipleProperty('working_groups', 'members')
    old_alerts = SharedMultipleProperty('old_alerts')
    following_channels = SharedMultipleProperty('following_channels', 'members')
    folders = SharedMultipleProperty('folders', 'author')
    questions = SharedMultipleProperty('questions', 'author')
    challenges = SharedMultipleProperty('challenges', 'author')

    def __init__(self, **kwargs):
        if 'locale' not in kwargs:
            kwargs['locale'] = DEFAULT_LOCALE

        super(Person, self).__init__(**kwargs)
        kwargs.pop('password')
        self.set_data(kwargs)
        self.set_title()
        self.last_connection = datetime.datetime.now(tz=pytz.UTC)
        self._read_at = OOBTree()
        self.guide_tour_data = PersistentDict({})

    def __setattr__(self, name, value):
        super(Person, self).__setattr__(name, value)
        if name == 'organization' and value:
            self.init_contents_organizations()

    def init_contents_organizations(self):
        novaideo_catalog = find_catalog('novaideo')
        dace_catalog = find_catalog('dace')
        organizations_index = novaideo_catalog['organizations']
        object_authors_index = novaideo_catalog['object_authors']
        object_provides_index = dace_catalog['object_provides']
        query = object_authors_index.any([get_oid(self)]) & \
            object_provides_index.any(
                [Iidea.__identifier__, IProposal.__identifier__]) & \
            organizations_index.any([0])

        for entity in query.execute().all():
            entity.init_organization()
            entity.reindex()

    def set_read_date(self, channel, date):
        self._read_at[get_oid(channel)] = date

    def get_read_date(self, channel):
        return self._read_at.get(
            get_oid(channel), datetime.datetime.now(tz=pytz.UTC))

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
        result.extend(self.questions)
        result.extend(self.challenges)
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
        current_organization = self.organization
        if organization:
            if current_organization is not organization:
                is_manager = current_organization and has_role(
                    ('OrganizationResponsible', current_organization), self,
                    ignore_superiors=True)
                if current_organization and is_manager:
                    revoke_roles(
                        self,
                        (('OrganizationResponsible', current_organization),))

                self.setproperty('organization', organization)
        elif current_organization:
            is_manager = has_role(
                ('OrganizationResponsible', current_organization), self,
                ignore_superiors=True)
            if is_manager:
                revoke_roles(
                    self,
                    (('OrganizationResponsible', current_organization),))

            self.delfromproperty('organization', current_organization)

    @property
    def all_alerts(self):
        novaideo_catalog = find_catalog('novaideo')
        dace_catalog = find_catalog('dace')
        alert_keys_index = novaideo_catalog['alert_keys']
        alert_exclude_keys_index = novaideo_catalog['alert_exclude_keys']
        object_provides_index = dace_catalog['object_provides']
        query = object_provides_index.any([IAlert.__identifier__]) & \
            alert_keys_index.any(self.get_alerts_keys()) & \
            alert_exclude_keys_index.notany([str(get_oid(self))])
        return query.execute()

    @property
    def alerts(self):
        old_alerts = [get_oid(a) for a in self.old_alerts]
        result = self.all_alerts

        def exclude(result_set, docids):
            filtered_ids = list(result_set.ids)
            for _id in docids:
                if _id in docids and _id in filtered_ids:
                    filtered_ids.remove(_id)

            return result_set.__class__(
                filtered_ids, len(filtered_ids), result_set.resolver)

        return exclude(result, old_alerts)

    def get_alerts_keys(self):
        result = ['all', str(get_oid(self))]
        return result

    def get_alerts(self, alerts=None, kind=None,
                   subject=None, **kwargs):
        if alerts is None:
            alerts = self.alerts

        if kind:
            alerts = [a for a in alerts
                      if a.is_kind_of(kind)]

        if subject:
            alerts = [a for a in alerts
                      if subject in a.subjects]

        if kwargs:
            alerts = [a for a in alerts
                      if a.has_args(**kwargs)]

        return alerts

    @property
    def user_groups(self):
        groups = list(self.groups)
        if self.organization:
            groups.append(self.organization)

        return groups


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
    organization = SharedUniqueProperty('organization')

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

    def has_trusted_email(self, trusted_emails):
        email = getattr(self, 'email', None)
        if email and trusted_emails:
            return any(
                email.find(t)>=0 for t in trusted_emails)

        return True

    @property
    def is_expired(self):
        return datetime.datetime.now(tz=pytz.UTC) > self.get_deadline_date()
