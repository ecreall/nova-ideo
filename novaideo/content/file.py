# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import colander
from zope.interface import implementer

from substanced.content import content

from dace.descriptors import SharedUniqueProperty
from pontus.core import VisualisableElementSchema
from pontus.widget import (
    RichTextWidget)

from .interface import IFile
from novaideo import _
from novaideo.core import (
    SearchableEntitySchema,
    SearchableEntity)
from novaideo.utilities.util import truncate_text, html_to_text


class FileSchema(VisualisableElementSchema, SearchableEntitySchema):

    text = colander.SchemaNode(
        colander.String(),
        widget=RichTextWidget(),
        title=_("Text")
        )


@content(
    'file',
    icon='icon novaideo-icon icon-user',
    )
@implementer(IFile)
class FileEntity(SearchableEntity):
    """ A file entity is an entity that can be searched"""

    icon = "glyphicon glyphicon-file"
    templates = {
        'default': 'novaideo:views/templates/file_result.pt',
        'bloc': 'novaideo:views/templates/file_bloc.pt'}
    type_title = _('File')
    author = SharedUniqueProperty('author')

    def __init__(self, **kwargs):
        super(FileEntity, self).__init__(**kwargs)
        self.set_data(kwargs)

    def _init_presentation_text(self):
        self._presentation_text = html_to_text(
            getattr(self, 'text', ''))

    def __setattr__(self, name, value):
        super(FileEntity, self).__setattr__(name, value)
        if name == 'text':
            self._init_presentation_text()

    def presentation_text(self, nb_characters=400):
        text = getattr(self, '_presentation_text', None)
        if text is None:
            self._init_presentation_text()
            text = getattr(self, '_presentation_text', '')

        return truncate_text(text, nb_characters)
