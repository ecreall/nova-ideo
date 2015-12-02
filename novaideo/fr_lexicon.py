# Copyright (c) 2015 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

from zope.interface import implementer
from pyramid.threadlocal import get_current_registry
from hypatia.text.interfaces import IPipelineElement
from hypatia.text.lexicon import Splitter, Lexicon

from dace.i18n.normalizer.interfaces import INormalizer
from dace.util import name_normalizer

from novaideo.fr_stopdict import get_stopdict


def normalize_word(word):
    normalizer = get_current_registry().getUtility(INormalizer,
                                                   'default_normalizer')
    if normalizer:
        return normalizer.normalize(word).decode().lower()

    return name_normalizer(word).lower()


@implementer(IPipelineElement)
class CaseNormalizer(object):

    def process(self, lst):
        return [normalize_word(w) for w in lst]


@implementer(IPipelineElement)
class StopWordRemover(object):

    dict = get_stopdict().copy()

    def process(self, lst):
        return [w for w in lst if w not in self.dict]
