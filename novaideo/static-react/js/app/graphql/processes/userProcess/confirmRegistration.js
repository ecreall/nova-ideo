export default function confirmRegistration({ mutate }) {
  return ({ registration }) => {
    return mutate({
      variables: {
        registration: registration
      }
    });
  };
}