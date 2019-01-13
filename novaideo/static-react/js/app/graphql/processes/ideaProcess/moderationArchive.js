import { ACTIONS } from '../../../processes';
import { updateQueries } from './archive';

export default function moderationArchive({ mutate }) {
  return ({ context, explanation }) => {
    return mutate({
      variables: {
        context: context.oid,
        explanation: explanation,
        actionTags: [ACTIONS.primary],
        processIds: [],
        nodeIds: [],
        processTags: []
      },
      optimisticResponse: {
        __typename: 'Mutation',
        moderationArchiveIdea: {
          __typename: 'ModerationArchiveIdea',
          status: true,
          idea: {
            ...context,
            state: ['archived'],
            actions: []
          }
        }
      },
      updateQueries: updateQueries(context, 'moderationArchiveIdea')
    });
  };
}