import update from 'immutability-helper';

import { PROCESSES } from '../../../processes';

export default function share({ mutate }) {
  return ({
    context, message, subject, members
  }) => {
    return mutate({
      variables: {
        context: context.oid,
        message: message,
        subject: subject,
        members: members
      },
      optimisticResponse: {
        __typename: 'Mutation',
        share: {
          __typename: 'Share',
          idea: {
            id: context.id,
            __typename: context.__typename,
          }
        }
      },
      updateQueries: {
        IdeasList: (prev) => {
          const processNodes = PROCESSES.ideamanagement.nodes;
          const currentIdea = prev.ideas.edges.filter((item) => {
            return item && item.node.id === context.id;
          })[0];
          if (!currentIdea) return false;
          const currentAction = currentIdea.node.actions.find((action) => {
            return action.nodeId === processNodes.share.nodeId;
          });
          if (!currentAction) return false;
          const indexAction = currentIdea.node.actions.indexOf(currentAction);
          const newIdea = update(currentIdea, {
            node: {
              actions: {
                $splice: [[indexAction, 1, { ...currentAction, counter: currentAction.counter + members.length }]]
              }
            }
          });
          const index = prev.ideas.edges.indexOf(currentIdea);
          return update(prev, {
            ideas: {
              edges: {
                $splice: [[index, 1, newIdea]]
              }
            }
          });
        },
        Idea: (prev, { queryVariables }) => {
          if (queryVariables.id !== context.id) return false;
          const processNodes = PROCESSES.ideamanagement.nodes;
          const currentAction = prev.node.actions.find((action) => {
            return action.nodeId === processNodes.share.nodeId;
          });
          if (!currentAction) return false;
          const indexAction = prev.node.actions.indexOf(currentAction);
          return update(prev, {
            node: {
              actions: {
                $splice: [[indexAction, 1, { ...currentAction, counter: currentAction.counter + members.length }]]
              }
            }
          });
        }
      }
    });
  };
}