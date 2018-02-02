/* eslint-disable react/no-array-index-key, no-confusing-arrow */
import React from 'react';
import { Field, reduxForm, initialize } from 'redux-form';
import { Translate, I18n } from 'react-redux-i18n';
import classNames from 'classnames';
import { connect } from 'react-redux';
import { gql, graphql } from 'react-apollo';
import update from 'immutability-helper';
import SendIcon from 'material-ui-icons/Send';
import { withStyles } from 'material-ui/styles';
import InsertDriveFileIcon from 'material-ui-icons/InsertDriveFile';
import IconButton from 'material-ui/IconButton';

import { commentFragment } from '../../graphql/queries';
import { renderTextBoxField, renderAnonymousCheckboxField, renderFilesListField } from './utils';
import FilesPickerPreview from './widgets/FilesPickerPreview';
import CommentMenu from './CommentMenu';
import { renderMenuItem } from '../common/menu/MenuList';

const styles = (theme) => {
  return {
    contentContainerStyle: {
      backgroundColor: 'white',
      borderRadius: 6
    },
    contentContainerStyleAddon: {
      boxShadow: '0 -1px 0 rgba(0,0,0,.1)'
    },
    container: {
      paddingLeft: 20,
      paddingRight: 20
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
      outline: 0,
      border: '2px solid #bfbfbf',
      borderRadius: 6,
      resize: 'none',
      color: '#2c2d30',
      fontSize: 15,
      lineHeight: '1.2rem',
      maxHeight: 'none',
      minHeight: '41px',
      alignItems: 'center',
      position: 'relative',
      '&:focus-within': {
        border: '2px solid #848484'
      }
    },
    inputContainerAnonymous: {
      borderColor: theme.palette.warning[700],
      '&:focus-within': {
        borderColor: theme.palette.warning[700]
      }
    },
    textField: {
      paddingLeft: 10,
      marginLeft: 48,
      minHeight: 45,
      display: 'flex',
      alignItems: 'center',
      width: '100%',
      position: 'relative',
      borderLeft: '2px solid #bfbfbf',
      '&:focus-within': {
        borderLeft: '2px solid #848484'
      }
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
      top: 13,
      left: 10
    },
    submit: {
      color: 'gray',
      opacity: 0.7
    },
    submitActive: {
      opacity: 1,
      color: theme.palette.primary[500],
      cursor: 'pointer'
    },
    action: {
      height: 41,
      width: 35,
      display: 'flex',
      padding: 5
    },
    maskIcon: {
      width: 'auto !important',
      height: 'auto !important'
    },
    maskDefault: {
      height: 41,
      width: 35,
      color: 'gray'
    },
    maskChecked: {
      color: theme.palette.warning[700]
    }
  };
};

export class DumbCommentForm extends React.Component {
  constructor(props, context) {
    super(props, context);
    this.filesPicker = null;
  }

  handleSubmit = () => {
    const { globalProps, formData, valid, context, action } = this.props;
    if (valid) {
      let files = formData.values.files || [];
      files = files.filter((file) => {
        return file;
      });
      this.props.commentObject({
        context: context,
        comment: formData.values.comment,
        attachedFiles: files,
        anonymous: Boolean(formData.values.anonymous),
        account: globalProps.account,
        action: `${action.processId}.${action.nodeId}`
      });
      this.initializeForm();
    }
  };

  initializeForm = () => {
    const { formData, form } = this.props;
    const anonymous = formData && formData.values && Boolean(formData.values.anonymous);
    this.props.dispatch(
      initialize(form, {
        comment: '',
        anonymous: anonymous,
        files: []
      })
    );
  };

  render() {
    const { formData, channel, globalProps: { site }, autoFocus, classes, theme } = this.props;
    const hasComment = formData && formData.values && formData.values.comment;
    let files = formData && formData.values && formData.values.files ? formData.values.files : [];
    files = files.filter((file) => {
      return file;
    });
    const isDiscuss = channel && channel.isDiscuss;
    const withAnonymous = site.anonymisation && !isDiscuss;
    const anonymousSelected = withAnonymous && formData && formData.values && Boolean(formData.values.anonymous);
    return (
      <div className={classNames(classes.contentContainerStyle, { [classes.contentContainerStyleAddon]: files.length > 0 })}>
        <div className={classes.container}>
          <FilesPickerPreview
            files={files}
            getPicker={() => {
              return this.filesPicker;
            }}
          />
          <div
            className={classNames(classes.inputContainer, {
              [classes.inputContainerAnonymous]: anonymousSelected
            })}
          >
            <CommentMenu
              fields={[
                () => {
                  return (
                    <Field
                      props={{
                        node: renderMenuItem({
                          Icon: InsertDriveFileIcon,
                          title: I18n.t('forms.attachFiles'),
                          hoverColor: theme.palette.info[500]
                        }),
                        initRef: (filesPicker) => {
                          this.filesPicker = filesPicker;
                        }
                      }}
                      withRef
                      name="files"
                      component={renderFilesListField}
                    />
                  );
                }
              ]}
            />
            <div className={classes.textField}>
              <Field
                props={{
                  onCtrlEnter: this.handleSubmit,
                  autoFocus: autoFocus
                }}
                name="comment"
                component={renderTextBoxField}
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
                <Translate value="forms.comment.textPlaceholder" name={channel ? channel.title : '...'} />
              </div>
            </div>
            <div className={withAnonymous && classes.addon}>
              {withAnonymous
                ? <Field
                  props={{
                    classes: classes
                  }}
                  name="anonymous"
                  component={renderAnonymousCheckboxField}
                  type="boolean"
                />
                : null}
            </div>

            <IconButton onClick={hasComment ? this.handleSubmit : undefined} className={classes.action}>
              <SendIcon
                size={22}
                className={classNames(classes.submit, {
                  [classes.submitActive]: hasComment
                })}
              />
            </IconButton>
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
                edited: false,
                author: {
                  __typename: 'Person',
                  id: `${authorId}comment`,
                  oid: `${authorOid}comment`,
                  isAnonymous: anonymous,
                  description: account.description,
                  function: account.function,
                  title: authorTitle,
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