import update from 'immutability-helper';

export default function deleteIdea({ mutate }) {
  return ({ context }) => {
    return mutate({
      variables: {
        context: context.oid
      },
      optimisticResponse: {
        __typename: 'Mutation',
        deleteIdea: {
          __typename: 'DeleteIdea',
          status: true
        }
      },
      updateQueries: {
        IdeasList: (prev, { mutationResult }) => {
          if (!mutationResult.data.deleteIdea.status) return prev;
          const currentIdea = prev.ideas.edges.filter((item) => {
            return item && item.node.id === context.id;
          })[0];
          const index = prev.ideas.edges.indexOf(currentIdea);
          return update(prev, {
            ideas: {
              edges: {
                $splice: [[index, 1]]
              }
            }
          });
        },
        Channels: (prev, { mutationResult }) => {
          if (!mutationResult.data.deleteIdea.status) return prev;
          const currentIdea = prev.account.channels.edges.filter((item) => {
            return item && item.node.id === context.id;
          })[0];
          const index = prev.account.channels.edges.indexOf(currentIdea);
          return update(prev, {
            account: {
              channels: {
                edges: {
                  $splice: [[index, 1]]
                }
              }
            }
          });
        },
        MyContents: (prev, { mutationResult }) => {
          if (!mutationResult.data.deleteIdea.status) return prev;
          const currentIdea = prev.account.contents.edges.filter((item) => {
            return item && item.node.id === context.id;
          })[0];
          const index = prev.account.contents.edges.indexOf(currentIdea);
          const totalCount = prev.account.contents.totalCount - 1;
          return update(prev, {
            account: {
              contents: {
                totalCount: { $set: totalCount },
                edges: {
                  $splice: [[index, 1]]
                }
              }
            }
          });
        }
      }
    });
  };
}