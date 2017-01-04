# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import deform
import colander
from pyramid.view import view_config

from dace.objectofcollaboration.principal.util import get_current
from dace.util import getSite
from dace.processinstance.core import (
    DEFAULTMAPPING_ACTIONS_VIEWS, Validator, ValidationError)
from dace.objectofcollaboration.entity import Entity
from pontus.form import FormView
from pontus.view import BasicView
from pontus.view_operation import MultipleView
from pontus.schema import Schema

from novaideo.content.processes.novaideo_view_manager.behaviors import (
    Contact)
from novaideo import _
from novaideo.views.widget import EmailInputWidget


@colander.deferred
def contact_choice(node, kw):
    root = getSite()
    contacts = [c for c in getattr(root, 'contacts', [])
                if c.get('email', None)]
    values = [(c.get('email'), c.get('title')) for c in contacts]
    return deform.widget.CheckboxChoiceWidget(values=values)


class ContactSchema(Schema):

    services = colander.SchemaNode(
        colander.Set(),
        widget=contact_choice,
        title=_("Services to contact"),
        validator=colander.Length(min=1)
        )

    name = colander.SchemaNode(
        colander.String(),
        title=_('Name'),
        missing='',
        description=_('Please enter your full name')
        )

    email = colander.SchemaNode(
        colander.String(),
        widget=EmailInputWidget(),
        validator=colander.All(
            colander.Email(),
            colander.Length(max=100)
            ),
        title=_('Email'),
        description=_('Please enter your email address')
        )

    subject = colander.SchemaNode(
        colander.String(),
        title=_('Subject')
        )

    message = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.TextAreaWidget(rows=4, cols=60),
        title=_('Message'),
        description=_('Please enter the message you want to send.')
        )


class ContactStudyReport(BasicView):
    title = _('Services to contact')
    name = 'contactreport'
    template = 'novaideo:views/novaideo_view_manager/templates/contact.pt'

    def update(self):
        result = {}
        root = getSite()
        values = {'contacts': getattr(root, 'contacts', [])}
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


class ContactValidator(Validator):

    @classmethod
    def validate(cls, context, request, **kw):
        root = getSite()
        for contact in getattr(root, 'contacts', []):
            if contact.get('email', None):
                return True

        raise ValidationError()


class ContactForm(FormView):
    title = _('Contact')
    name = 'contactform'
    formid = 'formcontact'
    schema = ContactSchema()
    behaviors = [Contact]
    validators = [ContactValidator]
    validate_behaviors = False

    def default_data(self):
        user = get_current()
        return {'name': getattr(user, 'first_name', ''),
                'email': getattr(user, 'email', '')}

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': Contact.node_definition.id})
        self.schema.widget = deform.widget.FormWidget(
            css_class='deform novaideo-ajax-form')


@view_config(
    name='contact',
    context=Entity,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class ContactMultipleView(MultipleView):
    title = _('Contact')
    name = 'contact'
    viewid = 'contact'
    template = 'pontus:templates/views_templates/simple_multipleview.pt'
    views = (ContactStudyReport, ContactForm)
    validators = [Contact.get_validator()]

    def before_update(self):
        if len(self.validated_children) == 1:
            self.validated_children[0].wrapper_template = 'pontus:templates/views_templates/simple_view_wrapper.pt'

        super(ContactMultipleView, self).before_update()


DEFAULTMAPPING_ACTIONS_VIEWS.update({Contact: ContactMultipleView})
