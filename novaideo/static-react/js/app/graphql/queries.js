/* eslint-disable import/prefer-default-export */
import { gql } from 'react-apollo';

export const actionFragment = gql`
  fragment action on Action {
    processId
    nodeId
    behaviorId
    title
    description
    counter
    style
    descriminator
    tags
    icon
    order
  }
`;

export const siteQuery = gql`
  query Site {
    root {
      siteId
      title
      logo {
        url
      }
      keywordsRequired
      keywords
      canAddKeywords
      anonymisation
      moderateProposals
      moderateIdeas
      examineProposals
      examineIdeas
      supportProposals
      supportIdeas
      manageChallenges
      manageQuestions
      manageProposals
    }
    actions{
      edges {
        node {
          ...action
        }
      }
    }
  }
  ${actionFragment}
`;

export const accountQuery = gql`
  query Account {
    account {
      oid
      id
      title
      description
      function
      availableTokens
      mask {
        id
        oid
        title
      }
      picture {
        url
      }
    }
  }
`;

export const actionsQuery = gql`
  query Actions($context: String, $processIds: [String], $nodeIds: [String], $processTags: [String], $actionTags: [String]) {
    actions(context: $context, processIds: $processIds, nodeIds: $nodeIds, processTags: $processTags, actionTags: $actionTags) {
      edges {
        node {
          ...action
        }
      }
    }
  }
  ${actionFragment}
`;

export const authorFragment = gql`
  fragment author on Person {
    id
    oid
    title
    description
    function
    isAnonymous
    picture {
      url
    }
  }
`;

export const ideaDataFragment = gql`
  fragment ideaData on Idea {
    id
    oid
    createdAt
    title
  }
`;

export const ideaFragment = gql`
  fragment idea on Idea {
    id
    oid
    createdAt
    title
    keywords
    text
    presentationText
    attachedFiles {
      url
      isImage
      variations
    }
    tokensSupport
    tokensOpposition
    userToken
    state
    opinion
    channel {
      id
      oid
      title
      isDiscuss
    }
    urls {
      url
      title
      description
      imageUrl
      siteName
      favicon
      domain
      authorAvatar
      authorName
    }
    author {
      ...author
    }
    actions(processIds: $processIds, nodeIds: $nodeIds, processTags: $processTags, actionTags: $actionTags) {
      ...action
    }
  }
  ${actionFragment}
  ${authorFragment}
`;

export const personInfoFragment = gql`
  fragment person on Person {
    id
    oid
    title
    createdAt
    description
    function
    isAnonymous
    channel {
      id
      oid
      title
      isDiscuss
    }
    picture {
      url
    }
    actions {
      ...action
    }
  }
  ${actionFragment}
`;

export const personInfoQuery = gql`
  query PersonInfo($id: ID!) {
    person: node(id: $id) {
      ...person
    }
  }
  ${personInfoFragment}
`;

export const personFragment = gql`
  fragment person on Person {
    id
    oid
    title
    createdAt
    description
    function
    isAnonymous
    channel {
      id
      oid
      title
    }
    picture {
      url
    }
    actions {
      ...action
    }
    contents(first: $first, after: $after) {
      pageInfo {
        endCursor
        hasNextPage
      }
      edges {
        node {
          ...idea
        }
      }
    }
  }
  ${actionFragment}
  ${ideaFragment}
`;

export const personQuery = gql`
  query Person($id: ID!,$first: Int!, $after: String!) {
    person: node(id: $id) {
      ...person
    }
  }
  ${personFragment}
`;

export const ideaQuery = gql`
  query($id: ID!, $processIds: [String], $nodeIds: [String], $processTags: [String], $actionTags: [String]) {
    idea: node(id: $id) {
      ...idea
    }
  }
  ${ideaFragment}
`;

export const ideasListQuery = gql`
  query IdeasList($first: Int!, $after: String!, $filter: String!,
                  $processIds: [String], $nodeIds: [String], $processTags: [String], $actionTags: [String]) {
    ideas(first: $first, after: $after, filter: $filter) {
      pageInfo {
        endCursor
        hasNextPage
      }
      edges {
        node {
          ...idea
        }
      }
    }
  }
  ${ideaFragment}
`;

