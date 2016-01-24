# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi
#
import colander

from pontus.form import FileUploadTempStore
from pontus.widget import FileWidget


def get_file_widget(**kargs):
    @colander.deferred
    def file_widget(node, kw):
        request = node.bindings['request']
        tmpstore = FileUploadTempStore(request)
        return FileWidget(
            tmpstore=tmpstore,
            **kargs
            )

    return file_widget
