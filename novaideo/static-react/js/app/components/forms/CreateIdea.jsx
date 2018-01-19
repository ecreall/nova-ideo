/* eslint-disable react/no-array-index-key, no-confusing-arrow */
import React from 'react';
import { Field, reduxForm } from 'redux-form';
import { connect } from 'react-redux';
import { gql, graphql } from 'react-apollo';
import { ReactNativeFile } from 'apollo-upload-client';
import update from 'immutability-helper';
import classNames from 'classnames';
import SendIcon from 'material-ui-icons/Send';
import { withStyles } from 'material-ui/styles';
import InsertDriveFileIcon from 'material-ui-icons/InsertDriveFile';
import IconButton from 'material-ui/IconButton';
import Avatar from 'material-ui/Avatar';
import Icon from 'material-ui/Icon';

import FilesPickerPreview from './widgets/FilesPickerPreview';
import SelectChipPreview from './widgets/SelectChipPreview';
import { renderTextBoxField, renderAnonymousCheckboxField, renderFilesListField, renderSelect } from './utils';
import { ideaFragment } from '../../graphql/queries';

const styles = (theme) => {
  return {
    contentContainerStyle: {
      padding: 20,
      paddingLeft: 11,
      backgroundColor: 'whitesmoke',
      border: 'solid 1px rgba(0,0,0,.1)',
      borderBottom: 'none'
    },
    contentContainerStyleAddon: {
      boxShadow: '0 -1px 0 rgba(0,0,0,.1)'
    },
    container: {
      display: 'flex'
    },
    addon: {
      display: 'flex',
      flexDirection: 'row'
    },
    addonContainer: {
      display: 'flex',
      flexDirection: 'row',
      justifyContent: 'space-between'
    },
    inputContainer: {
      display: 'flex',
      justifyContent: 'space-between',
      height: 'auto',
      outline: 0,
      border: '1px solid #bfbfbf',
      borderRadius: 4,
      resize: 'none',
      color: '#2c2d30',
      fontSize: '.9375rem',
      lineHeight: '1.2rem',
      maxHeight: 'none',
      minHeight: 40,
      position: 'relative',
      backgroundColor: 'white',
      flex: 1,
      flexDirection: 'column',
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
      flex: 1,
      paddingLeft: 10,
      paddingRight: 10,
      minHeight: 40,
      display: 'flex',
      alignItems: 'center',
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
      top: 11,
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
      display: 'flex',
      padding: 5
    },
    maskIcon: {
      width: 'auto !important',
      height: 'auto !important'
    },
    maskDefault: {
      height: 40,
      width: 40,
      color: '#a3a3a3'
    },
    maskChecked: {
      color: theme.palette.warning[700]
    },
    button: {
      height: 40,
      width: 40,
      color: '#a3a3a3'
    },
    avatar: {
      borderRadius: 4,
      marginTop: 1
    },
    form: {
      flex: 1,
      marginLeft: 10
    },
    previews: {
      borderTop: 'solid 1px #bfbfbf',
      backgroundColor: '#fafafa',
      padding: 5,
      borderBottomLeftRadius: 4,
      borderBottomRightRadius: 4
    }
  };
};

