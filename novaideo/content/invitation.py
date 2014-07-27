import colander
import deform
import deform.widget
from zope.interface import implementer

from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer

from dace.util import getSite
from dace.objectofcollaboration.entity import Entity
from dace.objectofcollaboration.object import (
                SHARED_UNIQUE,
                COMPOSITE_MULTIPLE,
                COMPOSITE_UNIQUE)
from dace.objectofcollaboration.principal.role import roles_id
from pontus.widget import RichTextWidget, Select2Widget
from pontus.core import VisualisableElement, VisualisableElementSchema
from pontus.file import Object as ObjectType

from .interface import IInvitation
from .person import PersonSchema



@colander.deferred
def roles_choice(node, kw):
    roles = sorted(roles_id.keys())
    values = [(i, i) for i in roles if not roles_id[i].islocal]
    return Select2Widget(values=values, multiple=True)


def context_is_a_invitation(context, request):
    return request.registry.content.istype(context, 'invitation')


class InvitationSchema(PersonSchema):

    roles = colander.SchemaNode(
                    colander.Set(),
                    widget=roles_choice,
                    title='Roles',
                    missing=['Collaborator'],
                    default=['Collaborator']
                )


@content(
    'invitation',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IInvitation)
class Invitation(VisualisableElement, Entity):
    name = renamer()
    properties_def = {'organization':(SHARED_UNIQUE, None, False)}

    def __init__(self, **kwargs):
        super(Invitation, self).__init__(**kwargs)
        self.title = 'Invitation'
        if 'first_name' in kwargs:
            self.first_name = kwargs.get('first_name')
            self.title = self.title + ' '+ self.first_name
 
        if 'last_name' in kwargs:
            self.last_name = kwargs.get('last_name')
            self.title = self.title + ' '+ self.last_name

        if 'email' in kwargs:
            self.email = kwargs.get('email')

        if 'user_title' in kwargs:
            self.user_title = kwargs.get('user_title')

        if 'roles' in kwargs:
            self.roles = kwargs.get('roles')

    @property
    def organization(self):
        return self.getproperty('organization')

    def setorganization(self, organization):
        self.setproperty('organization', organization)
