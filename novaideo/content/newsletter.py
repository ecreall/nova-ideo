# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import deform
import colander
import datetime
import pytz
from persistent.dict import PersistentDict
from zope.interface import implementer

from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer

from dace.descriptors import (
    SharedUniqueProperty,
    CompositeUniqueProperty)
from dace.objectofcollaboration.entity import Entity
from pontus.core import VisualisableElement, VisualisableElementSchema
from pontus.widget import (
    RichTextWidget)
from pontus.file import (
    File, ObjectData as ObjectDataOrigine, OBJECT_DATA)
from pontus.schema import omit, select, Schema

from .interface import INewsletter
from novaideo import _, log
from novaideo.content import get_file_widget
from novaideo.views.widget import SimpleMappingtWidget
from novaideo.utilities.util import gen_random_token


REC_DEFAULT = {
    'days': 7,
}


class ObjectData(ObjectDataOrigine):

    def clean_cstruct(self, node, cstruct):
        result, appstruct, hasevalue = super(ObjectData, self)\
            .clean_cstruct(node, cstruct)

        if 'working_params_conf' in result:
            work_conf = result.pop('working_params_conf')
            if 'content_template' in work_conf and work_conf['content_template'] and \
               OBJECT_DATA in work_conf['content_template']:
                work_conf['content_template'] = work_conf['content_template'][OBJECT_DATA]

            result.update(work_conf)

        if 'rec_conf' in result:
            rec_conf = result.pop('rec_conf')
            result.update(rec_conf)

        return result, appstruct, hasevalue


@colander.deferred
def default_content(node, kw):
    context = node.bindings['context']
    return context.get_content_template()


@colander.deferred
def default_subject(node, kw):
    context = node.bindings['context']
    return context.title


def context_is_a_newsletter(context, request):
    return request.registry.content.istype(context, 'newsletter')


class NewsletterRecConf(Schema):
    """Schema for newsletter conf"""

    recurrence = colander.SchemaNode(
        colander.Boolean(),
        widget=deform.widget.CheckboxWidget(),
        label=_('Recurring automatic sending'),
        description=_('Activate the automatic sending'),
        title='',
        missing=False
        )

    sending_date = colander.SchemaNode(
        colander.Date(),
        title=_('Next sending date')
        )

    recurrence_nb = colander.SchemaNode(
        colander.Int(),
        title=_('Frequency/days'),
        default=7
        )


class NewsletterWorkingParamConf(Schema):
    """Schema for newsletter conf"""

    automatic_registration = colander.SchemaNode(
        colander.Boolean(),
        widget=deform.widget.CheckboxWidget(),
        label=_('Automatic subscription'),
        description=_('Automatic subscription at user registration'),
        title='',
        missing=True
        )

    propose_to_registration = colander.SchemaNode(
        colander.Boolean(),
        widget=deform.widget.CheckboxWidget(),
        label=_('Propose for subscription'),
        description=_('Allow users to subscribe manually'),
        title='',
        missing=True
        )

    allow_unsubscribing = colander.SchemaNode(
        colander.Boolean(),
        widget=deform.widget.CheckboxWidget(),
        label=_('Allow unsubscription'),
        description=_('Allow users to unsubscribe'),
        title='',
        missing=True
        )

    content_template = colander.SchemaNode(
        ObjectDataOrigine(File),
        widget=get_file_widget(file_extensions=['html']),
        title=_('Content template'),
        missing=None,
        description=_("Only HTML files are supported."),
        )


@colander.deferred
def content_validator(node, kw):
    context = node.bindings['context']
    if kw.find('{unsubscribeurl}') >= 0 and\
       not getattr(context, 'allow_unsubscribing', True):
        raise colander.Invalid(
            node,
            _('The content does not contain the variable "unsubscribeurl"'))


class NewsletterSchema(VisualisableElementSchema):
    """Schema for newsletter"""

    typ_factory = ObjectData

    name = NameSchemaNode(
        editing=context_is_a_newsletter,
        )

    subject = colander.SchemaNode(
        colander.String(),
        title=_('Subject'),
        default=default_subject,
        description=_('The subject of the newsletter.')
        )

    description = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.TextAreaWidget(rows=4, cols=60),
        title=_("Description")
        )

    content = colander.SchemaNode(
        colander.String(),
        validator=colander.All(
            content_validator,
            ),
        widget=RichTextWidget(),
        default=default_content,
        missing='',
        title=_("Content"),
        description=_("The content to be sent."),
        )

    working_params_conf = omit(NewsletterWorkingParamConf(
        widget=SimpleMappingtWidget(
            mapping_css_class='controled-form'
                              ' object-well default-well',
            ajax=True,
            activator_icon="glyphicon glyphicon-cog",
            activator_title=_('Configure the working parameters'))),
        ["_csrf_token_"])

    rec_conf = omit(NewsletterRecConf(
        widget=SimpleMappingtWidget(
            mapping_css_class='controled-form'
                              ' object-well default-well',
            ajax=True,
            activator_icon="glyphicon glyphicon-repeat",
            activator_title=_('Configure the recurrence'))),
        ["_csrf_token_"])


@content(
    'newsletter',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(INewsletter)
class Newsletter(VisualisableElement, Entity):
    """Newsletter class"""

    type_title = _('Newsletter')
    icon = 'glyphicon glyphicon-envelope'
    templates = {'default': 'novaideo:views/templates/newsletter_result.pt',
                 'bloc': 'novaideo:views/templates/newsletter_result.pt'}
    name = renamer()
    content_template = CompositeUniqueProperty('content_template')

    def __init__(self, **kwargs):
        super(Newsletter, self).__init__(**kwargs)
        self.set_data(kwargs)
        self.subscribed = PersistentDict()

    @property
    def working_params_conf(self):
        return self.get_data(omit(NewsletterWorkingParamConf(),
                                  '_csrf_token_'))

    @property
    def rec_conf(self):
        return self.get_data(omit(NewsletterRecConf(),
                                  '_csrf_token_'))

    def get_content_template(self):
        if self.content_template:
            try:
                return self.content_template.fp.readall().decode()
            except Exception as error:
                log.warning(error)

        return ''

    def get_sending_date(self):
        return datetime.datetime.combine(
            getattr(
                self, 'sending_date', datetime.datetime.now(tz=pytz.UTC)),
            datetime.time(0, 0, 0, tzinfo=pytz.UTC))

    def get_next_sending_date(self, date=None):
        if date is None:
            date = self.get_sending_date()

        default = REC_DEFAULT.get('days')
        nb_rec = getattr(self, 'recurrence_nb', default)
        return (date + datetime.timedelta(days=nb_rec)).replace(tzinfo=pytz.UTC)

    def validate_content(self):
        content = getattr(self, 'content', '')
        if content:
            if not getattr(self, 'allow_unsubscribing', True):
                return content.find('{unsubscribeurl}') < 0

            return True

        return False

    def reset_content(self):
        if self.content_template:
            setattr(self, 'content', self.get_content_template())

    def subscribe(self, first_name, last_name, email, id_=None):
        if not id_:
            id_ = gen_random_token()

        user_data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'id': id_,
            'title': first_name + ' ' + last_name}

        self.subscribed[email] = user_data

    def is_subscribed(self, user):
        email = getattr(user, 'email', None)
        return email and email in self.subscribed
