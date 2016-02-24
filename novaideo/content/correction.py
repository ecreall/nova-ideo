# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import colander
from bs4 import BeautifulSoup
from zope.interface import implementer
from pyramid.threadlocal import get_current_registry

from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer

import html_diff_wrapper
from dace.util import get_obj
from dace.objectofcollaboration.entity import Entity
from dace.descriptors import SharedUniqueProperty, CompositeUniqueProperty

from pontus.widget import RichTextWidget
from pontus.core import VisualisableElementSchema, VisualisableElement

from .interface import ICorrection
from novaideo import _
from novaideo.views.widget import LimitedTextAreaWidget


def context_is_a_correction(context, request):
    return request.registry.content.istype(context, 'correction')


class CorrectionSchema(VisualisableElementSchema):
    """Schema for correction of a proposal"""
    name = NameSchemaNode(
        editing=context_is_a_correction,
        )

    description = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(max=300),
        widget=LimitedTextAreaWidget(rows=5, 
                                     cols=30, 
                                     limit=300),
        title=_("Abstract")
        )

    text = colander.SchemaNode(
        colander.String(),
        widget=RichTextWidget(),
        title=_("Text")
        )


@content(
    'correction',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(ICorrection)
class Correction(VisualisableElement, Entity):
    """Correction class"""
    name = renamer()
    author = SharedUniqueProperty('author')
    proposal = SharedUniqueProperty('proposal', 'corrections')
    current_version = CompositeUniqueProperty('current_version')

    def __init__(self, **kwargs):
        super(Correction, self).__init__(**kwargs)
        self.set_data(kwargs)
        self.corrections = {}
    
    def _adapt_correction(self, correction_tag, is_favour):
        """
        Add 'correction-favour-vote' css_class to the 'correction_tag'
        if 'is_favour' is True
        """

        correction_tag.find("span", id="correction_actions").decompose()
        vote_class = 'correction-favour-vote'
        if not is_favour:
            vote_class = 'correction-against-vote'

        correction_tag['class'] = vote_class
 
    def _get_adapted_content(self, user, text):
        """Return the appropriate text to the user"""

        soup = BeautifulSoup(text)
        corrections = soup.find_all("span", id='correction')
        if user is self.author:
            for correction in corrections:
                self._adapt_correction(correction, True)
        else:    
            for correction in corrections:
                correction_data = self.corrections[correction["data-item"]]
                voters_favour =  any((get_obj(v) is user \
                                     for v in correction_data['favour']))
                if voters_favour:
                    self._adapt_correction(correction, True)
                    continue

                voters_against =  any((get_obj(v) is user \
                                       for v in correction_data['against']))
                if voters_against:
                    self._adapt_correction(correction, False)
       
        registry = get_current_registry()
        return html_diff_wrapper.soup_to_text(soup)

    def get_adapted_description(self, user):
        """Return the appropriate description to the user"""

        return self._get_adapted_content(user, self.description)

    def get_adapted_text(self, user):
        """Return the appropriate text to the user"""

        return self._get_adapted_content(user, self.text)

    def get_adapted_title(self, user):
        """Return the appropriate text to the user"""

        return self._get_adapted_content(user, self.title).replace('<p>', '').replace('</p>', '')