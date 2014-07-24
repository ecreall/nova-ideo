import colander
import deform
import deform.widget
from zope.interface import implementer

from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer

from dace.util import getSite
from dace.objectofcollaboration.entity import Entity
from pontus.widget import RichTextWidget, Select2Widget
from pontus.core import VisualisableElement, VisualisableElementSchema

from .interface import IInvitation



@colander.deferred
def titles_choice(node, kw):
    context = node.bindings['context']
    request = node.bindings['request']
    root = getSite(context)
    values = [(i, i) for i in root.titles]
    return Select2Widget(values=values)


def context_is_a_invitation(context, request):
    return request.registry.content.istype(context, 'invitation')


class InvitationSchema(VisualisableElementSchema):

    name = NameSchemaNode(
        editing=context_is_a_invitation,
        )

    first_name =  colander.SchemaNode(
                    colander.String(),
                    title='First name' 
                    )

    last_name = colander.SchemaNode(
                    colander.String(),
                    title='Last name' 
                    )
    
    email = colander.SchemaNode(
                colander.String(),
                validator=colander.All(
                    colander.Email(),
                    colander.Length(max=100)
                    ),
                )
  
    user_title = colander.SchemaNode(
                    colander.String(),
                    widget=titles_choice,
                    title='Title'
                )


@content(
    'invitation',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IInvitation)
class Invitation(VisualisableElement, Entity):
    name = renamer()

    def __init__(self, **kwargs):
        super(Invitation, self).__init__(**kwargs)
        if 'first_name' in kwargs:
            self.first_name = kwargs.get('first_name')

        if 'last_name' in kwargs:
            self.last_name = kwargs.get('last_name')

        if 'email' in kwargs:
            self.email = kwargs.get('email')

        if 'user_title' in kwargs:
            self.user_title = kwargs.get('user_title')

