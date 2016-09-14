# Copyright (c) 2015 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

from pyramid_layout.layout import layout_config

from pontus.view import BasicView


@layout_config(name='web_services_layout', 
               template='novaideo:web_services/templates/web_services_layout.pt')
class WebServicesLayout(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request


class WebServicesJsonView(BasicView):

    def _get_pagin_data(self):
        page_limit = self.params('pageLimit')
        if page_limit is None:
            page_limit = 10
        else:
            page_limit = int(page_limit)

        current_page = self.params('page')
        if current_page is None:
            current_page = 1
        else:
            current_page = int(current_page)

        start = page_limit * (current_page - 1)
        end = start + page_limit
        return page_limit, current_page, start, end

    def __call__(self):
        operation_name = self.params('op')
        if operation_name is not None:
            operation = getattr(self, operation_name, None)
            if operation is not None:
                return operation()

        return {}
