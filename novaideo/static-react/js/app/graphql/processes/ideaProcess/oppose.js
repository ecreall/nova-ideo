import update from 'immutability-helper';
import { gql } from 'react-apollo';

import { actionFragment } from '../../queries';

export const opposeMutation = gql`
  mutation($context: String!) {
    opposeIdea(context: $context) {
      status
      user {
        availableTokens
      }
      idea {
        id
        tokensSupport
        tokensOpposition
        userToken
        actions{
          ...action
        }
      }
    }
  }
    ${actionFragment}
`;

export default function oppose({ mutate }) {
  return ({ context, availableTokens }) => {
    const { tokensSupport, tokensOpposition, userToken } = context;
    return mutate({
      variables: { context: context.oid },
      optimisticResponse: {
        __typename: 'Mutation',
        opposeIdea: {
          __typename: 'OpposeIdea',
          status: true,
          user: {
            __typename: 'Person',
            availableTokens: availableTokens - 1
          },
          idea: {
            ...context,
            tokensOpposition: tokensOpposition + 1,
            tokensSupport: userToken === 'support' ? tokensSupport - 1 : tokensSupport,
            userToken: 'oppose'
          }
        }
      },
      updateQueries: {
        Account: (prev, { mutationResult }) => {
          return update(prev, {
            account: {
              availableTokens: { $set: mutationResult.data.opposeIdea.user.availableTokens }
            }
          });
        },
        MySupports: (prev, { mutationResult }) => {
          const newIdea = mutationResult.data.opposeIdea.idea;
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