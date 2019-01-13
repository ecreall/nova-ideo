import { ACTIONS } from '../../../processes';
import { updateQueries } from './publish';

export default function submit({ mutate }) {
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
        submitIdea: {
          __typename: 'SubmitIdea',
          status: true,
          idea: {
            ...context,
            state: ['submitted'],
            actions: []
          }
        }
      },
      updateQueries: updateQueries(context, 'submitIdea')
    });
  };
}