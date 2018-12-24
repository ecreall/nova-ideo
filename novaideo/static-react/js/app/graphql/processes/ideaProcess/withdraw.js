import update from 'immutability-helper';

import { ACTIONS } from '../../../processes';

export default function withdraw({ mutate }) {
  return ({ context, availableTokens }) => {
    const { tokensSupport, tokensOpposition, userToken } = context;
    return mutate({
      variables: { context: context.oid, actionTags: [ACTIONS.primary] },
      optimisticResponse: {
        __typename: 'Mutation',
        withdrawTokenIdea: {
          __typename: 'OpposeIdea',
          status: true,
          user: {
            __typename: 'Person',
            availableTokens: availableTokens + 1
          },
          idea: {
            ...context,
            tokensSupport: userToken === 'support' ? tokensSupport - 1 : tokensSupport,
            tokensOpposition: userToken === 'oppose' ? tokensOpposition - 1 : tokensOpposition,
            userToken: 'withdraw'
          }
        }
      },
      updateQueries: {
        SiteData: (prev, { mutationResult }) => {
          return update(prev, {
            account: {
              availableTokens: {
                $set: mutationResult.data.withdrawTokenIdea.user.availableTokens
              }
            }
          });
        },
        MySupports: (prev, { mutationResult }) => {
          const newIdea = mutationResult.data.withdrawTokenIdea.idea;
          const currentIdea = prev.account.supportedIdeas.edges.filter((item) => {
            return item && item.node.id === newIdea.id;
          })[0];
          const index = prev.account.supportedIdeas.edges.indexOf(currentIdea);
          const totalCount = prev.account.supportedIdeas.totalCount - 1;
          return update(prev, {
            account: {
              supportedIdeas: {
                totalCount: { $set: totalCount },
                edges: {
                  $splice: [[index, 1]]
                }
              }
            }
          });
        },
        IdeasList: (prev, { mutationResult }) => {
          const newIdea = mutationResult.data.withdrawTokenIdea.idea;
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
          const newIdea = mutationResult.data.withdrawTokenIdea.idea;
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
        }
      }
    });
  };
}