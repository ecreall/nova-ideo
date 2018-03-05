/* eslint-disable no-underscore-dangle */
import update from 'immutability-helper';
import { gql } from 'react-apollo';

export const addReactionMutation = gql`
  mutation($context: String!, $emoji: String!) {
    addReaction(context: $context, emoji: $emoji) {
      status
    }
  }
`;

const updateCommentQueries = (prev, emoji, context, user) => {
  const currentComment = prev.node.comments.edges.filter((item) => {
    return item && item.node.id === context.id;
  })[0];
  if (!currentComment) return false;

  // update the current user emoji
  let updateUserEmoji = {};
  const currentUserEmoji = currentComment.node.emojis.filter((emojiData) => {
    return emojiData.isUserEmoji;
  })[0];
  if (currentUserEmoji) {
    const currentUser = currentUserEmoji.users.filter((userData) => {
      return userData.id === user.id;
    })[0];
    const indexCurrentUser = currentUserEmoji.users.indexOf(currentUser);
    const newCurrentUserEmoji = update(currentUserEmoji, {
      isUserEmoji: { $set: false },
      users: {
        $splice: [[indexCurrentUser, 1]]
      }
    });
    const indexCurrentUserEmoji = currentComment.node.emojis.indexOf(currentUserEmoji);
    updateUserEmoji = { $splice: [[indexCurrentUserEmoji, 1, newCurrentUserEmoji]] };
  }

  const newUser = { id: user.id, title: user.title, __typename: 'Person' };
  let newEmojis = {
    title: emoji,
    users: [newUser],
    isUserEmoji: true,
    __typename: 'Emoji'
  };
  const currentEmoji = currentComment.node.emojis.filter((emojiData) => {
    return emojiData.title === emoji;
  })[0];
  let newComment = null;
  if (currentEmoji) {
    const indexEmoji = currentComment.node.emojis.indexOf(currentEmoji);
    const currentUser = currentEmoji.users.filter((userData) => {
      return userData.id === user.id;
    })[0];
    if (!currentUser) {
      newEmojis = update(currentEmoji, {
        isUserEmoji: { $set: true },
        users: {
          $push: [newUser]
        }
      });
      newComment = update(currentComment, {
        node: {
          emojis: {
            $splice: [[indexEmoji, 1, newEmojis]]
          }
        }
      });
    }
  } else {
    newComment = update(currentComment, {
      node: {
        emojis: {
          $push: [newEmojis]
        }
      }
    });
  }
  if (!newComment) {
    newComment = update(currentComment, {
      node: {
        emojis: {
          ...updateUserEmoji
        }
      }
    });
  } else {
    newComment = update(newComment, {
      node: {
        emojis: {
          ...updateUserEmoji
        }
      }
    });
  }
  const index = prev.node.comments.edges.indexOf(currentComment);
  return update(prev, {
    node: {
      comments: {
        edges: {
          $splice: [[index, 1, newComment]]
        }
      }
    }
  });
};

export default function addReaction({ mutate }) {
  return ({ context, emoji, user }) => {
    return mutate({
      variables: { context: context.oid, emoji: emoji },
      optimisticResponse: {
        __typename: 'Mutation',
        addReaction: {
          __typename: 'AddReaction',
          status: true
        }
      },
      updateQueries: {
        Comments: (prev) => {
          return updateCommentQueries(prev, emoji, context, user);
        },
        Comment: (prev) => {
          return updateCommentQueries(prev, emoji, context, user);
        }
      }
    });
  };
}