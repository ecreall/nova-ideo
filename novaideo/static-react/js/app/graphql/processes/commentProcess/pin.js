/* eslint-disable no-underscore-dangle */
import update from 'immutability-helper';
import { gql } from 'react-apollo';

import { PROCESSES } from '../../../processes';

export const pinMutation = gql`
  mutation($context: String!) {
    pinComment(context: $context) {
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

export default function pinComment({ mutate }) {
  return ({ context }) => {
    const commentProcess = PROCESSES.commentmanagement;
    const nodeId = commentProcess.nodes.unpin.nodeId;
    const optimisticContext = update(context, {
      pinned: { $set: true }
    });
    return mutate({
      variables: { context: context.oid, processIds: [commentProcess.id], nodeIds: [nodeId] },
      optimisticResponse: {
        __typename: 'Mutation',
        pinComment: {
          __typename: 'PinComment',
          status: true,
          context: {
            ...optimisticContext
          }
        }
      },
      updateQueries: {
        Actions: (prev, { mutationResult, queryVariables }) => {
          if (queryVariables.context !== context.oid || !mutationResult.data.pinComment.status) return prev;
          const currentAction = prev.actions.edges.filter((item) => {
            return item && item.node.nodeId === commentProcess.nodes.pin.nodeId;
          })[0];
          if (!currentAction) return prev;
          const newAction = update(currentAction, {
            node: {
              nodeId: { $set: nodeId },
              behaviorId: { $set: nodeId },
              icon: { $set: 'typcn typcn-pin-outline' }
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
          if (queryVariables.pinned) {
            return update(prev, {
              node: {
                comments: {
                  totalCount: { $set: prev.node.comments.totalCount + 1 },
                  edges: {
                    $unshift: [
                      {
                        __typename: optimisticContext.__typename,
                        node: { ...optimisticContext }
                      }
                    ]
                  }
                }
              }
            });
          }
          const newContext = mutationResult.data.pinComment.context;
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