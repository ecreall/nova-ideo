# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import deform
from colander import null
from deform.widget import default_resource_registry
from pyramid.threadlocal import get_current_request
from pyramid import renderers

from pontus.widget import (
    SequenceWidget, Select2Widget,
    TextInputWidget)


class EmailInputWidget(deform.widget.TextInputWidget):
    template = 'novaideo:views/templates/email_input.pt'


class TOUCheckboxWidget(deform.widget.CheckboxWidget):
    template = 'novaideo:views/templates/terms_of_use_checkbox.pt'
    requirements = ( ('toucheckbox', None), )


class LimitedTextAreaWidget(deform.widget.TextAreaWidget):
    template = 'novaideo:views/templates/textarea.pt'
    default_alert_template = 'novaideo:views/templates/textarea_default_alert.pt'
    requirements = ( ('jquery.maskedinput', None), 
                     ('limitedtextarea', None)) 

    @property
    def alert_message(self):
        alert_values = {'limit': self.limit}
        template = self.default_alert_template
        if hasattr(self, 'alert_template'):
            template = self.alert_template

        if hasattr(self, 'alert_values'):
            alert_values = self.alert_values

        request = get_current_request()
        body = renderers.render(
               template, alert_values, request)
        return body

class MappinColgWidget(deform.widget.MappingWidget):

    template = 'novaideo:views/templates/mapping_col.pt'


class ConfirmationWidget(deform.widget.MappingWidget):
    template = 'novaideo:views/templates/confirmation_form.pt'


class InLineWidget(SequenceWidget):

    template = 'novaideo:views/templates/inline.pt'
    item_template = 'novaideo:views/templates/inline_item.pt'


class ObjectWidget(deform.widget.MappingWidget):

    template = 'novaideo:views/templates/object_mapping.pt'
    item_template = 'novaideo:views/templates/object_mapping_item.pt'


class SimpleMappingtWidget(deform.widget.MappingWidget):
    template = 'novaideo:views/templates/mapping_simple.pt'
    requirements = ( ('deform', None), ('simple_mapping', None))

class Select2WidgetSearch(Select2Widget):
    template = 'novaideo:views/templates/select2_search.pt'
    requirements = (('deform', None), ('select2search', None))


class AddIdeaWidget(deform.widget.MappingWidget):
    template = 'novaideo:views/templates/add_idea_widget.pt'
    requirements = (('deform', None), ('addnewidea', None))


class DragDropSequenceWidget(SequenceWidget):

    template = 'novaideo:views/templates/dragdrop_sequence/sequence.pt'
    item_template = 'novaideo:views/templates/dragdrop_sequence/sequence_item.pt'


class DragDropSelect2Widget(Select2Widget):
    template = 'novaideo:views/templates/dragdrop_sequence/select2.pt'
    requirements = (('deform', None), ('select2dragdrop', None))


class DragDropMappingWidget(deform.widget.MappingWidget):

    template = 'novaideo:views/templates/dragdrop_sequence/mapping.pt'
    item_template = 'novaideo:views/templates/dragdrop_sequence/mapping_item.pt'


class DateIcalWidget(TextInputWidget):
    template = 'novaideo:views/templates/date_ical.pt'
    requirements = (('jquery.maskedinput', None),
                    ('date_ical', None))


class BootstrapIconInputWidget(deform.widget.TextInputWidget):
    template = 'novaideo:views/templates/bootstrap_icon_input.pt'
    requirements = (('bootstrap_icon', None),)

    def serialize(self, field, cstruct, **kw):
        if cstruct is null:
            cstruct = ''
        elif isinstance(cstruct, dict):
            cstruct = cstruct.get('icon_class')+','+cstruct.get('icon')
        return super(BootstrapIconInputWidget, self).serialize(
                                                  field, cstruct, **kw)

    def deserialize(self, field, pstruct):
        row = super(BootstrapIconInputWidget, self).deserialize(field, pstruct)
        if row is null:
            return null

        data = row.split(',')
        try:
            return {'icon_class': data[0],
                    'icon': data[1]}
        except:
            return data


class CssWidget(TextInputWidget):
    template = 'novaideo:views/templates/style_picker.pt'
    requirements = (('jquery.maskedinput', None),
                    ('stylepicker', None))


class ReCAPTCHAWidget(deform.widget.TextInputWidget):
    template = 'novaideo:views/templates/recaptcha_input.pt'


default_resource_registry.set_js_resources('stylepicker', None,
               'novaideo:static/bgrins-spectrum/spectrum.js',
               'novaideo:static/js/style_picker.js')

default_resource_registry.set_css_resources('stylepicker', None,
              'novaideo:static/bgrins-spectrum/spectrum.css')

default_resource_registry.set_js_resources('bootstrap_icon', None,
           'novaideo:static/js/bootstrap_iconpicker.js',
           'novaideo:static/bootstrap-iconpicker/bootstrap-iconpicker/js/bootstrap-iconpicker.min.js')

default_resource_registry.set_css_resources('bootstrap_icon', None,
              'novaideo:static/bootstrap-iconpicker/bootstrap-iconpicker/css/bootstrap-iconpicker.min.css')

default_resource_registry.set_js_resources('simple_mapping', None,
               'novaideo:static/js/simple_mapping.js'  )

default_resource_registry.set_js_resources('toucheckbox', None,
               'novaideo:static/js/toucheckbox.js'  )

default_resource_registry.set_js_resources('addnewidea', None, 
                         'novaideo:static/js/add_new_idea.js'  )

default_resource_registry.set_js_resources('select2search', None, 
           'pontus:static/select2/dist/js/select2.min.js',
           'novaideo:static/select2_search/select2_search.js'  )

default_resource_registry.set_css_resources('select2search', None, 
              'pontus:static/select2/dist/css/select2.min.css',
              'novaideo:static/select2_search/select2_search.css'  )

default_resource_registry.set_js_resources('select2dragdrop', None, 
                'pontus:static/select2/dist/js/select2.min.js',
                'novaideo:static/js/dragdrop_select.js'  )

default_resource_registry.set_css_resources('select2dragdrop', None, 
                'pontus:static/select2/dist/css/select2.min.css',
                'novaideo:static/select2_search/select2_search.css'  )

default_resource_registry.set_js_resources('limitedtextarea', None, 
               'novaideo:static/limitedtextarea/limitedtextarea.js'  )

default_resource_registry.set_css_resources('limitedtextarea', None, 
              'novaideo:static/limitedtextarea/limitedtextarea.css'  )


default_resource_registry.set_js_resources('date_ical', None,
               'novaideo:static/js/date_ical.js')

default_resource_registry.set_css_resources('date_ical', None,
              'novaideo:static/css/date_ical.css')
