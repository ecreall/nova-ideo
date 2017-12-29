/* eslint-disable react/no-array-index-key, no-undef */
import React from 'react';
import { connect } from 'react-redux';
import { gql, graphql } from 'react-apollo';
import update from 'immutability-helper';
import Grid from 'material-ui/Grid';
import { Translate } from 'react-redux-i18n';
import Avatar from 'material-ui/Avatar';
import { CardActions } from 'material-ui/Card';
import IconButton from 'material-ui/IconButton';
import Icon from 'material-ui/Icon';
import { withStyles } from 'material-ui/styles';
import classNames from 'classnames';

import ImagesPreview from '../common/ImagesPreview';
import Keywords from '../common/Keywords';
import IconWithText from '../common/IconWithText';
import Evaluation from '../common/Evaluation';
import * as constants from '../../constants';
import { actionFragment } from '../../graphql/queries';
import { getActions } from '../../utils/entities';
import { updateApp } from '../../actions/actions';

const styles = (theme) => {
  return {
    ideaItem: {
      marginBottom: 10,
      marginTop: 5
    },
    header: {
      display: 'flex',
      flexDirection: 'row',
      alignItems: 'center',
      padding: 5,
      paddingLeft: 10
    },
    headerTitle: {
      display: 'flex',
      fontSize: 13,
      color: '#999999ff',
      justifyContent: 'space-around',
      paddingLeft: 10
    },
    headerAddOn: {
      fontSize: 10,
      color: '#999999ff',
      paddingLeft: 5
    },
    body: {
      display: 'flex',
      flexDirection: 'row',
      marginTop: -5
    },
    bodyTitle: {},
    bodyLeft: {
      width: 60,
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      paddingTop: 10,
      paddingBottom: 10
    },
    bodyContent: {
      display: 'flex',
      justifyContent: 'space-between',
      flexDirection: 'column',
      width: '100%'
    },
    textContainer: {
      display: 'flex',
      justifyContent: 'space-between'
    },
    imagesContainer: {
      width: '30%'
    },
    bodyFooter: {
      display: 'flex',
      flexDirection: 'row',
      marginTop: 15
    },
    actionsText: {
      fontSize: 13,
      color: '#585858',
      fontWeight: 'bold',
      marginLeft: 8,
      marginRight: 50,
      '&:hover': {
        color: theme.palette.primary['500']
      }
    },
    actionsIcon: {
      fontWeight: 100,
      fontSize: 16,
      marginRight: 5
    },
    sliderHeader: {
      marginLeft: 4,
      fontSize: 17,
      color: 'white',
      width: '90%'
    }
  };
};

const evaluationActions = {
  support: {
    nodeId: 'support',
    description: <Translate value="supportTheIdea" />
  },
  oppose: {
    nodeId: 'oppose',
    description: <Translate value="opposeTheIdea" />
  },
  withdrawToken: {
    nodeId: 'withdraw_token',
    description: <Translate value="withdrawTokenIdea" />
  }
};

