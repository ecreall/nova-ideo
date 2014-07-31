import colander
import deform.widget
from zope.interface import implementer

from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer

from dace.objectofcollaboration.entity import Entity
from dace.descriptors import CompositeMultipleProperty
from pontus.core import VisualisableElementSchema
from pontus.widget import SequenceWidget, FileWidget
from pontus.file import ObjectData, File
from pontus.schema import Schema, omit

from .interface import IComment
from .commentabl import Commentabl
from novaideo import _



def context_is_a_comment(context, request):
    return request.registry.content.istype(context, 'comment')


class CommentSchema(VisualisableElementSchema):

    name = NameSchemaNode(
        editing=context_is_a_comment,
        )

    comment = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(max=2000),
        widget=deform.widget.TextAreaWidget(rows=10, cols=60)
        )

    attached_files = colander.SchemaNode(
        colander.Sequence(),
        colander.SchemaNode(
            ObjectData(File),
            name=_("File"),
            widget= FileWidget()
            ),
        widget=SequenceWidget(max_len=4),
        title=_('Files')
        )


@content(
    'comment',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IComment)
class Comment(Commentabl):
    name = renamer()

    def __init__(self, **kwargs):
        super(Comment, self).__init__(**kwargs)


class AddCommentSchema(Schema):

    comment = omit(CommentSchema(factory=Comment,
                                 editable=True,
                                 name=_('Comment')),['_csrf_token_'])
