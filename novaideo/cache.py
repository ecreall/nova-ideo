
from dogpile.cache import make_region

REGION = make_region(
    ).configure(
    "dogpile.cache.memory_pickle",
    expiration_time=3600,
    )
