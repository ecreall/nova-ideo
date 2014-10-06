from dogpile.cache import make_region

region = make_region(
    ).configure(
    "dogpile.cache.memory_pickle",
    expiration_time=3600,
    )
