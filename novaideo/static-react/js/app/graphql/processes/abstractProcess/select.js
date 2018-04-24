/* eslint-disable no-underscore-dangle */
import update from 'immutability-helper';

import { filterActions } from '../../../utils/processes';
import { PROCESSES } from '../../../processes';

export default function select({ mutate }) {
  return ({ context }) => {
    const abstractProcess = PROCESSES.novaideoabstractprocess;
    const selectAction = filterActions(context.actions, {
      behaviorId: abstractProcess.nodes.select.nodeId
    })[0];
    const nodeId = abstractProcess.nodes.deselect.nodeId;
    const indexAction = context.actions.indexOf(selectAction);
    const newAction = update(selectAction, {
      counter: { $set: selectAction.counter + 1 },
      nodeId: { $set: nodeId },
      behaviorId: { $set: nodeId },
      icon: { $set: 'glyphicon glyphicon-star' },
      active: { $set: true }
    });
    const optimisticContext = update(context, {
      actions: {
        $set: [newAction]
      }
    });
    return mutate({
      variables: { context: context.oid, processIds: [abstractProcess.id], nodeIds: [nodeId] },
      optimisticResponse: {
        __typename: 'Mutation',
        select: {
          __typename: 'Select',
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
          const newContext = mutationResult.data.select.context;
          if (newContext.__typename !== 'Idea') return false;
          return update(prev, {
            account: {
              followedIdeas: {
                totalCount: { $set: prev.account.followedIdeas.totalCount + 1 },
                edges: {
                  $unshift: [
                    {
                      __typename: context.__typename,
                      node: {
                        __typename: context.__typename,
                        id: context.id,
                        oid: context.oid,
                        createdAt: context.createdAt,
                        title: context.title,
                        state: context.state || []
                      }
                    }
                  ]
                }
              }
            }
          });
        },
        IdeasList: (prev, { mutationResult }) => {
          const newContext = mutationResult.data.select.context;
          if (newContext.__typename !== 'Idea') return false;
          const newActions = newContext.actions;
          const currentIdea = prev.ideas.edges.filter((item) => {
            return item && item.node.id === newContext.id;
          })[0];
          if (!currentIdea) return false;
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
        PersonData: (prev, { mutationResult, queryVariables }) => {
          if (queryVariables.id !== context.id) return false;
          const newContext = mutationResult.data.select.context;
          const newActions = newContext.actions;
          return update(prev, {
            person: {
              nbFollowers: { $set: selectAction.counter + 1 },
              actions: {
                $splice: [[indexAction, 1, ...newActions]]
              }
            }
          });
        },
        Idea: (prev, { mutationResult, queryVariables }) => {
          const newContext = mutationResult.data.select.context;
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