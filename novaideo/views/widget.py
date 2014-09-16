import deform
from pontus.widget import SequenceWidget



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
