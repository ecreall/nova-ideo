
from dace.objectofcollaboration.principal.util import Anonymous

from novaideo.content.novaideo_application import NovaIdeoApplication


def homepage_connected_condition(context, user):
    return not isinstance(user, Anonymous)


GUIDE_TOUR_PAGES = {
    (NovaIdeoApplication, 'any', ''):
        (homepage_connected_condition, {
         'guide': 'novaideo_home',
         'page': 'index',
         'css_links': [],
         'js_links': ['novaideo:static/guideline/js/pages/home.js']
         })
}


def get_guide_tour_page(request, context, user, view_name):
    pages = [GUIDE_TOUR_PAGES.get(
             (context.__class__, s, view_name), None)
             for s in context.state]
    pages.append(GUIDE_TOUR_PAGES.get(
        (context.__class__, 'any', view_name), None))
    pages = [p for p in pages if p is not None and p[0](context, user)]
    return pages[0][1] if pages else {}
