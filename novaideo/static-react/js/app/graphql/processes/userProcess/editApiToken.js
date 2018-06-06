export default function editApiToken({ mutate }) {
  return ({ context }) => {
    return mutate({
      variables: {
        context: context.oid
      },
      optimisticResponse: {
        __typename: 'Mutation',
        EditApiToken: {
          __typename: 'EditApiToken',
          status: true,
          token: null
        }
      }
    });
  };
}