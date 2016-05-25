# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import colander
import deform
from pyramid.view import view_config

from dace.util import get_obj
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.objectofcollaboration.principal.util import get_current
from pontus.form import FormView
from pontus.schema import select, Schema
from pontus.widget import AjaxSelect2Widget, Length
from pontus.view_operation import MultipleView
from pontus.view import BasicView

from novaideo.content.processes.idea_management.behaviors import PresentIdea
from novaideo.content.idea import Idea
from novaideo import _, log


try:
    basestring
except NameError:
    basestring = str


PRESENT_MESSAGE = {'0': _(u"""Aucune personne contactée"""),
                   '1': _(u"""Personne contactée"""),
                   '*': _(u"""Personnes contactées""")}


class SentToView(BasicView):
    title = _('Sent to')
    name = 'sentto'
    validators = [PresentIdea.get_validator()]
    template = 'novaideo:views/idea_management/templates/sent_to.pt'
    wrapper_template = 'daceui:templates/simple_view_wrapper.pt'
    viewid = 'sentto'

    def update(self):
        members = self.context.persons_contacted
        len_members = len(members)
        index = str(len_members)
        if len_members > 1:
            index = '*'

        message = (_(PRESENT_MESSAGE[index]),
                   len_members,
                   index)
        result = {}
        values = {
            'message': message,
            'members': members,
            'basestring': basestring,
        }
        self.message = message
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


@colander.deferred
def members_choice(node, kw):
    context = node.bindings['context']
    request = node.bindings['request']
    values = []
    ajax_url = request.resource_url(context,
                                    '@@novaideoapi',
                                    query={'op': 'find_user'})

    def title_getter(oid):
        try:
            obj = get_obj(int(oid), None)
            if obj:
                return obj.title
            else:
                return oid
        except Exception as e:
            log.warning(e)
            return oid

    return AjaxSelect2Widget(
        values=values,
        ajax_url=ajax_url,
        multiple=True,
        create=True,
        ajax_item_template="user_item_template",
        title_getter=title_getter,
        )


@colander.deferred
def default_subject(node, kw):
    context = node.bindings['context']
    mail_template = node.bindings['mail_template']
    return mail_template['subject'].format(subject_title=context.title)


@colander.deferred
def default_message(node, kw):
    context = node.bindings['context']
    request = node.bindings['request']
    mail_template = node.bindings['mail_template']
    localizer = request.localizer
    url = request.resource_url(context, "@@index")
    user = get_current()
    return mail_template['template'].format(
        recipient_title='',
        recipient_first_name='',
        recipient_last_name='',
        subject_url=url,
        subject_title=getattr(context, 'title', context.name),
        my_title=localizer.translate(_(getattr(user, 'user_title', ''))),
        my_first_name=getattr(user, 'first_name', user.name),
        my_last_name=getattr(user, 'last_name', ''),
        novaideo_title=request.root.title
    )


@colander.deferred
def emails_validator(node, kw):
    new_emails = [e for e in kw if isinstance(e, basestring)]
    validator = colander.Email()
    for email in new_emails:
        validator(node, email)


class PresentIdeaSchema(Schema):

    members = colander.SchemaNode(
        colander.Set(),
        widget=members_choice,
        validator=colander.All(
            Length(_, min=1,
                   min_message="""Vous devez sélectionner """
                               """au moins {min} membre, ou saisir {min}"""
                               """ adresse courrier électronique."""),
            emails_validator),

        title=_('Recipients')
        )

    subject = colander.SchemaNode(
        colander.String(),
        default=default_subject,
        title=_('Subject'),
        )

    message = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(max=2000),
        default=default_message,
        widget=deform.widget.TextAreaWidget(rows=10, cols=60),
        )

    send_to_me = colander.SchemaNode(
        colander.Boolean(),
        widget=deform.widget.CheckboxWidget(),
        label=_('Send to me'),
        title='',
        missing=False
        )


class PresentIdeaFormView(FormView):

    title = _('Submit the idea to others')
    schema = select(PresentIdeaSchema(),
                    ['members', 'subject', 'message', 'send_to_me'])
    behaviors = [PresentIdea]
    formid = 'formpresentideaform'
    name = 'presentideaform'

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi', query={'op': 'present_entity'})
        formwidget = deform.widget.FormWidget(css_class='presentform')
        formwidget.template = 'novaideo:views/templates/ajax_form.pt'
        self.schema.widget = formwidget

    def bind(self):
        root = self.request.root
        mail_template = root.get_mail_template('presentation_idea')
        return {'mail_template': mail_template}


@view_config(
    name='present',
    context=Idea,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class PresentIdeaView(MultipleView):

    title = _('Submit the idea to others')
    description = _('Submit the idea to others')
    name = 'present'
    template = 'daceui:templates/simple_mergedmultipleview.pt'
    wrapper_template = 'novaideo:views/idea_management/templates/panel_item.pt'
    views = (SentToView, PresentIdeaFormView)
    contextual_help = 'present-help'

    def get_message(self):
        message = (PRESENT_MESSAGE['0']).format()
        if self.validated_children:
            message = getattr(self.validated_children[0], 'message', message)

        return message

    def before_update(self):
        self.viewid = 'present'
        super(PresentIdeaView, self).before_update()

DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {PresentIdea: PresentIdeaView})
