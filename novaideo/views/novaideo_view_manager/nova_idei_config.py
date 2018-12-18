# -*- coding: utf8 -*-
# Copyright (c) 2015 by Ecreall under licence AGPL terms
# available on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.objectofcollaboration.principal.util import has_role
from dace.util import getSite
from dace.processinstance.core import (
    ValidationError, Validator)
from pontus.view import BasicView

from novaideo import _


# class NovaIdeoConfigValidator(Validator):

#     @classmethod
#     def validate(cls, context, request, **kw):
#         if has_role(role=('Anonymous',)):
#             return True

#         raise ValidationError(msg=_("Permission denied"))


@view_config(
    name='novaideoconfig',
    renderer='pontus:templates/views_templates/grid.pt',
    layout='old'
    )
class NovaIdeoConfigView(BasicView):

    title = _('Main numeric parameters')
    name = 'novaideoconfig'
    template = 'novaideo:views/novaideo_view_manager/templates/novaideo_config.pt'
    # validators = [NovaIdeoConfigValidator]

    def update(self):
        result = {}
        values = {'root': getSite()}
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result
