# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember

from substanced.util import get_oid
from substanced.event import LoggedIn

from dace.objectofcollaboration.entity import Entity
from dace.objectofcollaboration.principal.util import get_current
from dace.util import getSite, get_obj
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView
from pontus.util import merge_dicts

from novaideo.content.processes.comment_management.behaviors import (
    SeeComment)
from novaideo.core import can_access
from novaideo import log
from novaideo.content.comment import Comment
from novaideo.utilities.util import render_listing_obj


@view_config(
    name='seecomment',
    context=Entity,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SeeCommentView(BasicView):
    title = ''
    name = 'seecomment'
    template = 'novaideo:views/comment_management/templates/see_comment.pt'
    viewid = 'seecomment'
    wrapper_template = 'novaideo:views/templates/simple_wrapper.pt'
    css_class = 'simple-bloc'
    container_css_class = 'home'
    requirements = {'css_links': [],
                    'js_links': ['novaideo:static/js/comment.js']}

    def update(self):
        comment_id = self.params('comment_id')
        user = get_current()
        comment = None
        try:
            obj = get_obj(int(comment_id)) if comment_id else None
            if isinstance(obj, Comment) and can_access(user, obj):
                comment = obj
        except Exception as error:
            log.warning(error)

        comment_body = ''
        if comment:
            comment_body = render_listing_obj(
                self.request, comment, user)

        values = {
            'comment_body': comment_body
        }
        result = {}
        body = self.content(
            args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        result = merge_dicts(self.requirements_copy, result)
        return result
