from dace.util import find_catalog
from pyramid.view import view_config

from novaideo.content.interface import (
    IPerson,
    Iidea,
    IQuestion,
    IChallenge,
    IProposal,
    INovaIdeoApplication)


@view_config(name='stats', context=INovaIdeoApplication, renderer='json')
def site_data(context, request):
    counts = {}
    dace_catalog = find_catalog('dace')
    novaideo_catalog = find_catalog('novaideo')
    created_at_index = novaideo_catalog['created_at']
    states_index = dace_catalog['object_states']
    object_provides_index = dace_catalog['object_provides']

    latest_content = object_provides_index.any(
        (IPerson.__identifier__,
         Iidea.__identifier__,
         IQuestion.__identifier__,
         IProposal.__identifier__,
         IChallenge.__identifier__)).execute(
        ).sort(created_at_index, reverse=True).first()

    query = object_provides_index.any((IPerson.__identifier__,)) & \
        states_index.notany(['deactivated'])
    counts['members'] = len(query.execute())

    query = object_provides_index.any((Iidea.__identifier__,)) & \
        states_index.any(['published'])
    counts['ideas'] = len(query.execute())

    counts['questions'] = 0
    if 'question' in request.content_to_manage:
        query = object_provides_index.any((IQuestion.__identifier__,)) & \
            states_index.any(['published'])
        counts['questions'] = len(query.execute())

    counts['proposals'] = 0
    if 'proposal' in request.content_to_manage:
        query = object_provides_index.any((IProposal.__identifier__,)) & \
            states_index.notany(['archived', 'draft'])
        counts['proposals'] = len(query.execute())

    counts['challenges'] = 0
    if 'challenge' in request.content_to_manage:
        query = object_provides_index.any((IChallenge.__identifier__,)) & \
            states_index.any(['published'])
        counts['challenges'] = len(query.execute())

    result = {'counts': counts}
    root = request.root
    logo = getattr(root, 'picture', None)
    result["logoUrl"] = logo.url if logo else \
        request.static_url('novaideo:static/images/novaideo_logo.png')
    result["latestContentCreatedDate"] = latest_content.created_at.strftime('%Y-%m-%d') if latest_content is not None else None
    result["creationDate"] = root.created_at.strftime('%Y-%m-%d')
    result["title"] = root.title
    result["url"] = request.resource_url(root, '')
    result["description"] = root.description
    result["type"] = 'private' if \
        getattr(root, 'only_for_members', False) else 'public'
    config = {}
    config["moderate_proposals"] = root.moderate_proposals
    config["moderate_ideas"] = root.moderate_ideas
    config["examine_proposals"] = root.examine_proposals
    config["examine_ideas"] = root.examine_ideas
    config["support_proposals"] = root.support_proposals
    config["support_ideas"] = root.support_ideas
    config["manage_challenges"] = root.manage_challenges
    config["manage_questions"] = root.manage_questions
    config["manage_proposals"] = root.manage_proposals
    result['config'] = config
    return result
