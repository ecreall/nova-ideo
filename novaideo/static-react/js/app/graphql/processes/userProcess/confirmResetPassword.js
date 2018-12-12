export default function confirmResetPassword({ mutate }) {
  return ({ context, password }) => {
    return mutate({
      variables: {
        context: context,
        password: password
      }
    });
  };
}