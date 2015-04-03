# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import colander
import deform.widget
from zope.interface import implementer

from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer

from dace.descriptors import SharedUniqueProperty
from dace.util import getSite
from pontus.core import VisualisableElementSchema
from pontus.widget import Select2Widget, AjaxSelect2Widget
from pontus.schema import Schema

from .interface import IComment
from novaideo.core import Commentable
from novaideo import _
from novaideo.views.widget import SimpleMappingtWidget


@colander.deferred
def intention_choice(node, kw):
    root = getSite()
    intentions = sorted(root.comment_intentions)
    values = [(str(i), i) for i in intentions ]
    values.insert(0, ('', _('- Select -')))
    return Select2Widget(values=values)


@colander.deferred
def relatedcontents_choice(node, kw):
    request = node.bindings['request']
    root = getSite()
    values = []
    ajax_url = request.resource_url(root, '@@search', 
                                    query={'op':'find_entities', 
                                           'content_types':['CorrelableEntity']
                                           }
                               )
    return AjaxSelect2Widget(values=values,
                        ajax_url=ajax_url,
                        ajax_item_template="related_item_template",
                        css_class="search-idea-form",
                        multiple=True,
                        page_limit=50)


class RelatedContentsSchema(Schema):
    """Schema for associtation"""

    related_contents = colander.SchemaNode(
        colander.Set(),
        widget=relatedcontents_choice,
        title=_('Associated contents'),
        description=_('Choose contents to associate.'),
        missing=[],
        default=[],
        )

    associate = colander.SchemaNode(
        colander.Boolean(),
        widget=deform.widget.CheckboxWidget(css_class="hide-bloc"),
        label='',
        title ='',
        default=False,
        missing=False
        )


def context_is_a_comment(context, request):
    return request.registry.content.istype(context, 'comment')


class CommentSchema(VisualisableElementSchema):
    """Schema for comment"""

    name = NameSchemaNode(
        editing=context_is_a_comment,
        )

    intention = colander.SchemaNode(
        colander.String(),
        widget=intention_choice,
        title=_('Intention'),
        default=_('Remark')
        )

    comment = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(max=2000),
        widget=deform.widget.TextAreaWidget(rows=4, cols=60),
        title=_("Message")
        )

    related_contents = RelatedContentsSchema(
                widget=SimpleMappingtWidget(
                    mapping_css_class="controled-form associate-form hide-bloc",
                    ajax=True,
                    activator_css_class="glyphicon glyphicon-link",
                    activator_title=_('Associate')))


@content(
    'comment',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IComment)
class Comment(Commentable):
    """Comment class"""
    name = renamer()
    author = SharedUniqueProperty('author')
    related_correlation = SharedUniqueProperty('related_correlation', 'targets')

    def __init__(self, **kwargs):
        super(Comment, self).__init__(**kwargs)
        self.set_data(kwargs)

    @property
    def subject(self):
        """Return the commented entity"""

        if not isinstance(self.__parent__, Comment):
            return self.__parent__
        else:
            return self.__parent__.subject 