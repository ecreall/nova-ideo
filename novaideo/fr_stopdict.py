# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

"""Provide a default list of stop words for the index.

The specific splitter and lexicon are customizable, but the default
ZCTextIndex should do something useful.
"""


def get_stopdict():
    """Return a dictionary of stopwords."""
    return _dict

# This list of French stopwords comes from http://www.ranks.nl/stopwords/french
_words = [
    "alors", "au", "aucuns", "aussi", "autre", "avant", "avec", "avoir", "bon",
    "car", "ce", "cela", "ces", "ceux", "chaque", "ci", "comme", "comment",
    "dans", "des", "du", "dedans", "dehors", "depuis", "devrait", "doit",
    "donc", "dos", "début", "elle", "elles", "en", "encore", "essai", "est",
    "et", "eu", "fait", "faites", "fois", "font", "hors", "ici", "il", "ils",
    "je", "juste", "la", "le", "les", "leur", "là", "ma", "maintenant", "mais",
    "mes", "mine", "moins", "mon", "mot", "même", "ni", "nommés", "notre", "nous",
    "ou", "où", "par", "parce", "pas", "peut", "peu", "plupart", "pour", "pourquoi",
    "quand", "que", "quel", "quelle", "quelles", "quels", "qui", "sa", "sans",
    "ses", "seulement", "si", "sien", "son", "sont", "sous", "soyez", "sujet",
    "sur", "ta", "tandis", "tellement", "tels", "tes", "ton", "tous", "tout",
    "trop", "très", "tu", "voient", "vont", "votre", "vous", "vu", "ça", "étaient",
    "état", "étions", "été", "être", "soit", "un", "une", "d'un", "d'une", "de", "à"
]


_dict = {}


for w in _words:
    _dict[w] = None
