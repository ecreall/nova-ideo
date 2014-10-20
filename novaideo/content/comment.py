import colander
import deform.widget
from zope.interface import implementer

from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer

from dace.descriptors import CompositeMultipleProperty, SharedUniqueProperty
from dace.util import getSite
from dace.objectofcollaboration.principal.util import get_current
from pontus.core import VisualisableElementSchema
from pontus.widget import SequenceWidget, FileWidget, Select2Widget
from pontus.file import ObjectData, File
from pontus.schema import Schema, omit

from .interface import IComment
from novaideo.core import Commentable
from novaideo import _
from novaideo.views.widget import Select2WidgetSearch, SimpleMappingtWidget


@colander.deferred
def intention_choice(node, kw):
    root = getSite()
    intentions = sorted(root.comment_intentions)
    values = [(i, i) for i in intentions ]
    values.insert(0, ('', '- Select -'))
    return Select2Widget(values=values)


@colander.deferred
def relatedcontents_choice(node, kw):
    context = node.bindings['context']
    request = node.bindings['request']
    root = getSite()
    user = get_current()
    contents = list(user.contents)
    values = [(i, i.title) for i in contents]
    return Select2WidgetSearch(multiple= True, 
                               values=values,
                               item_css_class='search-idea-form',
                               url=request.resource_url(root, '@@search', query={'op':'toselect', 'content_types':['CorrelableEntity']}))


class RelatedContentsSchema(Schema):

    related_contents = colander.SchemaNode(
        colander.Set(),
        widget=relatedcontents_choice,
        title=_('Associated contents'),
        description=_('Choose contents to associate.'),
        missing=[],
        default=[],
        )


def context_is_a_comment(context, request):
    return request.registry.content.istype(context, 'comment')


class CommentSchema(VisualisableElementSchema):

    name = NameSchemaNode(
        editing=context_is_a_comment,
        )

    intention = colander.SchemaNode(
        colander.String(),
        widget=intention_choice,
        title=_('Intention'),
        )

    comment = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(max=2000),
        widget=deform.widget.TextAreaWidget(rows=4, cols=60),
        )

    related_contents = RelatedContentsSchema(widget=SimpleMappingtWidget(mapping_css_class="controled-form hide-bloc",
                                                                   ajax=True,
                                                                   activator_css_class="glyphicon glyphicon-link",
                                                                   activator_title=_('Associate')))


@content(
    'comment',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IComment)
class Comment(Commentable):
    name = renamer()
    author = SharedUniqueProperty('author')

    def __init__(self, **kwargs):
        super(Comment, self).__init__(**kwargs)
        self.set_data(kwargs)

    @property
    def subject(self):
        if not isinstance(self.__parent__, Comment):
            return self.__parent__
        else:
            return self.__parent__.subject 


class AddCommentSchema(Schema):

    comment = omit(CommentSchema(factory=Comment,
                                 editable=True,
                                 name=_('Comment')), ['_csrf_token_'])
