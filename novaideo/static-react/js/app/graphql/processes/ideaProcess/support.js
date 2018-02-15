import update from 'immutability-helper';
import { gql } from 'react-apollo';

import { actionFragment } from '../../queries';

export const supportMutation = gql`
  mutation($context: String!) {
    supportIdea(context: $context) {
      status
      user {
        availableTokens
      }
      idea {
        id
        tokensSupport
        tokensOpposition
        userToken
        actions {
          ...action
        }
      }
    }
  }
    ${actionFragment}
`;

export default function support({ mutate }) {
  return ({ context, availableTokens }) => {
    const { tokensSupport, tokensOpposition, userToken } = context;
    return mutate({
      variables: { context: context.oid },
      optimisticResponse: {
        __typename: 'Mutation',
        supportIdea: {
          __typename: 'SupportIdea',
          status: true,
          user: {
            __typename: 'Person',
            availableTokens: availableTokens - 1
          },
          idea: {
            ...context,
            tokensSupport: tokensSupport + 1,
            tokensOpposition: userToken === 'oppose' ? tokensOpposition - 1 : tokensOpposition,
            userToken: 'support'
          }
        }
      },
      updateQueries: {
        Account: (prev, { mutationResult }) => {
          return update(prev, {
            account: {
              availableTokens: { $set: mutationResult.data.supportIdea.user.availableTokens }
            }
          });
        },
        MySupports: (prev, { mutationResult }) => {
          const newIdea = mutationResult.data.supportIdea.idea;
          const currentIdea = prev.account.supportedIdeas.edges.filter((item) => {
            return item && item.node.id === newIdea.id;
          })[0];
          const totalCount = prev.account.supportedIdeas.totalCount + 1;
          if (!currentIdea) {
            return update(prev, {
              account: {
                supportedIdeas: {
                  totalCount: { $set: totalCount },
                  edges: {
                    $unshift: [
                      {
                        __typename: 'Idea',
                        node: { ...context, ...newIdea }
                      }
                    ]
                  }
                }
              }
            });
          }
          const index = prev.account.supportedIdeas.edges.indexOf(currentIdea);
          return update(prev, {
            account: {
              supportedIdeas: {
                totalCount: { $set: totalCount },
                edges: {
                  $splice: [
                    [
                      index,
                      1,
                      {
                        __typename: 'Idea',
                        node: { ...context, ...newIdea }
                      }
                    ]
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