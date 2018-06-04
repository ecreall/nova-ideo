import update from 'immutability-helper';

import { ACTIONS } from '../../../processes';
import { truncateText } from '../../../utils/globalFunctions';

export default function edit({ ownProps, mutate }) {
  return ({ context, plainText, text, title, keywords, attachedFiles, oldFiles }) => {
    const { formData } = ownProps;
    const files = formData.values.files
      ? formData.values.files.map((file, index) => {
        return {
          id: file.id || `file-id${index}`,
          oid: file.oid || `file-oid${index}`,
          title: file.name,
          url: file.preview.url,
          isImage: file.preview.type === 'image',
          variations: [],
          size: file.size || 0,
          mimetype: file.preview.type,
          __typename: 'File'
        };
      })
      : [];
    return mutate({
      variables: {
        context: context.oid,
        text: text,
        title: title,
        keywords: keywords,
        attachedFiles: attachedFiles,
        oldFiles: oldFiles,
        processIds: [],
        nodeIds: [],
        processTags: [],
        actionTags: [ACTIONS.primary]
      },
      optimisticResponse: {
        __typename: 'Mutation',
        editIdea: {
          __typename: 'EditIdea',
          status: true,
          idea: {
            ...context,
            title: title,
            keywords: keywords,
            text: text,
            presentationText: truncateText(plainText),
            attachedFiles: files
          }
        }
      },
      updateQueries: {
        IdeasList: (prev, { mutationResult }) => {
          const newContext = mutationResult.data.editIdea.idea;
          const currentIdea = prev.ideas.edges.filter((item) => {
            return item && item.node.id === context.id;
          })[0];
          if (!currentIdea) return false;
          const newIdea = update(currentIdea, {
            node: {
              text: { $set: newContext.text },
              title: { $set: newContext.title },
              attachedFiles: { $set: newContext.attachedFiles },
              keywords: { $set: newContext.keywords },
              presentationText: { $set: newContext.presentationText }
            }
          });
          const index = prev.ideas.edges.indexOf(currentIdea);
          return update(prev, {
            ideas: {
              edges: {
                $splice: [[index, 1, newIdea]]
              }
            }
          });
        },
        Idea: (prev, { mutationResult, queryVariables }) => {
          const newIdea = mutationResult.data.editIdea.idea;
          if (queryVariables.id !== context.id) return false;
          return update(prev, {
            idea: {
              text: { $set: newIdea.text },
              title: { $set: newIdea.title },
              attachedFiles: { $set: newIdea.attachedFiles },
              keywords: { $set: newIdea.keywords },
              presentationText: { $set: newIdea.presentationText }
            }
          });
        }
      }
    });
  };
}