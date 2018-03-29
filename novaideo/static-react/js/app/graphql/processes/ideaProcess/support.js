import update from 'immutability-helper';
import gql from 'graphql-tag';

import { actionFragment } from '../../queries';
import { ACTIONS } from '../../../processes';

export const supportMutation = gql`
  mutation($context: String!, $actionTags: [String]) {
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
        actions(actionTags: $actionTags) {
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
      variables: { context: context.oid, actionTags: [ACTIONS.primary] },
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
        IdeasList: (prev, { mutationResult }) => {
          const newIdea = mutationResult.data.supportIdea.idea;
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
          const newIdea = mutationResult.data.supportIdea.idea;
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