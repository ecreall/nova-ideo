import update from 'immutability-helper';

export default function editProfile({ mutate }) {
  return ({
    context,
    firstName,
    lastName,
    email,
    description,
    userFunction,
    locale,
    picture,
    oldPicture,
    coverPicture,
    oldCoverPicture
  }) => {
    return mutate({
      variables: {
        context: context.oid,
        firstName: firstName,
        lastName: lastName,
        email: email,
        description: description,
        function: userFunction,
        locale: locale,
        picture: !oldPicture && picture ? [picture] : [],
        oldPicture: oldPicture,
        coverPicture: !oldCoverPicture && coverPicture ? [coverPicture] : [],
        oldCover: oldCoverPicture
      },
      optimisticResponse: {
        __typename: 'Mutation',
        editProfile: {
          __typename: 'EditProfile',
          status: true,
          profile: {
            ...context,
            title: `${firstName} ${lastName}`,
            firstName: firstName,
            lastName: lastName,
            email: email,
            description: description,
            function: userFunction,
            locale: locale,
            picture: picture && {
              id: (context.picture && context.picture.id) || picture.id || `picture-id${context.id}`,
              oid: picture.oid || `picture-oid${context.id}`,
              title: picture.name,
              url: picture.preview.url,
              isImage: true,
              variations: [],
              size: picture.size || 0,
              mimetype: picture.preview.type,
              __typename: 'File'
            },
            coverPicture: coverPicture && {
              id: (context.coverPicture && context.coverPicture.id) || coverPicture.id || `coverPicture-id${context.id}`,
              oid: coverPicture.oid || `coverPicture-oid${context.id}`,
              title: coverPicture.name,
              url: coverPicture.preview.url,
              isImage: true,
              variations: [],
              size: coverPicture.size || 0,
              mimetype: coverPicture.preview.type,
              __typename: 'File'
            }
          }
        }
      },
      updateQueries: {
        Person: (prev, { queryVariables, mutationResult }) => {
          if (queryVariables.id !== context.id) return false;
          if (!mutationResult.data.editProfile.status) return false;
          const profile = mutationResult.data.editProfile.profile;
          return update(prev, {
            person: {
              title: { $set: profile.title },
              function: { $set: userFunction },
              description: { $set: description },
              picture: context.picture && !profile.picture ? { $set: null } : { $set: profile.picture }
            }
          });
        },
        PersonData: (prev, { queryVariables, mutationResult }) => {
          if (queryVariables.id !== context.id) return false;
          if (!mutationResult.data.editProfile.status) return false;
          const profile = mutationResult.data.editProfile.profile;
          return update(prev, {
            person: {
              title: { $set: profile.title },
              firstName: { $set: firstName },
              lastName: { $set: lastName },
              function: { $set: userFunction },
              description: { $set: description },
              email: { $set: email },
              picture: context.picture && !profile.picture ? { $set: null } : { $set: profile.picture },
              coverPicture: context.coverPicture && !profile.coverPicture ? { $set: null } : { $set: profile.coverPicture }
            }
          });
        },
        ProfileParameters: (prev, { queryVariables, mutationResult }) => {
          if (queryVariables.id !== context.id) return false;
          if (!mutationResult.data.editProfile.status) return false;
          const profile = mutationResult.data.editProfile.profile;
          return update(prev, {
            person: {
              title: { $set: profile.title },
              firstName: { $set: firstName },
              lastName: { $set: lastName },
              function: { $set: userFunction },
              description: { $set: description },
              locale: { $set: locale },
              email: { $set: email },
              picture: context.picture && !profile.picture ? { $set: null } : { $set: profile.picture },
              coverPicture: context.coverPicture && !profile.coverPicture ? { $set: null } : { $set: profile.coverPicture }
            }
          });
        }
      }
    });
  };
}