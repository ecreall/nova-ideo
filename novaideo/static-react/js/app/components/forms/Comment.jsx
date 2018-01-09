/* eslint-disable react/no-array-index-key, no-confusing-arrow */
import React from 'react';
import { Field, reduxForm, initialize } from 'redux-form';
import classNames from 'classnames';
import { connect } from 'react-redux';
import { gql, graphql } from 'react-apollo';
import update from 'immutability-helper';
import SendIcon from 'material-ui-icons/Send';
import { withStyles } from 'material-ui/styles';

import { commentFragment } from '../../graphql/queries';
import { renderInput, renderCheckbox } from './utils';

const styles = {
  contentContainerStyle: {
    backgroundColor: 'white'
  },
  container: {
    paddingLeft: 15,
    paddingRight: 15
  },
  addon: {
    display: 'flex',
    flexDirection: 'row',
    justifyContent: 'space-between'
  },
  inputContainer: {
    display: 'flex',
    flexDirection: 'row',
    justifyContent: 'space-between',
    height: 'auto',
    borderColor: '#717274',
    outline: 0,
    border: '2px solid #717274',
    borderRadius: '.375rem',
    resize: 'none',
    color: '#2c2d30',
    fontSize: '.9375rem',
    lineHeight: '1.2rem',
    maxHeight: 'none',
    minHeight: '41px',
    alignItems: 'center'
  },
  textField: {
    paddingLeft: 10,
    display: 'flex',
    alignItems: 'center',
    width: '100%',
    position: 'relative'
  },
  placeholder: {
    color: '#000',
    opacity: '.375',
    filter: 'grayscale(100%)',
    textOverflow: 'ellipsis',
    overflow: 'hidden',
    whiteSpace: 'nowrap',
    fontStyle: 'normal',
    pointerEvents: 'none',
    position: 'absolute',
    display: 'none',
    top: 0,
    left: 0,
    right: 0,
    maxHeight: '100%'
  },
  placeholderActive: {
    display: 'block',
    left: 10
  },
  submit: {
    color: 'gray',
    opacity: 0.7
  },
  submitActive: {
    opacity: 1,
    color: 'blue'
  },
  action: {
    display: 'flex',
    padding: 5
  }
};

