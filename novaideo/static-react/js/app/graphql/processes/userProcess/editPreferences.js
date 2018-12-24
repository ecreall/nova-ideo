import update from 'immutability-helper';

export default function editPreferences({ mutate }) {
  return ({ connectedUser, context, preferences }) => {
    const isConnectedUser = connectedUser.id === context.id;
    const oldPreferences = isConnectedUser ? connectedUser.preferences : {};
    const formattedPreferences = { ...preferences, theme: { ...preferences.theme, __typename: 'ThemePreferences' } };
    return mutate({
      variables: { context: context.oid, preferences: preferences },
      optimisticResponse: {
        __typename: 'Mutation',
        editPreferences: {
          __typename: 'EditPreferences',
          profile: {
            __typename: 'Person',
            id: context.id,
            preferences: { ...oldPreferences, ...formattedPreferences }
          }
        }
      },
      updateQueries: {
        SiteData: (prev, { mutationResult }) => {
          if (!isConnectedUser) return false;
          return update(prev, {
            account: {
              preferences: { $set: mutationResult.data.editPreferences.profile.preferences }
            }
          });
        }
      }
    });
  };
}