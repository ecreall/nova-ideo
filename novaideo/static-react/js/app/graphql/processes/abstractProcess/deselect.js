/* eslint-disable no-underscore-dangle */
import update from 'immutability-helper';
import { gql } from 'react-apollo';

import { actionFragment } from '../../queries';
import { filterActions } from '../../../utils/entities';
import { PROCESSES } from '../../../constants';

export const deselectMutation = gql`
  mutation($context: String!, $processId: String, $nodeIds: [String!]) {
    deselect(context: $context) {
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
    const deselectAction = filterActions(context.actions, {
      behaviorId: PROCESSES.novaideoabstractprocess.nodes.deselect.nodeId
    })[0];
    const newAction = update(deselectAction, {
      counter: { $set: deselectAction.counter - 1 },
      nodeId: { $set: 'select' },
      behaviorId: { $set: 'select' },
      icon: { $set: 'glyphicon glyphicon-star-empty' }
    });
    const optimisticContext = update(context, {
      actions: {
        $set: [newAction]
      }
    });
    return mutate({
      variables: { context: context.oid, processId: 'novaideoabstractprocess', nodeIds: ['select'] },
      optimisticResponse: {
        __typename: 'Mutation',
        deselect: {
          __typename: 'Deselect',
          status: true,
          context: {
            ...optimisticContext
          }
        }
      },
      updateQueries: {
        MyFollowings: (prev, { mutationResult }) => {
          const newContext = mutationResult.data.deselect.context;
          const currentContext = prev.account.followedIdeas.edges.filter((item) => {
            return item && item.node.id === newContext.id;
          })[0];
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
        IdeasList: (prev, { mutationResult }) => {
          const newContext = mutationResult.data.deselect.context;
          if (newContext.__typename !== 'Idea') return prev;
          const indexAction = context.actions.indexOf(deselectAction);
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