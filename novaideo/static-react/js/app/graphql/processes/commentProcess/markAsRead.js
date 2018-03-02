import update from 'immutability-helper';
import { gql } from 'react-apollo';

export const markAsReadMutation = gql`
  mutation($context: String!) {
    markAsRead(context: $context) {
      status
    }
  }
`;

export default function markAsRead({ mutate }) {
  return ({ context, isDiscussion }) => {
    const channelId = context.id;
    return mutate({
      variables: { context: context.oid },
      updateQueries: {
        Comments: (prev) => {
          const currentComment = prev.node.comments.edges.filter((item) => {
            return item && item.node.id === channelId;
          })[0];
          if (!currentComment) return false;
          const index = prev.node.comments.edges.indexOf(currentComment);
          const newComment = update(currentComment, {
            node: {
              lenUnreadReplies: {
                $set: 0
              }
            }
          });
          return update(prev, {
            node: {
              comments: {
                edges: {
                  $splice: [[index, 1, newComment]]
                }
              }
            }
          });
        },
        Channels: (prev) => {
          if (isDiscussion) return false;
          const currentChannel = prev.account.channels.edges.filter((item) => {
            return item && item.node.id === channelId;
          })[0];
          if (!currentChannel) return false;
          const index = prev.account.channels.edges.indexOf(currentChannel);
          const newChannel = update(currentChannel, {
            node: {
              lenUnreadComments: {
                $set: 0
              }
            }
          });
          return update(prev, {
            account: {
              channels: {
                edges: {
                  $splice: [[index, 1, newChannel]]
                }
              }
            }
          });
        },
        Discussions: (prev) => {
          if (!isDiscussion) return false;
          const currentChannel = prev.account.discussions.edges.filter((item) => {
            return item && item.node.id === channelId;
          })[0];
          if (!currentChannel) return false;
          const index = prev.account.discussions.edges.indexOf(currentChannel);
          const newChannel = update(currentChannel, {
            node: {
              lenUnreadComments: {
                $set: 0
              }
            }
          });
          return update(prev, {
            account: {
              discussions: {
                edges: {
                  $splice: [[index, 1, newChannel]]
                }
              }
            }
          });
        }
      }
    });
  };
}