export class DumbIdeaItem extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      opened: false,
      actionOpened: false
    };
  }

  getExaminationValue = () => {
    const { node } = this.props;
    if (node.state.includes('favorable')) return 'bottom';
    if (node.state.includes('to_study')) return 'middle';
    if (node.state.includes('unfavorable')) return 'top';
    return undefined;
  };

  getEvaluationActions = () => {
    const { node } = this.props;
    const withdraw = evaluationActions.withdrawToken;
    const support = node.userToken === 'support' ? withdraw : evaluationActions.support;
    const oppose = node.userToken === 'oppose' ? withdraw : evaluationActions.oppose;
    const result = {
      top: support,
      down: oppose
    };
    return result;
  };

  evaluationPress = (action) => {
    const { node, network, globalProps } = this.props;
    if (!network.isLogged) {
      globalProps.showMessage(<Translate value="LogInToPerformThisAction" />);
    } else if (!action) {
      globalProps.showMessage(<Translate value="AuthorizationFailed" />);
    } else {
      switch (action.nodeId) {
      case 'withdraw_token':
        this.props
          .withdraw({
            context: node.oid
          })
          .catch(globalProps.showError);
        break;
      case 'support':
        if (globalProps.account.availableTokens || node.userToken === 'oppose') {
          this.props
            .support({
              context: node.oid
            })
            .catch(globalProps.showError);
        } else {
          globalProps.showMessage(<Translate value="AuthorizationFailed" />);
        }
        break;
      case 'oppose':
        if (globalProps.account.availableTokens || node.userToken === 'support') {
          this.props
            .oppose({
              context: node.oid
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

  performAction = (action, idea) => {
    const { network, select, deselect, openChannel } = this.props;
    if (action.nodeId === 'comment') {
      if (!this.state.actionOpened) {
        this.setState({ actionOpened: true }, () => {
          return openChannel('chatApp', { drawer: true, open: true, channel: idea.channel.id });
        });
      }
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

  onActionPress = (action) => {
    this.performAction(action, this.props.node, this);
  };

  render() {
    const { node, adapters, globalProps, classes } = this.props;
    const instance = { support_ideas: true, examine_ideas: false };
    const author = node.author;
    const authorPicture = author.picture;
    const createdAt = node.createdAt;
    const images = node.attachedFiles
      ? node.attachedFiles.filter((image) => {
        return image.isImage;
      })
      : [];
    const Examination = adapters.examination;
    const communicationActions = getActions(node.actions, constants.ACTIONS.communicationAction);
    return (
      <div className={classes.ideaItem}>
        <div className={classes.header}>
          <Avatar size={40} src={authorPicture ? `${authorPicture.url}/profil` : ''} />
          <span className={classes.headerTitle}>
            {author.title}
          </span>
          <span className={classes.headerAddOn}>
            {createdAt}
          </span>
        </div>
        <div className={classes.body}>
          <div className={classes.bodyLeft}>
            {instance.support_ideas && node.state.includes('published')
              ? <Evaluation
                icon={{
                  top:
                      node.userToken === 'support'
                        ? 'mdi-set mdi-arrow-up-drop-circle-outline'
                        : 'mdi-set mdi-arrow-up-drop-circle',
                  down:
                      node.userToken === 'oppose'
                        ? 'mdi-set mdi-arrow-down-drop-circle-outline'
                        : 'mdi-set mdi-arrow-down-drop-circle'
                }}
                onPress={{ top: this.evaluationPress, down: this.evaluationPress }}
                onLongPress={{ top: this.onActionLongPress, down: this.onActionLongPress }}
                text={{ top: node.tokensSupport, down: node.tokensOpposition }}
                action={this.getEvaluationActions()}
                active={node.state.includes('submitted_support')}
              />
              : null}
            {instance.examine_ideas && node.state.includes('examined')
              ? <Examination message={node.opinion} value={this.getExaminationValue()} />
              : null}
          </div>
          <div className={classes.bodyContent}>
            <div>
              <div className={classes.bodyTitle}>
                <IconWithText name="mdi-set mdi-lightbulb" text={node.title} iconSize={17} />
              </div>
              <Keywords onKeywordPress={this.props.searchEntities} keywords={node.keywords} />

              <Grid container item>
                <Grid item xs={12} sm={images.length > 0 ? 7 : 12}>
                  {node.presentationText}
                </Grid>
                {images.length > 0 &&
                  <Grid item xs={12} sm={5}>
                    <ImagesPreview navigation={globalProps.navigation} images={images} />
                  </Grid>}
              </Grid>
            </div>
            <div className={classes.bodyFooter}>
              <CardActions disableActionSpacing>
                {communicationActions.map((action, key) => {
                  return (
                    <IconButton
                      className={classes.actionsText}
                      key={key}
                      onClick={() => {
                        return this.onActionPress(action);
                      }}
                      aria-label="Add to favorites"
                    >
                      <Icon className={classNames(action.stylePicto, classes.actionsIcon)} />
                      {action.counter}
                    </IconButton>
                  );
                })}
              </CardActions>
            </div>
          </div>
        </div>
      </div>
    );
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
        const { tokensSupport, tokensOpposition, userToken } = ownProps.node;
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
                ...ownProps.node,
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
                            node: { ...ownProps.node, ...newIdea }
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
                            node: { ...ownProps.node, ...newIdea }
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
          const { tokensSupport, tokensOpposition, userToken } = ownProps.node;
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
                  ...ownProps.node,
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
                              node: { ...ownProps.node, ...newIdea }
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
                              node: { ...ownProps.node, ...newIdea }
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
            const { tokensSupport, tokensOpposition, userToken } = ownProps.node;
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
                    ...ownProps.node,
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
              const selectAction = ownProps.node.actions.filter((item) => {
                return item && item.behaviorId === 'select';
              })[0];
              const indexAction = ownProps.node.actions.indexOf(selectAction);
              const newAction = update(selectAction, {
                counter: { $set: selectAction.counter + 1 },
                nodeId: { $set: 'deselect' },
                behaviorId: { $set: 'deselect' },
                stylePicto: { $set: 'glyphicon glyphicon-star' }
              });
              const optimisticIdea = update(ownProps.node, {
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
                    const newIdea = update(ownProps.node, {
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
                const deselectAction = ownProps.node.actions.filter((item) => {
                  return item && item.behaviorId === 'deselect';
                })[0];
                const newAction = update(deselectAction, {
                  counter: { $set: deselectAction.counter - 1 },
                  nodeId: { $set: 'select' },
                  behaviorId: { $set: 'select' },
                  stylePicto: { $set: 'glyphicon glyphicon-star-empty' }
                });
                const optimisticIdea = update(ownProps.node, {
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
                      const indexAction = ownProps.node.actions.indexOf(deselectAction);
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
        })(DumbIdeaItem)
      )
    )
  )
);

export const mapDispatchToProps = { openChannel: updateApp };

export const mapStateToProps = (state) => {
  return {
    globalProps: state.globalProps,
    network: state.network,
    adapters: state.adapters
  };
};

export default withStyles(styles, { withTheme: true })(connect(mapStateToProps, mapDispatchToProps)(DumbIdeaItemActions));