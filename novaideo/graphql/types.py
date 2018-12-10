# -*- coding: utf-8 -*-
from pyramid.httpexceptions import HTTPUnauthorized
from pyramid.security import Everyone

from dace.util import get_obj
from novaideo.core import can_access
from novaideo import _


class SecureObjectType(object):

    @classmethod
    def get_node(cls, id, context, info):
        try:
            result = get_obj(int(id))
        except Exception:
            return None

        if not can_access(context.user, result):
            raise HTTPUnauthorized(_("You are not authorized to access to this page"))

        return result
