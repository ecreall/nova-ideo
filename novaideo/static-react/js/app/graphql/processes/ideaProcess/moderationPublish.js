import { ACTIONS } from '../../../processes';
import { updateQueries } from './publish';

export default function moderationPublish({ mutate }) {
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
        moderationPublishIdea: {
          __typename: 'ModerationPublishIdea',
          status: true,
          idea: {
            ...context,
            state: ['published', 'submitted_support'],
            actions: []
          }
        }
      },
      updateQueries: updateQueries(context, 'moderationPublishIdea')
    });
  };
}