export class DumbCreateIdeaForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      opened: false,
      displayErrors: false,
      sending: false
    };
    this.container = null;
  }

  componentDidMount() {
    document.addEventListener('click', this.closeForm);
  }

  componentWillUnmount() {
    document.removeEventListener('click', this.closeForm);
  }

  closeForm = (event) => {
    const { formData } = this.props;
    if (this.state.opened && this.container && !this.container.contains(event.target) && !formData.values) {
      this.setState({ opened: false });
    }
  };

  openForm = () => {
    if (!this.state.opened) {
      this.setState({ opened: true });
    }
  };

  handleSubmit = (action) => {
    const { formData, valid, globalProps } = this.props;
    if (valid) {
      // submit form here
      const close = () => {
        this.props.navigation.goBack();
      };
      this.setState({ sending: true });
      // we must encode the file name
      const files = formData.values.files
        ? ReactNativeFile.list(
          formData.values.files.map((file) => {
            return {
              uri: file.url,
              name: encodeURI(file.name),
              type: `${file.type}/*`
            };
          })
        )
        : [];
      if (action.nodeId === 'creatandpublish') {
        this.props.createAndPublish({
          text: formData.values.text,
          title: formData.values.title,
          keywords: formData.values.keywords.map((item) => {
            return item.title;
          }),
          attachedFiles: files,
          anonymous: Boolean(formData.values.anonymous),
          account: globalProps.account
        });
        close();
      }
      if (action.nodeId === 'creat') {
        this.props.createIdea({
          text: formData.values.text,
          title: formData.values.title,
          keywords: formData.values.keywords.map((item) => {
            return item.title;
          }),
          attachedFiles: files,
          anonymous: Boolean(formData.values.anonymous),
          account: globalProps.account
        });
        close();
      }
    } else {
      this.setState({ displayErrors: true });
    }
  };

  render() {
    const { formData, globalProps: { siteConf, account }, classes } = this.props;
    const hasComment = formData && formData.values && formData.values.text;
    let files = formData && formData.values && formData.values.files ? formData.values.files : [];
    const selectedKeywords = formData && formData.values && formData.values.keywords ? formData.values.keywords : {};
    files = files.filter((file) => {
      return file;
    });
    const withAnonymous = siteConf.anonymisation;
    const anonymousSelected = withAnonymous && formData && formData.values && Boolean(formData.values.anonymous);
    const authorPicture = account.picture;
    const { opened } = this.state;
    const keywords = {};
    siteConf.keywords.forEach((keyword) => {
      keywords[keyword] = keyword;
    });
    siteConf.keywords.forEach((keyword) => {
      keywords[`${keyword}z`] = keyword;
    });
    siteConf.keywords.forEach((keyword) => {
      keywords[`${keyword}zF`] = keyword;
    });
    siteConf.keywords.forEach((keyword) => {
      keywords[`${keyword}z2`] = keyword;
    });
    siteConf.keywords.forEach((keyword) => {
      keywords[`${keyword}z4`] = keyword;
    });
    return (
      <div
        ref={(container) => {
          this.container = container;
        }}
        className={classes.contentContainerStyle}
      >
        <div className={classes.container}>
          <div className={classes.left}>
            <Avatar classes={{ root: classes.avatar }} ize={30} src={authorPicture ? `${authorPicture.url}/profil` : ''} />
          </div>
          <div className={classes.form}>
            <div
              className={classNames(classes.inputContainer, {
                [classes.inputContainerAnonymous]: anonymousSelected
              })}
              onClick={this.openForm}
            >
              <div className={classes.textField}>
                <Field
                  props={{
                    onCtrlEnter: this.handleSubmit,
                    style: {
                      picker: {
                        bottom: 'auto'
                      }
                    }
                  }}
                  name="text"
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
                  Your text here
                </div>
              </div>
              {(files.length > 0 || Object.keys(selectedKeywords).length > 0) &&
                <div className={classes.previews}>
                  <SelectChipPreview
                    items={selectedKeywords}
                    onItemDelete={(id) => {
                      this.keywordsPicker.toggleOption(false, id);
                    }}
                  />
                  <FilesPickerPreview
                    files={files}
                    getPicker={() => {
                      return this.filesPicker;
                    }}
                  />
                </div>}
            </div>

            {opened &&
              <div className={classes.addonContainer}>
                <div className={classes.addon}>
                  <Field
                    props={{
                      label: <Icon className={'mdi-set mdi-tag-multiple'} />,
                      options: keywords,
                      canAdd: siteConf.canAddKeywords,
                      initRef: (keywordsPicker) => {
                        this.keywordsPicker = keywordsPicker;
                      }
                    }}
                    withRef
                    name="keywords"
                    component={renderSelect}
                  />
                  <Field
                    props={{
                      node: (
                        <IconButton className={classes.button}>
                          <InsertDriveFileIcon />
                        </IconButton>
                      ),
                      initRef: (filesPicker) => {
                        this.filesPicker = filesPicker;
                      }
                    }}
                    withRef
                    name="files"
                    component={renderFilesListField}
                  />
                  {withAnonymous
                    ? <Field
                      props={{
                        classes: classes,
                        label: 'RemainAnonymous'
                      }}
                      name="anonymous"
                      component={renderAnonymousCheckboxField}
                      type="boolean"
                    />
                    : null}
                </div>
                <div className={classes.action}>
                  <SendIcon
                    onClick={hasComment ? this.handleSubmit : undefined}
                    size={22}
                    className={classNames(classes.submit, {
                      [classes.submitActive]: hasComment
                    })}
                  />
                </div>
              </div>}
          </div>
        </div>
      </div>
    );
  }
}

