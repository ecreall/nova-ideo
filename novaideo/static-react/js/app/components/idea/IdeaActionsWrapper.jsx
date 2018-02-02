/* eslint-disable react/no-array-index-key, no-undef */
import React from 'react';
import { connect } from 'react-redux';
import { gql, graphql } from 'react-apollo';
import update from 'immutability-helper';
import { Translate, I18n } from 'react-redux-i18n';

import { actionFragment } from '../../graphql/queries';
import { goTo, get } from '../../utils/routeMap';

function evaluationActions() {
  return {
    support: {
      nodeId: 'support',
      description: I18n.t('evaluation.supportTheIdea')
    },
    oppose: {
      nodeId: 'oppose',
      description: I18n.t('evaluation.opposeTheIdea')
    },
    withdrawToken: {
      nodeId: 'withdraw_token',
      description: I18n.t('evaluation.withdrawTokenIdea')
    }
  };
}

export function getExaminationValue(idea) {
  if (idea.state.includes('favorable')) return 'bottom';
  if (idea.state.includes('to_study')) return 'middle';
  if (idea.state.includes('unfavorable')) return 'top';
  return undefined;
}

export function getEvaluationActions(idea) {
  const actions = evaluationActions();
  const withdraw = actions.withdrawToken;
  const support = idea.userToken === 'support' ? withdraw : actions.support;
  const oppose = idea.userToken === 'oppose' ? withdraw : actions.oppose;
  const result = {
    top: support,
    down: oppose
  };
  return result;
}

export class DumbIdeaActionsManager extends React.Component {
  evaluationClick = (action) => {
    const { idea, network, globalProps } = this.props;
    if (!network.isLogged) {
      globalProps.showMessage(<Translate value="LogInToPerformThisAction" />);
    } else if (!action) {
      globalProps.showMessage(<Translate value="AuthorizationFailed" />);
    } else {
      switch (action.nodeId) {
      case 'withdraw_token':
        this.props
          .withdraw({
            context: idea.oid
          })
          .catch(globalProps.showError);
        break;
      case 'support':
        if (globalProps.account.availableTokens || idea.userToken === 'oppose') {
          this.props
            .support({
              context: idea.oid
            })
            .catch(globalProps.showError);
        } else {
          globalProps.showMessage(<Translate value="AuthorizationFailed" />);
        }
        break;
      case 'oppose':
        if (globalProps.account.availableTokens || idea.userToken === 'support') {
          this.props
            .oppose({
              context: idea.oid
            })
            .catch(globalProps.showError);
        } else {
          globalProps.showMessage(<Translate value="AuthorizationFailed" />);
        }
        break;
      default:
        globalProps.showMessage(<Translate value="comingSoon" />);
      }
    }
  };

  performAction = (action) => {
    const { idea, network, select, deselect, globalProps } = this.props;
    if (action.nodeId === 'comment') {
      goTo(get('messages', { channelId: idea.channel.id }, { right: 'idea' }));
    } else if (!network.isLogged) {
      globalProps.showMessage(<Translate value="LogInToPerformThisAction" />);
    } else {
      switch (action.behaviorId) {
      case 'select':
        select({ context: idea.oid }).catch(globalProps.showError);
        break;
      case 'deselect':
        deselect({ context: idea.oid }).catch(globalProps.showError);
        break;
      default:
        globalProps.showMessage(<Translate value="comingSoon" />);
      }
    }
  };

  render() {
    const children = React.Children.map(this.props.children, (child) => {
      return React.cloneElement(child, {
        actionsManager: this
      });
    });
    return children;
  }
}

const support = gql`
  mutation($context: String!) {
    supportIdea(context: $context) {
      status
      user {
        availableTokens
      }
      idea {
        id
        tokensSupport
        tokensOpposition
        userToken
        actions {
          ...action
        }
      }
    }
  }
    ${actionFragment}
`;

