import update from 'immutability-helper';
import gql from 'graphql-tag';

export const addPrivateChannelMutation = gql`
  mutation($context: String!) {
    addPrivateChannel(context: $context) {
      status
      channel {
        id
        oid
        title
        lenUnreadComments
        subject {
          ... on Person {
            id
            oid
            picture {
              url
            }
          }
        }
      }
    }
  }
`;

export default function addPrivateChannel({ mutate }) {
  return ({ context }) => {
    return mutate({
      variables: { context: context.oid },
      optimisticResponse: {
        __typename: 'Mutation',
        addPrivateChannel: {
          __typename: 'AddPrivateChannel',
          status: true,
          channel: {
            __typename: 'Channel',
            id: `channel-${context.id}`,
            oid: `channel-${context.id}`,
            title: context.title,
            lenUnreadComments: 0,
            subject: context
          }
        }
      },
      updateQueries: {
        Discussions: (prev, { mutationResult }) => {
          const newChannel = mutationResult.data.addPrivateChannel.channel;
          if (!newChannel) return false;
          return update(prev, {
            account: {
              discussions: {
                edges: {
                  $unshift: [
                    {
                      __typename: 'Channel',
                      node: newChannel
                    }
                  ]
                }
              }
            }
          });
        }
      }
    });
  };
}