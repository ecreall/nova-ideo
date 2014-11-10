
import deform


class SearchFormWidget(deform.widget.FormWidget):
    template = 'novaideo:views/novaideo_view_manager/templates/search_form.pt'


class SearchTextInputWidget(deform.widget.TextInputWidget):
    template = 'novaideo:views/novaideo_view_manager/templates/search_textinput.pt'