export const mySupportsQuery = gql`
  query MySupports($first: Int!, $after: String!) {
    account {
      id
      supportedIdeas(first: $first, after: $after) {
        totalCount
        pageInfo {
          endCursor
          hasNextPage
        }
        edges {
          node {
            ...ideaData
          }
        }
      }
    }
  }
  ${ideaDataFragment}
`;

export const myFollowingsQuery = gql`
  query MyFollowings($first: Int!, $after: String!) {
    account {
      id
      followedIdeas(first: $first, after: $after) {
        totalCount
        pageInfo {
          endCursor
          hasNextPage
        }
        edges {
          node {
            ...ideaData
          }
        }
      }
    }
  }
  ${ideaDataFragment}
`;

export const myContentsQuery = gql`
  query MyContents($first: Int!, $after: String!) {
    account {
      id
      contents(first: $first, after: $after) {
        totalCount
        pageInfo {
          endCursor
          hasNextPage
        }
        edges {
          node {
            ...ideaData
          }
        }
      }
    }
  }
  ${ideaDataFragment}
`;

export const commentFragment = gql`
  fragment comment on Comment {
    id
    oid
    rootOid
    createdAt
    text
    edited
    channel {
      id
      oid
      title
      isDiscuss
      unreadComments {
        id
        oid
      }
      subject {
        ... on IEntity {
          id
          oid
        }
      }
    }
    author {
      ...author
    }
    attachedFiles {
      url
      isImage
      variations
    }
    urls {
      url
      title
      description
      imageUrl
      siteName
      favicon
      domain
      authorAvatar
      authorName
    }
    lenComments
    actions(processIds: $processIds, nodeIds: $nodeIds, processTags: $processTags, actionTags: $actionTags){
      ...action
    }
  }
  ${actionFragment}
  ${authorFragment}
`;

export const commentQuery = gql`
  query Comment($first: Int!, $after: String!, $filter: String!, $id: ID!, $processIds: [String], $nodeIds: [String]) {
    node(id: $id) {
      ...comment
      ... on Comment {
        comments(first: $first, after: $after, filter: $filter) {
          pageInfo {
            endCursor
            hasNextPage
          }
          edges {
            node {
              ...comment
            }
          }
        }
        actions(processIds: $processIds, nodeIds: $nodeIds) {
          ...action
        }
      }
    }
  }
  ${commentFragment}
  ${actionFragment}
`;

export const commentsQuery = gql`
  query Comments($first: Int!, $after: String!, $filter: String!, $id: ID!,
                 $subjectActionsNodeIds: [String], $processIds: [String], $nodeIds: [String],
                 $processTags: [String], $actionTags: [String]) {
    node(id: $id) {
      ... on Channel{
           id
           oid
           title
           lenComments
           isDiscuss
           unreadComments {
             id
             oid
           }
           subject {
             ... on IEntity {
               id
               oid
               actions(nodeIds: $subjectActionsNodeIds) {
                 ...action
               }
             }
           }

          comments(first: $first, after: $after, filter: $filter) {
            pageInfo {
              endCursor
              hasNextPage
            }
            edges {
              node {
                ...comment
              }
            }
          }
        }
      }
    }
  ${commentFragment}
  ${actionFragment}
`;

export const channelQuery = gql`
  query Channel($id: ID!) {
    node(id: $id) {
      ... on Channel {
        id
        oid
        title
        lenComments
        isDiscuss
        subject {
          ... on IEntity {
            id
            oid
          }
        }
      }
    }
  }
`;

export const channelsQuery = gql`
  query Channels($first: Int!, $after: String!) {
    account {
      id
      channels(first: $first, after: $after) {
        pageInfo {
          endCursor
          hasNextPage
        }
        edges {
          node {
            id
            oid
            title
            unreadComments {
              id
              oid
            }
            subject {
              ... on IEntity {
                id
                oid
              }
            }
          }
        }
      }
    }
  }
`;

export const discussionsQuery = gql`
  query Discussions($first: Int!, $after: String!) {
    account {
      id
      discussions(first: $first, after: $after) {
        pageInfo {
          endCursor
          hasNextPage
        }
        edges {
          node {
            id
            oid
            title
            unreadComments {
              id
              oid
            }
            subject {
              ... on Person {
                id
                oid
                picture {
                  url
                }
              }
            }
          }
        }
      }
    }
  }
`;