# -*- coding: utf8 -*-
import colander
import deform.widget
from zope.interface import implementer, invariant

from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer
from substanced.principal import UserSchema
from substanced.interfaces import IUserLocator
from substanced.principal import DefaultUserLocator

from dace.util import getSite, find_entities, find_catalog
from dace.objectofcollaboration.principal import User
from dace.descriptors import (
    SharedUniqueProperty,
    CompositeMultipleProperty,
    CompositeUniqueProperty,
    SharedMultipleProperty)
from pontus.core import VisualisableElement, VisualisableElementSchema
from pontus.widget import FileWidget, Select2Widget
from pontus.file import Image, ObjectData, Object as ObjectType

from novaideo.core import (
    SearchableEntity,
    SearchableEntitySchema,
    default_keywords_choice,
    keywords_choice,
    CorrelableEntity)
from .interface import IPerson
from novaideo import _


@colander.deferred
def organization_choice(node, kw):
    context = node.bindings['context']
    values = []
    root = getSite()
    if root is None:
        root = context.__parent__.__parent__

    prop = sorted(root.organizations, key=lambda p: p.title)
    values = [(i, i.title) for i in prop]
    values.insert(0, ('', '- Select -'))
    return Select2Widget(values=values)


@colander.deferred
def titles_choice(node, kw):
    root = getSite()
    values = [(i, i) for i in root.titles]
    values.insert(0, ('', '- Select -'))
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
def contacts_choice(node, kw):
    context = node.bindings['context']
    values = []
    users = find_entities([IPerson], ['active'])
    values = [(i, i.name) for i in users if not (i in context.contacts)]
    values = sorted(values, key=lambda p: p[1])
    return Select2Widget(values=values, multiple=True)


@colander.deferred
def default_contacts(node, kw):
    context = node.bindings['context']
    prop = sorted(context.contacts, key=lambda p: p.name)
    return prop


def context_is_a_person(context, request):
    return request.registry.content.istype(context, 'person')


class PersonSchema(VisualisableElementSchema, UserSchema, SearchableEntitySchema):

    name = NameSchemaNode(
        editing=context_is_a_person,
        )

    keywords =  colander.SchemaNode(
        colander.Set(),
        default=default_keywords_choice,
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
        )

    picture = colander.SchemaNode(
        ObjectData(Image),
        widget=FileWidget(),
        required=False,
        missing=None,
        )

    first_name =  colander.SchemaNode(
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
        title=_('Title'),
        )

    password = colander.SchemaNode(
        colander.String(),
        widget = deform.widget.CheckedPasswordWidget(),
        validator=colander.Length(min=3, max=100),
        )

    organization = colander.SchemaNode(
        ObjectType(),
        widget=organization_choice,
        missing=None,
        title=_('Organization'),
        )


    @invariant
    def person_name_invariant(self, appstruct):
        context = self.bindings['context']
        request = self.bindings['request']
        root = getSite()
        name = ''
        if 'first_name' in appstruct:
            name = name + appstruct['first_name']
            if 'last_name' in appstruct:
                name = name + ' ' + appstruct['last_name']

        if context.name == name:
            return 

        system_catalog = find_catalog('system')
        name_index = system_catalog['name']
        query = name_index.eq(name)
        resultset = query.execute()
        if resultset.__len__() > 0:
            raise colander.Invalid(self, _('The user ' + name + ' already exists!'))


@content(
    'person',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IPerson)
class Person(VisualisableElement, User, SearchableEntity, CorrelableEntity):
    result_template = 'novaideo:views/templates/person_result.pt'
    name = renamer()
    tokens = CompositeMultipleProperty('tokens')
    tokens_ref = SharedMultipleProperty('tokens_ref')
    organization = SharedUniqueProperty('organization', 'members')
    picture = CompositeUniqueProperty('picture')
    ideas = SharedMultipleProperty('ideas', 'author')
    selections = SharedMultipleProperty('selections')
    working_groups = SharedMultipleProperty('working_groups', 'members')

    def __init__(self, **kwargs):
        super(Person, self).__init__(**kwargs)
        kwargs.pop('password')
        self.set_data(kwargs)
        self.set_title()

    def set_title(self):
        self.title = self.first_name + ' ' + self.last_name

    @property
    def proposals(self):
        return [wg.proposal for wg in self.working_groups]

    @property
    def contacts(self):
        return [s for s in self.selections if isinstance(s, Person)]

    @property
    def participations(self):
        result = [p for p in list(self.proposals) if not('draft' in p.state)]
        return result

    @property
    def contents(self):
        result = list(self.ideas)
        result.extend(self.proposals)
        #TODO 
        return result

    @property
    def supports(self):
        result = [] #[t.__parent__ for t in self.tokens_ref if not(t.__parent__ is self)] Error TODO add cache system
        for t in self.tokens_ref:
            if not(t.__parent__ is self):
                result.append(t.__parent__)

        return list(set(result))

    @property
    def active_working_groups(self):
        return [w for w in self.working_groups if not any(s in w.proposal.state for s in ['draft', 'published'])]
    
