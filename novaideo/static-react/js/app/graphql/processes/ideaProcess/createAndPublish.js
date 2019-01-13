import update from 'immutability-helper';

import { ACTIONS, STATE } from '../../../processes';
import { truncateText } from '../../../utils/globalFunctions';

export default function createAndPublish({ ownProps, mutate }) {
  return ({
    context, plainText, text, title, keywords, attachedFiles, oldFiles, anonymous, account
  }) => {
    const { formData, globalProps: { site } } = ownProps;
    const files = attachedFiles.length > 0
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
    const ideaState = site.moderateIdeas ? [STATE.idea.submitted] : [STATE.idea.published];
    if (site.moderateIdeas && site.supportIdeas) {
      ideaState.splice(0, 0, STATE.idea.submittedSupport);
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
        createAndPublish: {
          __typename: 'CreateAndPublish',
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
            state: ideaState,
            channel: {
              __typename: 'Channel',
              id: 'channel-id',
              oid: 'channel-oid',
              title: title,
              isDiscuss: false
            },
            opinion: '',
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
                    ...account.picture
                  }
                  : null
            },
            actions: [],
            urls: []
          }
        }
      },
      updateQueries: {
        IdeasList: (prev, { mutationResult }) => {
          const newIdea = mutationResult.data.createAndPublish.idea;
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
          const newIdea = mutationResult.data.createAndPublish.idea;
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