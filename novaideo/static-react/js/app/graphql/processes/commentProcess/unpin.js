/* eslint-disable no-underscore-dangle */
import update from 'immutability-helper';
import { gql } from 'react-apollo';

import { PROCESSES } from '../../../processes';

export const unpinMutation = gql`
  mutation($context: String!) {
    unpinComment(context: $context) {
      status
      context {
        ... on Comment {
          id
          oid
          pinned
        }
      }
    }
  }
`;

export default function unpinComment({ mutate }) {
  return ({ context }) => {
    const commentProcess = PROCESSES.commentmanagement;
    const nodeId = commentProcess.nodes.pin.nodeId;
    const optimisticContext = update(context, {
      pinned: { $set: false }
    });
    return mutate({
      variables: { context: context.oid },
      optimisticResponse: {
        __typename: 'Mutation',
        unpinComment: {
          __typename: 'UnpinComment',
          status: true,
          context: {
            ...optimisticContext
          }
        }
      },
      updateQueries: {
        Actions: (prev, { mutationResult, queryVariables }) => {
          if (queryVariables.context !== context.oid || !mutationResult.data.unpinComment.status) return prev;
          const currentAction = prev.actions.edges.filter((item) => {
            return item && item.node.nodeId === commentProcess.nodes.unpin.nodeId;
          })[0];
          if (!currentAction) return prev;
          const newAction = update(currentAction, {
            node: {
              nodeId: { $set: nodeId },
              behaviorId: { $set: nodeId },
              icon: { $set: 'typcn typcn-pin' }
            }
          });
          const index = prev.actions.edges.indexOf(currentAction);
          return update(prev, {
            actions: {
              edges: {
                $splice: [[index, 1, newAction]]
              }
            }
          });
        },
        Comments: (prev, { mutationResult, queryVariables }) => {
          if (queryVariables.id !== context.channel.id) return false;
          const newContext = mutationResult.data.unpinComment.context;
          const currentComment = prev.node.comments.edges.filter((item) => {
            return item && item.node.id === context.id;
          })[0];
          if (!currentComment) return false;
          const newComment = update(currentComment, {
            node: {
              pinned: { $set: newContext.pinned }
            }
          });
          const index = prev.node.comments.edges.indexOf(currentComment);
          return update(prev, {
            node: {
              comments: {
                edges: {
                  $splice: [[index, 1, newComment]]
                }
              }
            }
          });
        }
      }
    });
  };
}