# -*- coding: utf8 -*-
import colander
import deform.widget
from zope.interface import implementer
from persistent.list import PersistentList
from pyramid.threadlocal import get_current_request

from substanced.interfaces import IUserLocator
from substanced.principal import DefaultUserLocator
from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer

from dace.util import getSite
from dace.objectofcollaboration.entity import Entity
from dace.descriptors import SharedUniqueProperty, CompositeMultipleProperty, SharedMultipleProperty
from pontus.core import VisualisableElement, VisualisableElementSchema
from pontus.widget import (
    RichTextWidget,
    LineWidget,
    TableWidget,
    Select2Widget,
    SequenceWidget,
    FileWidget)
from pontus.file import ObjectData, File
from pontus.schema import omit

from .interface import Iidea
from novaideo.core import Commentable
from novaideo import _
from novaideo.core import (
    VersionableEntity,
    DuplicableEntity,
    SearchableEntity,
    SearchableEntitySchema,
    CorrelableEntity)


@colander.deferred
def intention_choice(node, kw):
    root = getSite()
    intentions = sorted(root.idea_intentions)
    values = [(i, i) for i in intentions ]
    return Select2Widget(values=values)


def context_is_a_idea(context, request):
    return request.registry.content.istype(context, 'idea')


class IdeaSchema(VisualisableElementSchema, SearchableEntitySchema):

    name = NameSchemaNode(
        editing=context_is_a_idea,
        )

    description = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(max=300),
        widget=deform.widget.TextAreaWidget(rows=10, cols=30),
        title=_("Abstract"),
        description=_("(300 caracteres maximum)")
        )

    text = colander.SchemaNode(
        colander.String(),
        widget= RichTextWidget(),
        title=_('Text'),
        missing='',
        )

    intention = colander.SchemaNode(
        colander.String(),
        widget=intention_choice,
        title=_('Intention'),
        default=_('Creation'),
        )

    attached_files = colander.SchemaNode(
        colander.Sequence(),
        colander.SchemaNode(
            ObjectData(File),
            name=_("File"),
            widget=FileWidget()
            ),
        widget=SequenceWidget(),
        missing=[],
        title=_('Files'),
        )


@content(
    'idea',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(Iidea)
class Idea(Commentable, VersionableEntity, DuplicableEntity,
           SearchableEntity, CorrelableEntity):
    result_template = 'novaideo:views/templates/idea_result.pt'
    template = 'novaideo:views/templates/idea_list_element.pt'
    name = renamer()
    author = SharedUniqueProperty('author', 'ideas')
    attached_files = CompositeMultipleProperty('attached_files')

    def __init__(self, **kwargs):
        super(Idea, self).__init__(**kwargs)
        self.set_data(kwargs)
        self.email_persons_contacted = PersistentList()

    @property
    def related_proposals(self):
        return [c.source for c in self.source_correlations if ((c.type==1) and ('related_proposals' in c.tags))]

    @property
    def persons_contacted(self):
        request = get_current_request()
        adapter = request.registry.queryMultiAdapter(
                (self, request),
                IUserLocator
                )
        if adapter is None:
            adapter = DefaultUserLocator(self, request)

        result = []
        for email in self.email_persons_contacted:
            user = adapter.get_user_by_email(email)
            if user is not None:
                result.append(user)
            else:
                result.append(email)

        return set(result)

