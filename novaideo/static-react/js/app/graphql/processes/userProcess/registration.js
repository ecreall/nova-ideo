export default function registration({ mutate }) {
  return ({
    firstName, lastName, email, password
  }) => {
    return mutate({
      variables: {
        firstName: firstName,
        lastName: lastName,
        email: email,
        password: password
      },
      optimisticResponse: {
        __typename: 'Mutation',
        registration: {
          __typename: 'Registration',
          status: true
        }
      }
    });
  };
}