// Decorate the form component
const CreateIdeaReduxForm = reduxForm({
  form: 'createIdea' // a unique name for this form
})(DumbCreateIdeaForm);

const mapStateToProps = (state) => {
  return {
    formData: state.form.createIdea,
    instance: state.instance,
    globalProps: state.globalProps
  };
};

const createPublishIdea = gql`
  mutation($text: String!, $title: String!, $keywords: [String]!, $attachedFiles: [Upload], $anonymous: Boolean) {
    createAndPublish(
      title: $title
      keywords: $keywords
      text: $text
      attachedFiles: $attachedFiles,
      anonymous: $anonymous
    ) {
      status
      idea {
        ...idea
      }
    }
  }
  ${ideaFragment}
`;
const createIdea = gql`
  mutation($text: String!, $title: String!, $keywords: [String]!, $attachedFiles: [Upload], $anonymous: Boolean) {
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

const CreateIdeaForm = graphql(createPublishIdea, {
  props: function ({ ownProps, mutate }) {
    return {
      createAndPublish: function ({ text, title, keywords, attachedFiles, anonymous, account }) {
        const { formData, instance } = ownProps;
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
            text: text,
            title: title,
            keywords: keywords,
            attachedFiles: attachedFiles,
            anonymous: anonymous
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
                presentationText: text,
                attachedFiles: files,
                tokensSupport: 0,
                tokensOpposition: 0,
                userToken: null,
                state: instance.support_ideas ? ['submitted_support'] : ['published'],
                channel: {
                  __typename: 'Channel',
                  id: 'channel-id',
                  oid: 'channel-oid'
                },
                opinion: '',
                urls: [],
                author: {
                  __typename: 'Person',
                  isAnonymous: anonymous,
                  id: `${account.id}createidea`,
                  oid: `${account.oid}createidea`,
                  title: !anonymous ? account.title : 'Anonymous',
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
              const newIdea = mutationResult.data.createAndPublish.idea;
              // if the idea is submitted to moderation
              if (newIdea.state.includes('submitted')) return prev;
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
              return update(prev, {
                account: {
                  contents: {
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
      }
    };
  }
})(
  graphql(createIdea, {
    props: function ({ ownProps, mutate }) {
      return {
        createIdea: function ({ text, title, keywords, attachedFiles, anonymous, account }) {
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
              text: text,
              title: title,
              keywords: keywords,
              attachedFiles: attachedFiles,
              anonymous: anonymous
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
                    oid: 'channel-oid'
                  },
                  opinion: '',
                  urls: [],
                  author: {
                    __typename: 'Person',
                    isAnonymous: anonymous,
                    id: `${account.id}createidea`,
                    oid: `${account.oid}createidea`,
                    title: !anonymous ? account.title : 'Anonymous',
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
                return update(prev, {
                  account: {
                    contents: {
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
        }
      };
    }
  })(CreateIdeaReduxForm)
);

export default withStyles(styles, { withTheme: true })(connect(mapStateToProps)(CreateIdeaForm));