const oppose = gql`
  mutation($context: String!) {
    opposeIdea(context: $context) {
      status
      user {
        availableTokens
      }
      idea {
        id
        tokensSupport
        tokensOpposition
        userToken
        actions{
          ...action
        }
      }
    }
  }
    ${actionFragment}
`;

const withdraw = gql`
  mutation($context: String!) {
    withdrawTokenIdea(context: $context) {
      status
      user {
        availableTokens
      }
      idea {
        id
        tokensSupport
        tokensOpposition
        userToken
        actions {
          ...action
        }
      }
    }
  }
    ${actionFragment}
`;

const select = gql`
  mutation($context: String!, $processId: String, $nodeIds: [String!]) {
    select(context: $context) {
      status
      idea {
        id
        oid
        actions(processId: $processId, nodeIds: $nodeIds) {
          ...action
        }
      }
    }
  }
  ${actionFragment}
`;

const deselect = gql`
  mutation($context: String!, $processId: String, $nodeIds: [String!]) {
    deselect(context: $context) {
      status
      idea {
        id
        oid
        actions(processId: $processId, nodeIds: $nodeIds) {
          ...action
        }
      }
    }
  }
  ${actionFragment}
`;

const DumbIdeaItemActions = graphql(support, {
  props: function ({ ownProps, mutate }) {
    return {
      support: function ({ context }) {
        const { tokensSupport, tokensOpposition, userToken } = ownProps.idea;
        return mutate({
          variables: { context: context },
          optimisticResponse: {
            __typename: 'Mutation',
            supportIdea: {
              __typename: 'SupportIdea',
              status: true,
              user: {
                __typename: 'Person',
                availableTokens: ownProps.globalProps.account.availableTokens - 1
              },
              idea: {
                ...ownProps.idea,
                tokensSupport: tokensSupport + 1,
                tokensOpposition: userToken === 'oppose' ? tokensOpposition - 1 : tokensOpposition,
                userToken: 'support'
              }
            }
          },
          updateQueries: {
            Account: (prev, { mutationResult }) => {
              return update(prev, {
                account: {
                  availableTokens: { $set: mutationResult.data.supportIdea.user.availableTokens }
                }
              });
            },
            MySupports: (prev, { mutationResult }) => {
              const newIdea = mutationResult.data.supportIdea.idea;
              const currentIdea = prev.account.supportedIdeas.edges.filter((item) => {
                return item && item.node.id === newIdea.id;
              })[0];
              if (!currentIdea) {
                return update(prev, {
                  account: {
                    supportedIdeas: {
                      edges: {
                        $unshift: [
                          {
                            __typename: 'Idea',
                            node: { ...ownProps.idea, ...newIdea }
                          }
                        ]
                      }
                    }
                  }
                });
              }
              const index = prev.account.supportedIdeas.edges.indexOf(currentIdea);
              return update(prev, {
                account: {
                  supportedIdeas: {
                    edges: {
                      $splice: [
                        [
                          index,
                          1,
                          {
                            __typename: 'Idea',
                            node: { ...ownProps.idea, ...newIdea }
                          }
                        ]
                      ]
                    }
                  }
                }
              });
            }
          }
        });
      }
    };
  }
})(
  graphql(oppose, {
    props: function ({ ownProps, mutate }) {
      return {
        oppose: function ({ context }) {
          const { tokensSupport, tokensOpposition, userToken } = ownProps.idea;
          return mutate({
            variables: { context: context },
            optimisticResponse: {
              __typename: 'Mutation',
              opposeIdea: {
                __typename: 'OpposeIdea',
                status: true,
                user: {
                  __typename: 'Person',
                  availableTokens: ownProps.globalProps.account.availableTokens - 1
                },
                idea: {
                  ...ownProps.idea,
                  tokensOpposition: tokensOpposition + 1,
                  tokensSupport: userToken === 'support' ? tokensSupport - 1 : tokensSupport,
                  userToken: 'oppose'
                }
              }
            },
            updateQueries: {
              Account: (prev, { mutationResult }) => {
                return update(prev, {
                  account: {
                    availableTokens: { $set: mutationResult.data.opposeIdea.user.availableTokens }
                  }
                });
              },
              MySupports: (prev, { mutationResult }) => {
                const newIdea = mutationResult.data.opposeIdea.idea;
                const currentIdea = prev.account.supportedIdeas.edges.filter((item) => {
                  return item && item.node.id === newIdea.id;
                })[0];
                if (!currentIdea) {
                  return update(prev, {
                    account: {
                      supportedIdeas: {
                        edges: {
                          $unshift: [
                            {
                              __typename: 'Idea',
                              node: { ...ownProps.idea, ...newIdea }
                            }
                          ]
                        }
                      }
                    }
                  });
                }
                const index = prev.account.supportedIdeas.edges.indexOf(currentIdea);
                return update(prev, {
                  account: {
                    supportedIdeas: {
                      edges: {
                        $splice: [
                          [
                            index,
                            1,
                            {
                              __typename: 'Idea',
                              node: { ...ownProps.idea, ...newIdea }
                            }
                          ]
                        ]
                      }
                    }
                  }
                });
              }
            }
          });
        }
      };
    }
  })(
    graphql(withdraw, {
      props: function ({ ownProps, mutate }) {
        return {
          withdraw: function ({ context }) {
            const { tokensSupport, tokensOpposition, userToken } = ownProps.idea;
            return mutate({
              variables: { context: context },
              optimisticResponse: {
                __typename: 'Mutation',
                withdrawTokenIdea: {
                  __typename: 'OpposeIdea',
                  status: true,
                  user: {
                    __typename: 'Person',
                    availableTokens: ownProps.globalProps.account.availableTokens + 1
                  },
                  idea: {
                    ...ownProps.idea,
                    tokensSupport: userToken === 'support' ? tokensSupport - 1 : tokensSupport,
                    tokensOpposition: userToken === 'oppose' ? tokensOpposition - 1 : tokensOpposition,
                    userToken: 'withdraw'
                  }
                }
              },
              updateQueries: {
                Account: (prev, { mutationResult }) => {
                  return update(prev, {
                    account: {
                      availableTokens: {
                        $set: mutationResult.data.withdrawTokenIdea.user.availableTokens
                      }
                    }
                  });
                },
                MySupports: (prev, { mutationResult }) => {
                  const newIdea = mutationResult.data.withdrawTokenIdea.idea;
                  const currentIdea = prev.account.supportedIdeas.edges.filter((item) => {
                    return item && item.node.id === newIdea.id;
                  })[0];
                  const index = prev.account.supportedIdeas.edges.indexOf(currentIdea);
                  return update(prev, {
                    account: {
                      supportedIdeas: {
                        edges: {
                          $splice: [[index, 1]]
                        }
                      }
                    }
                  });
                },
                IdeasList: (prev, { mutationResult }) => {
                  const newIdea = mutationResult.data.withdrawTokenIdea.idea;
                  const currentIdea = prev.ideas.edges.filter((item) => {
                    return item && item.node.id === newIdea.id;
                  })[0];
                  if (!currentIdea) return prev;
                  const index = prev.ideas.edges.indexOf(currentIdea);
                  return update(prev, {
                    ideas: {
                      edges: {
                        $splice: [[index, 1, { __typename: 'Idea', node: { ...currentIdea.node, ...newIdea } }]]
                      }
                    }
                  });
                }
              }
            });
          }
        };
      }
    })(
      graphql(select, {
        props: function ({ ownProps, mutate }) {
          return {
            select: function ({ context }) {
              const selectAction = ownProps.idea.actions.filter((item) => {
                return item && item.behaviorId === 'select';
              })[0];
              const indexAction = ownProps.idea.actions.indexOf(selectAction);
              const newAction = update(selectAction, {
                counter: { $set: selectAction.counter + 1 },
                nodeId: { $set: 'deselect' },
                behaviorId: { $set: 'deselect' },
                stylePicto: { $set: 'glyphicon glyphicon-star' }
              });
              const optimisticIdea = update(ownProps.idea, {
                actions: {
                  $set: [newAction]
                }
              });
              return mutate({
                variables: { context: context, processId: 'novaideoabstractprocess', nodeIds: ['deselect'] },
                optimisticResponse: {
                  __typename: 'Mutation',
                  select: {
                    __typename: 'Select',
                    status: true,
                    idea: {
                      ...optimisticIdea
                    }
                  }
                },
                updateQueries: {
                  MyFollowings: (prev, { mutationResult }) => {
                    const newActions = mutationResult.data.select.idea.actions;
                    const newIdea = update(ownProps.idea, {
                      actions: {
                        $splice: [[indexAction, 1, ...newActions]]
                      }
                    });
                    return update(prev, {
                      account: {
                        followedIdeas: {
                          edges: {
                            $unshift: [
                              {
                                __typename: 'Idea',
                                node: { ...newIdea }
                              }
                            ]
                          }
                        }
                      }
                    });
                  },
                  IdeasList: (prev, { mutationResult }) => {
                    const idea = mutationResult.data.select.idea;
                    const newActions = idea.actions;
                    const currentIdea = prev.ideas.edges.filter((item) => {
                      return item && item.node.id === idea.id;
                    })[0];
                    if (!currentIdea) return prev;
                    const newIdea = update(currentIdea, {
                      node: {
                        actions: {
                          $splice: [[indexAction, 1, ...newActions]]
                        }
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
                  }
                }
              });
            }
          };
        }
      })(
        graphql(deselect, {
          props: function ({ ownProps, mutate }) {
            return {
              deselect: function ({ context }) {
                const deselectAction = ownProps.idea.actions.filter((item) => {
                  return item && item.behaviorId === 'deselect';
                })[0];
                const newAction = update(deselectAction, {
                  counter: { $set: deselectAction.counter - 1 },
                  nodeId: { $set: 'select' },
                  behaviorId: { $set: 'select' },
                  stylePicto: { $set: 'glyphicon glyphicon-star-empty' }
                });
                const optimisticIdea = update(ownProps.idea, {
                  actions: {
                    $set: [newAction]
                  }
                });
                return mutate({
                  variables: { context: context, processId: 'novaideoabstractprocess', nodeIds: ['select'] },
                  optimisticResponse: {
                    __typename: 'Mutation',
                    deselect: {
                      __typename: 'Deselect',
                      status: true,
                      idea: {
                        ...optimisticIdea
                      }
                    }
                  },
                  updateQueries: {
                    MyFollowings: (prev, { mutationResult }) => {
                      const newIdea = mutationResult.data.deselect.idea;
                      const currentIdea = prev.account.followedIdeas.edges.filter((item) => {
                        return item && item.node.id === newIdea.id;
                      })[0];
                      const index = prev.account.followedIdeas.edges.indexOf(currentIdea);
                      return update(prev, {
                        account: {
                          followedIdeas: {
                            edges: {
                              $splice: [[index, 1]]
                            }
                          }
                        }
                      });
                    },
                    IdeasList: (prev, { mutationResult }) => {
                      const indexAction = ownProps.idea.actions.indexOf(deselectAction);
                      const idea = mutationResult.data.deselect.idea;
                      const newActions = idea.actions;
                      const currentIdea = prev.ideas.edges.filter((item) => {
                        return item && item.node.id === idea.id;
                      })[0];
                      if (!currentIdea) return prev;
                      const newIdea = update(currentIdea, {
                        node: {
                          actions: {
                            $splice: [[indexAction, 1, ...newActions]]
                          }
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
                    }
                  }
                });
              }
            };
          }
        })(DumbIdeaActionsManager)
      )
    )
  )
);

export const mapStateToProps = (state) => {
  return {
    globalProps: state.globalProps,
    network: state.network
  };
};

export default connect(mapStateToProps, null, null, { withRef: true })(DumbIdeaItemActions);