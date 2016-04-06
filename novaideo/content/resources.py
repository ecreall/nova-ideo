# # Copyright (c) 2015 by Ecreall under licence AGPL terms
# # avalaible on http://www.gnu.org/licenses/agpl.html

# # licence: AGPL
# # author: Amen Souissi

# import os

# from arango import Arango


# ARANGO_HOST, ARANGO_PORT = os.getenv(
#     'ARANGO_PORT', 'localhost:8529').split(':')
# ARANGO_ROOT_PASSWORD = os.getenv('ARANGO_ROOT_PASSWORD', '')

# arango_server = Arango(
#     host=ARANGO_HOST, port=ARANGO_PORT,
#     password=ARANGO_ROOT_PASSWORD)


# def arango_db__check():
#     try:
#         arango_server.create_database("novaideo")
#     except Exception:
#         pass

# arango_db__check()


# def create_collection(db, id_):
#     try:
#         db.create_collection(id_)
#     except Exception:
#         pass

#     return db.col(id_)
