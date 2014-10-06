import deform
from deform.widget import default_resource_registry
from pontus.widget import SequenceWidget, Select2Widget



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


class SearchContentWidget(deform.widget.MappingWidget):
    template = 'novaideo:views/templates/mapping_simple.pt'


class Select2WidgetSearch(Select2Widget):
    template = 'novaideo:views/templates/select2.pt'
    requirements = (('deform', None), ('select2search', None))

class AddIdeaWidget(deform.widget.MappingWidget):
    template = 'novaideo:views/templates/add_idea_widget.pt'
    requirements = (('deform', None), ('addnewidea', None))

default_resource_registry.set_js_resources('addnewidea', None, 'novaideo:static/js/add_new_idea.js'  )
default_resource_registry.set_js_resources('select2search', None, 'pontus.dace_ui_extension:static/select2/select2.js',
                                                                  'novaideo:static/select2_search/select2_search.js'  )
default_resource_registry.set_css_resources('select2search', None, 'pontus.dace_ui_extension:static/select2/select2.css',
                                                                  'novaideo:static/select2_search/select2_search.css'  )
