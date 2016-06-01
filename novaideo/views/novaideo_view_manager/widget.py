# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import deform
from deform.widget import default_resource_registry


class SearchFormWidget(deform.widget.FormWidget):
    template = 'novaideo:views/novaideo_view_manager/templates/search_form.pt'


class SearchTextInputWidget(deform.widget.TextInputWidget):
    template = 'novaideo:views/novaideo_view_manager/templates/search_textinput.pt'
    requirements = (('live_search', None),)


default_resource_registry.set_js_resources(
    'live_search', None,
    'novaideo:static/js/live_search.js')

default_resource_registry.set_css_resources(
    'live_search', None,
    'pontus:static/select2/dist/css/select2.min.css')
