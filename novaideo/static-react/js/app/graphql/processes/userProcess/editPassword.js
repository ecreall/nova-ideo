export default function editPassword({ mutate }) {
  return ({ context, currentPassword, password }) => {
    return mutate({
      variables: {
        context: context.oid,
        currentPassword: currentPassword,
        password: password
      },
      optimisticResponse: {
        __typename: 'Mutation',
        editPassword: {
          __typename: 'EditPassword',
          status: true
        }
      }
    });
  };
}