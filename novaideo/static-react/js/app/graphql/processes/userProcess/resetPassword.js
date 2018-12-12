export default function resetPassword({ mutate }) {
  return ({ email }) => {
    return mutate({
      variables: {
        email: email
      },
      optimisticResponse: {
        __typename: 'Mutation',
        resetPassword: {
          __typename: 'ResetPassword',
          status: true
        }
      }
    });
  };
}