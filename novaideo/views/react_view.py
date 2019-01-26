
def react_view(request):
    """
    The view rendered by any react-based URL requested
    """
    return {'request': request}


def register_react_views(config, routes):
    if not routes:
        return
    for route in routes:
        config.add_view(react_view, route_name=route,
                        request_method='GET',
                        renderer='novaideo:views/templates/master.pt')


def includeme(config):
    config.add_route('react_home', '')
    config.add_route('registrations', '/registrations/*extra_path')
    config.add_route('resets', '/resets/*extra_path')
    config.add_route('messages', '/messages/*extra_path')
    config.add_route('ideas', '/ideas/*extra_path')
    config.add_route('users', '/users/*extra_path')
    config.add_route('login', '/login')
    react_routes = [
        "react_home",
        "registrations",
        "resets",
        "messages",
        "ideas",
        "users",
        "login"
    ]
    register_react_views(config, react_routes)
