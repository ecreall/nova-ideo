/* eslint-disable no-underscore-dangle */
import update from 'immutability-helper';

import { filterActions } from '../../../utils/processes';
import { PROCESSES } from '../../../processes';

export default function select({ mutate }) {
  return ({ context }) => {
    const abstractProcess = PROCESSES.novaideoabstractprocess;
    const deselectAction = filterActions(context.actions, {
      behaviorId: abstractProcess.nodes.deselect.nodeId
    })[0];
    const nodeId = abstractProcess.nodes.select.nodeId;
    const indexAction = context.actions.indexOf(deselectAction);
    const newAction = update(deselectAction, {
      counter: { $set: deselectAction.counter - 1 },
      nodeId: { $set: nodeId },
      behaviorId: { $set: nodeId },
      icon: { $set: 'glyphicon glyphicon-star-empty' }
    });
    const optimisticContext = update(context, {
      actions: {
        $set: [newAction]
      }
    });
    return mutate({
      variables: {
        context: context.oid,
        processIds: [abstractProcess.id],
        nodeIds: [nodeId]
      },
      optimisticResponse: {
        __typename: 'Mutation',
        deselect: {
          __typename: 'Deselect',
          status: true,
          context: {
            __typename: optimisticContext.__typename,
            id: optimisticContext.id,
            oid: optimisticContext.oid,
            actions: optimisticContext.actions
          }
        }
      },
      updateQueries: {
        MyFollowings: (prev, { mutationResult }) => {
          const newContext = mutationResult.data.deselect.context;
          const currentContext = prev.account.followedIdeas.edges.filter((item) => {
            return item && item.node.id === newContext.id;
          })[0];
          if (!currentContext) return false;
          const index = prev.account.followedIdeas.edges.indexOf(currentContext);
          const totalCount = prev.account.followedIdeas.totalCount - 1;
          return update(prev, {
            account: {
              followedIdeas: {
                totalCount: { $set: totalCount },
                edges: {
                  $splice: [[index, 1]]
                }
              }
            }
          });
        },
        PersonData: (prev, { mutationResult, queryVariables }) => {
          if (queryVariables.id !== context.id) return false;
          const newContext = mutationResult.data.deselect.context;
          const newActions = newContext.actions;
          return update(prev, {
            person: {
              nbFollowers: { $set: deselectAction.counter - 1 },
              actions: {
                $splice: [[indexAction, 1, ...newActions]]
              }
            }
          });
        },
        IdeasList: (prev, { mutationResult }) => {
          const newContext = mutationResult.data.deselect.context;
          if (newContext.__typename !== 'Idea') return prev;
          const newActions = newContext.actions;
          const currentIdea = prev.ideas.edges.filter((item) => {
            return item && item.node.id === newContext.id;
          })[0];
          if (!currentIdea) return prev;
          const newIdea = update(currentIdea, {
            node: {
              actions: {
                $splice: [[indexAction, 1, ...newActions]]
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
        Idea: (prev, { mutationResult, queryVariables }) => {
          const newContext = mutationResult.data.deselect.context;
          if (queryVariables.id !== context.id || newContext.__typename !== 'Idea') return false;
          const newActions = newContext.actions;
          return update(prev, {
            idea: {
              actions: {
                $splice: [[indexAction, 1, ...newActions]]
              }
            }
          });
        }
      }
    });
  };
}