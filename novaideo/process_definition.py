from zope.interface import Interface

from pyramid.view import view_config

from dace.processdefinition.processdef import ProcessDefinition
from dace.processdefinition.activitydef import ActivityDefinition
from dace.processdefinition.transitiondef import TransitionDefinition
from dace.processdefinition.eventdef import (
    StartEventDefinition,
    EndEventDefinition)
from dace.objectofcollaboration.services.processdef_container import (
    process_definition)
from dace.processinstance.activity import ElementaryAction
from dace.util import getAllBusinessAction

# Step 1
class MyBehavior(ElementaryAction):
    context = Interface

    def start(self, context, request, appstruct, **kw):
        # Your code hear
        return {'message': 'Hello world!'}


# Step 2
@process_definition(
    id='myprocessid',
    name='myprocessid',
    title='My process')
class MyProcess(ProcessDefinition):

    def _init_definition(self):
        # define process nodes
        self.defineNodes(
            # start node: the beginning of the process
            start=StartEventDefinition(),
            # hello node
            hello=ActivityDefinition(
                # MyBehavior is the behavior to execute
                # when the node is called
                contexts=[MyBehavior],
                description='Hello behavior',
                title='Hello!'),
            # end node: the ending of the process
            end=EndEventDefinition(),
        )
        # define transitions between process nodes
        self.defineTransitions(
            TransitionDefinition('start', 'hello'),
            TransitionDefinition('hello', 'end'),
        )


# Step 3
@view_config(name='my_process', renderer='json')
def my_process_view(request):
    # Recuperate all of behaviors in all of process
    # instances with id equal to 'myprocessid'
    process_actions = getAllBusinessAction(
        request.root, request,
        process_id='myprocessid')
    action_title = None
    excution = None
    process_id = None
    if process_actions:
        # Get the first action
        action_to_execute = process_actions[0]
        # Get action title
        action_title = action_to_execute.node.title
        # Excute the first action
        result = action_to_execute.execute(
            request.root, request, {})
        # Get the execution result of the behavior.
        # See 'start' method of MyBehavior class
        excution = result.get('message', None)
        # Get the process instance id
        process_id = action_to_execute.process.__name__

    return {'action title': action_title,
            'message': excution,
            'process id': process_id}
