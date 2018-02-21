import update from 'immutability-helper';
import { gql } from 'react-apollo';

import { actionFragment } from '../../queries';
import { ACTIONS } from '../../../processes';

export const opposeMutation = gql`
  mutation($context: String!, $actionTags: [String]) {
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
        actions(actionTags: $actionTags) {
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
      variables: { context: context.oid, actionTags: [ACTIONS.primary] },
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
        IdeasList: (prev, { mutationResult }) => {
          const newIdea = mutationResult.data.opposeIdea.idea;
          const currentIdea = prev.ideas.edges.filter((item) => {
            return item && item.node.id === newIdea.id;
          })[0];
          if (!currentIdea) return prev;
          const index = prev.ideas.edges.indexOf(currentIdea);
          return update(prev, {
            ideas: {
              edges: {
                $splice: [[index, 1, { __typename: 'Idea', node: { ...currentIdea.node, ...newIdea } }]]
              }
            }
          });
        },
        Idea: (prev, { mutationResult, queryVariables }) => {
          const newIdea = mutationResult.data.opposeIdea.idea;
          if (queryVariables.id !== context.id) return false;
          return update(prev, {
            idea: {
              tokensSupport: { $set: newIdea.tokensSupport },
              tokensOpposition: { $set: newIdea.tokensOpposition },
              userToken: { $set: newIdea.userToken },
              actions: {
                $set: newIdea.actions
              }
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