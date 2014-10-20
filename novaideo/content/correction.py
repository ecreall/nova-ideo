import colander
import deform
from bs4 import BeautifulSoup
from zope.interface import implementer
from pyramid.threadlocal import get_current_request, get_current_registry

from substanced.interfaces import IUserLocator
from substanced.principal import DefaultUserLocator
from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer

from dace.util import getSite, get_obj
from dace.objectofcollaboration.principal.util import get_current
from dace.objectofcollaboration.entity import Entity
from dace.descriptors import SharedUniqueProperty

from pontus.widget import RichTextWidget
from pontus.core import VisualisableElementSchema, VisualisableElement

from .interface import ICorrection
from novaideo import _
from novaideo.utilities.text_analyzer import ITextAnalyzer



def context_is_a_correction(context, request):
    return request.registry.content.istype(context, 'correction')


class CorrectionSchema(VisualisableElementSchema):

    name = NameSchemaNode(
        editing=context_is_a_correction,
        )

    text = colander.SchemaNode(
        colander.String(),
        widget=RichTextWidget()
        )


@content(
    'correction',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(ICorrection)
class Correction(VisualisableElement, Entity):
    name = renamer()
    author = SharedUniqueProperty('author')
    proposal = SharedUniqueProperty('proposal', 'corrections')

    def __init__(self, **kwargs):
        super(Correction, self).__init__(**kwargs)
        self.set_data(kwargs)
        self.corrections = {}
    
    def _adapt_correction(self, correction_tag, is_favour):
        correction_tag.find("span", id="correction_actions").decompose()
        vote_class = 'correction-favour-vote'
        if not is_favour:
            vote_class = 'correction-against-vote'

        correction_tag['class'] = vote_class
 
    def _get_adapted_content(self, user, text):
        soup = BeautifulSoup(text)
        corrections = soup.find_all("span", id='correction')
        if user is self.author:
            for correction in corrections:
                self._adapt_correction(correction, True)
        else:    
            for correction in corrections:
                correction_data = self.corrections[correction["data-item"]]
                voters_favour =  any((get_obj(v) is user for v in correction_data['favour']))
                if voters_favour:
                    self._adapt_correction(correction, True)
                    continue

                voters_against =  any((get_obj(v) is user for v in correction_data['against']))
                if voters_against:
                    self._adapt_correction(correction, False)
       
        text_analyzer = get_current_registry().getUtility(ITextAnalyzer,'text_analyzer')
        return text_analyzer.soup_to_text(soup)

    def get_adapted_description(self, user):
        return self._get_adapted_content(user, self.description)

    def get_adapted_text(self, user):
        return self._get_adapted_content(user, self.text)

