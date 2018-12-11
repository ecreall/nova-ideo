import update from 'immutability-helper';

import { ACTIONS } from '../../../processes';

export default function publish({ mutate }) {
  return ({ context }) => {
    return mutate({
      variables: {
        context: context.oid,
        actionTags: [ACTIONS.primary],
        processIds: [],
        nodeIds: [],
        processTags: []
      },
      optimisticResponse: {
        __typename: 'Mutation',
        publishIdea: {
          __typename: 'PublishIdea',
          status: true,
          idea: {
            ...context,
            state: ['published', 'submitted_support'],
            actions: []
          }
        }
      },
      updateQueries: {
        IdeasList: (prev, { mutationResult }) => {
          const newIdea = mutationResult.data.publishIdea.idea;
          const currentIdea = prev.ideas.edges.filter((item) => {
            return item && item.node.id === newIdea.id;
          })[0];
          if (!currentIdea) return false;
          const index = prev.ideas.edges.indexOf(currentIdea);
          return update(prev, {
            ideas: {
              edges: {
                $splice: [[index, 1, { __typename: 'Idea', node: newIdea }]]
              }
            }
          });
        },
        Idea: (prev, { mutationResult, queryVariables }) => {
          const newIdea = mutationResult.data.publishIdea.idea;
          if (queryVariables.id !== context.id) return false;
          return update(prev, {
            idea: {
              actions: { $set: newIdea.actions },
              state: { $set: newIdea.state }
            }
          });
        },
        Comments: (prev, { mutationResult, queryVariables }) => {
          const newIdea = mutationResult.data.publishIdea.idea;
          const channelId = newIdea.channel.id;
          if (queryVariables.id !== channelId) return false;
          return update(prev, {
            node: {
              subject: {
                actions: { $set: newIdea.actions }
              }
            }
          });
        }
      }
    });
  };
}