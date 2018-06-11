import update from 'immutability-helper';

import { ACTIONS } from '../../../processes';

export default function makeItsOpinion({ mutate }) {
  return ({ context, opinion, explanation }) => {
    return mutate({
      variables: { context: context.oid, opinion: opinion, explanation: explanation, actionTags: [ACTIONS.primary] },
      optimisticResponse: {
        __typename: 'Mutation',
        makeItsOpinion: {
          __typename: 'MakeItsOpinion',
          status: true,
          idea: {
            ...context,
            state: ['examined', 'published', opinion]
          }
        }
      },
      updateQueries: {
        IdeasList: (prev, { mutationResult }) => {
          const newIdea = mutationResult.data.makeItsOpinion.idea;
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
          const newIdea = mutationResult.data.makeItsOpinion.idea;
          if (queryVariables.id !== context.id) return false;
          return update(prev, {
            idea: {
              state: {
                $set: newIdea.state
              },
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