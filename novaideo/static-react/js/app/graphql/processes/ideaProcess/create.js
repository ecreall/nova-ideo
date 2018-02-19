import update from 'immutability-helper';
import { gql } from 'react-apollo';

import { ideaFragment } from '../../queries';
import { ACTIONS } from '../../../processes';

export const createMutation = gql`
  mutation($text: String!, $title: String!, $keywords: [String]!, $attachedFiles: [Upload], $anonymous: Boolean,
           $processIds: [String], $nodeIds: [String], $processTags: [String], $actionTags: [String]) {
    createIdea(
      title: $title,
      keywords: $keywords,
      text: $text,
      attachedFiles: $attachedFiles,
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
  return ({ text, title, keywords, attachedFiles, anonymous, account }) => {
    const { formData } = ownProps;
    const files =
      attachedFiles.length > 0
        ? formData.values.files.map((file) => {
          return {
            url: file.preview.url,
            isImage: file.preview.type === 'image',
            variations: [],
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
        text: text,
        title: title,
        keywords: keywords,
        attachedFiles: attachedFiles,
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
            presentationText: text,
            attachedFiles: files,
            tokensSupport: 0,
            tokensOpposition: 0,
            userToken: null,
            state: ['to work'],
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