import update from 'immutability-helper';
import gql from 'graphql-tag';

import { ideaFragment } from '../../queries';
import { ACTIONS, STATE } from '../../../processes';
import { truncateText } from '../../../utils/globalFunctions';

export const createMutation = gql`
  mutation($context: String, $text: String!, $title: String!, $keywords: [String]!, $attachedFiles: [Upload],
           $oldFiles: [String], $anonymous: Boolean,
           $processIds: [String], $nodeIds: [String], $processTags: [String], $actionTags: [String]) {
    createIdea(
      context: $context,
      title: $title,
      keywords: $keywords,
      text: $text,
      attachedFiles: $attachedFiles,
      oldFiles: $oldFiles,
      anonymous: $anonymous) {
      status
      idea {
        ...idea
      }
    }
  }
  ${ideaFragment}
`;

export default function create({ ownProps, mutate }) {
  return ({ context, plainText, text, title, keywords, attachedFiles, oldFiles, anonymous, account }) => {
    const { formData } = ownProps;
    const files =
      attachedFiles.length > 0
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
    const createdAt = new Date();
    let authorId = account.id;
    let authorOid = account.oid;
    let authorTitle = account.title;
    if (anonymous) {
      if (account.mask) {
        authorId = account.mask.id;
        authorOid = account.mask.oid;
        authorTitle = account.mask.title;
      } else {
        authorId = 'anonymousId';
        authorOid = 'anonymousOid';
        authorTitle = 'Anonymous';
      }
    }
    return mutate({
      variables: {
        context: context ? context.oid : '',
        text: text,
        title: title,
        keywords: keywords,
        attachedFiles: attachedFiles,
        oldFiles: oldFiles,
        anonymous: anonymous,
        processIds: [],
        nodeIds: [],
        processTags: [],
        actionTags: [ACTIONS.primary]
      },
      optimisticResponse: {
        __typename: 'Mutation',
        createIdea: {
          __typename: 'CreateIdea',
          status: true,
          idea: {
            __typename: 'Idea',
            id: '0',
            oid: '0',
            createdAt: createdAt.toISOString(),
            title: title,
            keywords: keywords,
            text: text,
            presentationText: truncateText(plainText),
            attachedFiles: files,
            tokensSupport: 0,
            tokensOpposition: 0,
            userToken: null,
            state: [STATE.idea.private],
            channel: {
              __typename: 'Channel',
              id: 'channel-id',
              oid: 'channel-oid',
              isDiscuss: false
            },
            opinion: '',
            urls: [],
            author: {
              __typename: 'Person',
              isAnonymous: anonymous,
              id: `${authorId}createidea`,
              oid: `${authorOid}createidea`,
              title: authorTitle,
              description: account.description,
              function: account.function,
              picture:
                !anonymous && account.picture
                  ? {
                    __typename: 'File',
                    url: account.picture.url
                  }
                  : null
            },
            actions: []
          }
        }
      },
      updateQueries: {
        IdeasList: (prev, { mutationResult }) => {
          const newIdea = mutationResult.data.createIdea.idea;
          return update(prev, {
            ideas: {
              edges: {
                $unshift: [
                  {
                    __typename: 'Idea',
                    node: newIdea
                  }
                ]
              }
            }
          });
        },
        MyContents: (prev, { mutationResult }) => {
          const newIdea = mutationResult.data.createIdea.idea;
          const totalCount = prev.account.contents.totalCount + 1;
          return update(prev, {
            account: {
              contents: {
                totalCount: { $set: totalCount },
                edges: {
                  $unshift: [
                    {
                      __typename: 'Idea',
                      node: newIdea
                    }
                  ]
                }
              }
            }
          });
        }
      }
    });
  };
}