export class DumbCommentForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      displayErrors: false,
      sending: false
    };
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleSubmit() {
    const { formData, valid, form, context, action } = this.props;
    if (valid) {
      // submit form here
      this.setState({ sending: true });
      // we must encode the file name
      const files = [];
      const anonymous = Boolean(formData.values.anonymous);
      const account = { id: 'userid', oid: 'useroid' };
      this.props.commentObject({
        context: context,
        comment: formData.values.comment,
        attachedFiles: files,
        anonymous: anonymous,
        account: account,
        action: `${action.processId}.${action.nodeId}`
      });
      this.props.dispatch(initialize(form, { anonymous: anonymous, files: [] }));
    } else {
      this.setState({ displayErrors: true });
    }
  }

  render() {
    const { formData, classes } = this.props;
    const errors = formData ? formData.syncErrors : {};
    const hasComment = formData && formData.values && formData.values.comment;
    // const withAnonymous = siteConf.anonymisation && !channel.isDiscuss;
    const withAnonymous = true;
    return (
      <div style={styles.contentContainerStyle}>
        <div style={styles.container}>
          <div style={withAnonymous ? styles.addon : {}}>
            {withAnonymous
              ? <Field
                props={{
                  label: 'RemainAnonymous',
                  displayErrors: this.state.displayErrors,
                  errors: errors
                }}
                name="anonymous"
                component={renderCheckbox}
                type="boolean"
              />
              : null}
          </div>
          <div style={styles.inputContainer}>
            <div style={styles.textField}>
              <Field
                props={{
                  placeholder: 'yourMessageHere',
                  placeholderTextColor: 'gray'
                }}
                name="comment"
                component={renderInput}
                type="text"
              />
              <div
                className={classNames(classes.placeholder, {
                  [classes.placeholderActive]: !hasComment
                })}
                aria-hidden="true"
                role="presentation"
                tabIndex="-1"
              >
                Your text here
              </div>
            </div>
            <div style={styles.action}>
              <div onClick={hasComment ? this.handleSubmit : undefined}>
                <SendIcon
                  size={22}
                  className={classNames(classes.submit, {
                    [classes.submitActive]: hasComment
                  })}
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

// Decorate the form component
const CommentReduxForm = reduxForm({ destroyOnUnmount: false })(DumbCommentForm);

const mapStateToProps = (state, props) => {
  return {
    formState: state.form,
    formData: state.form[props.form],
    globalProps: state.globalProps
  };
};

const commentObject = gql`
  mutation($context: String!, $comment: String!, $action: String!, $attachedFiles: [Upload], $anonymous: Boolean) {
    commentObject(
      context: $context
      comment: $comment
      action: $action
      attachedFiles: $attachedFiles,
      anonymous: $anonymous
    ) {
      status
      comment {
        ...comment
      }
    }
  }
  ${commentFragment}
`;

const CommentForm = graphql(commentObject, {
  props: function ({ ownProps, mutate }) {
    return {
      commentObject: function ({ context, comment, action, attachedFiles, anonymous, account }) {
        const { formData } = ownProps;
        const files =
          attachedFiles.length > 0
            ? formData.values.files.map((file) => {
              return {
                url: file.url,
                isImage: file.type === 'image',
                __typename: 'File'
              };
            })
            : [];
        const createdAt = new Date();
        return mutate({
          variables: {
            context: context,
            comment: comment,
            attachedFiles: attachedFiles,
            anonymous: anonymous,
            action: action
          },
          optimisticResponse: {
            __typename: 'Mutation',
            commentObject: {
              __typename: 'CommentObject',
              status: true,
              comment: {
                __typename: 'Comment',
                id: '0',
                oid: '0',
                channel: { ...ownProps.channel, unreadComments: [] },
                rootOid: ownProps.rootContext,
                createdAt: createdAt.toISOString(),
                text: comment,
                attachedFiles: files,
                urls: [],
                author: {
                  __typename: 'Person',
                  id: `${account.id}comment`,
                  oid: `${account.oid}comment`,
                  isAnonymous: anonymous,
                  description: account.description,
                  function: account.function,
                  title: !anonymous ? account.title : 'Anonymous',
                  picture:
                    !anonymous && account.picture
                      ? {
                        __typename: 'File',
                        url: account.picture.url
                      }
                      : null
                },
                actions: [],
                lenComments: 0
              }
            }
          },
          updateQueries: {
            IdeasList: (prev) => {
              const currentIdea = prev.ideas.edges.filter((item) => {
                return item && item.node.oid === ownProps.rootContext;
              })[0];
              if (!currentIdea) {
                return prev;
              }
              const commentAction = currentIdea.node.actions.filter((item) => {
                return item && item.behaviorId === 'comment';
              })[0];
              const indexAction = currentIdea.node.actions.indexOf(commentAction);
              const newAction = update(commentAction, {
                counter: { $set: commentAction.counter + 1 }
              });
              const newIdea = update(currentIdea, {
                node: {
                  actions: {
                    $splice: [[indexAction, 1, newAction]]
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
            },
            Profil: (prev) => {
              if (prev.person.oid !== ownProps.rootContext) return prev;
              const commentAction = prev.person.actions.filter((item) => {
                return item && item.behaviorId === 'discuss';
              })[0];
              const indexAction = prev.person.actions.indexOf(commentAction);
              const newAction = update(commentAction, {
                counter: { $set: commentAction.counter + 1 }
              });
              return update(prev, {
                person: {
                  actions: {
                    $splice: [[indexAction, 1, newAction]]
                  }
                }
              });
            },
            Channels: (prev) => {
              if (ownProps.channel.isDiscuss) return prev;
              const currentChannel = prev.account.channels.edges.filter((item) => {
                return item && item.node.id === ownProps.channel.id;
              })[0];
              if (currentChannel) {
                return prev;
              }
              const newChannel = { ...ownProps.channel, unreadComments: [] };
              return update(prev, {
                account: {
                  channels: {
                    edges: {
                      $unshift: [
                        {
                          __typename: 'Channel',
                          node: newChannel
                        }
                      ]
                    }
                  }
                }
              });
            },
            Discussions: (prev) => {
              if (!ownProps.channel.isDiscuss) return prev;
              const currentChannel = prev.account.discussions.edges.filter((item) => {
                return item && item.node.id === ownProps.channel.id;
              })[0];
              if (currentChannel) {
                return prev;
              }
              const newChannel = { ...ownProps.channel, unreadComments: [] };
              return update(prev, {
                account: {
                  discussions: {
                    edges: {
                      $unshift: [
                        {
                          __typename: 'Channel',
                          node: newChannel
                        }
                      ]
                    }
                  }
                }
              });
            },
            Comments: (prev, { mutationResult }) => {
              if (ownProps.context !== prev.node.subject.oid) {
                return prev;
              }

              const newComment = mutationResult.data.commentObject.comment;
              return update(prev, {
                node: {
                  lenComments: { $set: prev.node.lenComments + 1 },
                  comments: {
                    edges: {
                      $unshift: [
                        {
                          __typename: 'Comment',
                          node: newComment
                        }
                      ]
                    }
                  }
                }
              });
            },
            Comment: (prev, { mutationResult }) => {
              if (ownProps.context !== prev.node.oid) {
                return prev;
              }
              const newComment = mutationResult.data.commentObject.comment;
              return update(prev, {
                node: {
                  lenComments: { $set: prev.node.lenComments + 1 },
                  comments: {
                    edges: {
                      $unshift: [
                        {
                          __typename: 'Comment',
                          node: newComment
                        }
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
})(CommentReduxForm);

export default withStyles(styles, { withTheme: true })(connect(mapStateToProps)(CommentForm));