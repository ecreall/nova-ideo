# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import deform


class SearchFormWidget(deform.widget.FormWidget):
    template = 'novaideo:views/novaideo_view_manager/templates/search_form.pt'


class SearchTextInputWidget(deform.widget.TextInputWidget):
    template = 'novaideo:views/novaideo_view_manager/templates/search_textinput.pt'
