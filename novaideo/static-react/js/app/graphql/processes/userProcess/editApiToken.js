import update from 'immutability-helper';

export default function editApiToken({ mutate }) {
  return ({ context, password }) => {
    return mutate({
      variables: {
        context: context.oid,
        password: password
      },
      optimisticResponse: {
        __typename: 'Mutation',
        editApiToken: {
          __typename: 'EditApiToken',
          status: true,
          apiToken: context.apiToken
        }
      },
      updateQueries: {
        ProfileParameters: (prev, { queryVariables, mutationResult }) => {
          if (queryVariables.id !== context.id) return false;
          if (!mutationResult.data.editApiToken.status) return false;
          const apiToken = mutationResult.data.editApiToken.apiToken;
          return update(prev, {
            person: {
              apiToken: { $set: apiToken }
            }
          });
        }
      }
    });
  };
}