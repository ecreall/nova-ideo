import update from 'immutability-helper';
import { gql } from 'react-apollo';

import { commentFragment } from '../../queries';
import { ACTIONS } from '../../../processes';

export const editMutation = gql`
  mutation($context: String!, $comment: String!, $attachedFiles: [Upload], $oldFiles: [String],
           $processIds: [String], $nodeIds: [String], $processTags: [String], $actionTags: [String]) {
    editComment(
      context: $context
      comment: $comment
      attachedFiles: $attachedFiles
      oldFiles: $oldFiles
    ) {
      status
      comment {
        ...comment
        ...on Comment {
          channel {
            id
            oid
            title
            isDiscuss
          }
        }
      }
    }
  }
  ${commentFragment}
`;

export default function edit({ ownProps, mutate }) {
  return ({ context, text, attachedFiles, oldFiles }) => {
    const { formData } = ownProps;
    const files = formData.values.files
      ? formData.values.files.map((file, index) => {
        return {
          id: file.id || `file-id${index}`,
          oid: file.oid || `file-oid${index}`,
          url: file.preview.url,
          isImage: file.preview.type === 'image',
          variations: [],
          __typename: 'File'
        };
      })
      : [];

    return mutate({
      variables: {
        context: context.oid,
        comment: text,
        attachedFiles: attachedFiles,
        oldFiles: oldFiles,
        processIds: [],
        nodeIds: [],
        processTags: [],
        actionTags: [ACTIONS.primary]
      },
      optimisticResponse: {
        __typename: 'Mutation',
        editComment: {
          __typename: 'EditComment',
          status: true,
          isNewChannel: false,
          comment: {
            ...context,
            text: text,
            attachedFiles: files,
            edited: true,
            urls: []
          }
        }
      },
      updateQueries: {
        Comments: (prev, { mutationResult, queryVariables }) => {
          const search = queryVariables.filter || queryVariables.pinned || queryVariables.file;
          if (search) return false;
          const newContext = mutationResult.data.editComment.comment;
          const currentComment = prev.node.comments.edges.filter((item) => {
            return item && item.node.id === context.id;
          })[0];
          if (!currentComment) return false;
          const newComment = update(currentComment, {
            node: {
              text: { $set: newContext.text },
              edited: { $set: newContext.edited },
              pinned: { $set: newContext.pinned },
              attachedFiles: { $set: newContext.attachedFiles },
              urls: { $set: newContext.urls }
            }
          });
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
        }
      }
    });
  };
}