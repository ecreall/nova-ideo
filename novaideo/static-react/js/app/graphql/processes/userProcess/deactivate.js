import update from 'immutability-helper';

import { filterActions } from '../../../utils/processes';

export default function deactivate({ mutate }) {
  return ({ context }) => {
    return mutate({
      variables: {
        context: context.oid
      },
      optimisticResponse: {
        __typename: 'Mutation',
        deactivate: {
          __typename: 'Deactivate',
          status: true,
          profile: {
            id: context.id,
            actions: [],
            __typename: 'Person'
          }
        }
      },
      updateQueries: {
        Actions: (prev, { mutationResult, queryVariables }) => {
          if (queryVariables.context !== context.oid || !mutationResult.data.deactivate.status) return prev;
          let actions = mutationResult.data.deactivate.profile.actions;
          actions = filterActions(actions, {
            tags: queryVariables.actionTags,
            nodeId: queryVariables.nodeIds,
            processId: queryVariables.processIds
          });
          actions = actions.map((action) => {
            return { node: action, __typename: 'ActionEdge' };
          });
          return update(prev, {
            actions: {
              edges: {
                $set: actions
              }
            }
          });
        },
        ProfileParameters: (prev, { mutationResult, queryVariables }) => {
          if (queryVariables.id !== context.id || !mutationResult.data.deactivate.status) return false;
          let actions = mutationResult.data.deactivate.profile.actions;
          actions = filterActions(actions, {
            tags: queryVariables.actionTags,
            nodeId: queryVariables.nodeIds,
            processId: queryVariables.processIds
          });
          return update(prev, {
            person: {
              actions: {
                $set: actions
              }
            }
          });
        },
        Person: (prev, { mutationResult, queryVariables }) => {
          if (queryVariables.id !== context.id || !mutationResult.data.deactivate.status) return false;
          let actions = mutationResult.data.deactivate.profile.actions;
          actions = filterActions(actions, {
            tags: queryVariables.actionTags,
            nodeId: queryVariables.nodeIds,
            processId: queryVariables.processIds
          });
          return update(prev, {
            person: {
              actions: {
                $set: actions
              }
            }
          });
        },
        PersonData: (prev, { mutationResult, queryVariables }) => {
          if (queryVariables.id !== context.id || !mutationResult.data.deactivate.status) return false;
          let actions = mutationResult.data.deactivate.profile.actions;
          actions = filterActions(actions, {
            tags: queryVariables.actionTags,
            nodeId: queryVariables.nodeIds,
            processId: queryVariables.processIds
          });
          return update(prev, {
            person: {
              actions: {
                $set: actions
              }
            }
          });
        }
      }
    });
  };
}