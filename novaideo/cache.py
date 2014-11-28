# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from dogpile.cache import make_region

REGION = make_region(
    ).configure(
    "dogpile.cache.memory_pickle",
    expiration_time=3600,
    )
