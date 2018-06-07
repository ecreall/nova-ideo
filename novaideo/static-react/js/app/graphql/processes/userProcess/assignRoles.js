import update from 'immutability-helper';

export default function assignRoles({ mutate }) {
  return ({ context, roles }) => {
    return mutate({
      variables: {
        context: context.oid,
        roles: roles
      },
      optimisticResponse: {
        __typename: 'Mutation',
        assignRoles: {
          __typename: 'AssignRoles',
          status: true,
          roles: roles
        }
      },
      updateQueries: {
        ProfileParameters: (prev, { queryVariables, mutationResult }) => {
          if (queryVariables.id !== context.id) return false;
          if (!mutationResult.data.assignRoles.status) return false;
          const roles = mutationResult.data.assignRoles.roles;
          return update(prev, {
            person: {
              roles: { $set: roles }
            }
          });
        }
      }
    });
  };
}