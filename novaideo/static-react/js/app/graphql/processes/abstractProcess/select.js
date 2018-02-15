/* eslint-disable no-underscore-dangle */
import update from 'immutability-helper';
import { gql } from 'react-apollo';

import { actionFragment } from '../../queries';
import { filterActions } from '../../../utils/entities';
import { PROCESSES } from '../../../constants';

export const selectMutation = gql`
  mutation($context: String!, $processId: String, $nodeIds: [String!]) {
    select(context: $context) {
      status
      context {
        ... on IEntity {
          id
          oid
          actions(processId: $processId, nodeIds: $nodeIds) {
            ...action
          }
        }
      }
    }
  }
  ${actionFragment}
`;

export default function select({ mutate }) {
  return ({ context }) => {
    const selectAction = filterActions(context.actions, {
      behaviorId: PROCESSES.novaideoabstractprocess.nodes.select.nodeId
    })[0];
    const indexAction = context.actions.indexOf(selectAction);
    const newAction = update(selectAction, {
      counter: { $set: selectAction.counter + 1 },
      nodeId: { $set: 'deselect' },
      behaviorId: { $set: 'deselect' },
      icon: { $set: 'glyphicon glyphicon-star' }
    });
    const optimisticContext = update(context, {
      actions: {
        $set: [newAction]
      }
    });
    return mutate({
      variables: { context: context.oid, processId: 'novaideoabstractprocess', nodeIds: ['deselect'] },
      optimisticResponse: {
        __typename: 'Mutation',
        select: {
          __typename: 'Select',
          status: true,
          context: {
            ...optimisticContext
          }
        }
      },
      updateQueries: {
        MyFollowings: (prev, { mutationResult }) => {
          const newActions = mutationResult.data.select.context.actions;
          const totalCount = prev.account.followedIdeas.totalCount + 1;
          const newContext = update(context, {
            actions: {
              $splice: [[indexAction, 1, ...newActions]]
            }
          });
          return update(prev, {
            account: {
              followedIdeas: {
                totalCount: { $set: totalCount },
                edges: {
                  $unshift: [
                    {
                      __typename: newContext.__typename,
                      node: { ...newContext }
                    }
                  ]
                }
              }
            }
          });
        },
        IdeasList: (prev, { mutationResult }) => {
          const newContext = mutationResult.data.select.context;
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
        }
      }
    });
  };
}