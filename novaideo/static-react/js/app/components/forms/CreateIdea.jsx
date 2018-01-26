/* eslint-disable react/no-array-index-key, no-confusing-arrow */
import React from 'react';
import { Field, reduxForm, initialize } from 'redux-form';
import { connect } from 'react-redux';
import { gql, graphql } from 'react-apollo';
import { I18n } from 'react-redux-i18n';
import update from 'immutability-helper';
import classNames from 'classnames';
import SendIcon from 'material-ui-icons/Send';
import { withStyles } from 'material-ui/styles';
import AttachFileIcon from 'material-ui-icons/AttachFile';
import IconButton from 'material-ui/IconButton';
import Avatar from 'material-ui/Avatar';
import Icon from 'material-ui/Icon';
import Tooltip from 'material-ui/Tooltip';

import FilesPickerPreview from './widgets/FilesPickerPreview';
import SelectChipPreview from './widgets/SelectChipPreview';
import { renderTextInput, renderTextBoxField, renderAnonymousCheckboxField, renderFilesListField, renderSelect } from './utils';
import { ideaFragment } from '../../graphql/queries';

const styles = (theme) => {
  return {
    fromContainer: {
      padding: '15px 11px',
      backgroundColor: 'whitesmoke',
      border: 'solid 1px rgba(0,0,0,.1)',
      borderBottom: 'none',
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
      border: '1px solid #a0a0a2',
      borderRadius: 4,
      resize: 'none',
      color: '#2c2d30',
      fontSize: 15,
      lineHeight: '1.2rem',
      maxHeight: 'none',
      minHeight: 40,
      position: 'relative',
      backgroundColor: 'white',
      flex: 1,
      flexDirection: 'column'
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
      justifyContent: 'flex-end',
      padding: 5
    },
    maskIcon: {
      width: 'auto !important',
      height: 'auto !important'
    },
    maskDefault: {
      height: 40,
      width: 40,
      color: '#808080'
    },
    maskChecked: {
      color: theme.palette.warning[700]
    },
    button: {
      height: 40,
      width: 40,
      color: '#808080'
    },
    avatar: {
      borderRadius: 4,
      marginTop: 1
    },
    anonymousAvatar: {
      color: theme.palette.tertiary.hover.color,
      backgroundColor: theme.palette.tertiary.color,
      fontWeight: 900
    },
    form: {
      flex: 1,
      marginLeft: 10
    },
    label: {
      display: 'flex',
      alignItems: 'center',
      fontWeight: 700,
      margin: '0 0 .25rem',
      fontSize: 13,
      cursor: 'pointer'
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
      opened: false
    };
    this.container = null;
    this.filesPicker = null;
    this.keywordsPicker = null;
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

  handleSubmit = () => {
    const action = { nodeId: 'creatandpublish' };
    const { formData, valid, globalProps } = this.props;
    if (valid) {
      // we must encode the file name
      let files = formData.values.files || [];
      files = files.filter((file) => {
        return file;
      });
      if (action.nodeId === 'creatandpublish') {
        this.props.createAndPublish({
          text: formData.values.text,
          title: formData.values.title,
          keywords: Object.values(formData.values.keywords),
          attachedFiles: files,
          anonymous: Boolean(formData.values.anonymous),
          account: globalProps.account
        });
        this.initializeForm();
      }
      if (action.nodeId === 'creat') {
        this.props.createIdea({
          text: formData.values.text,
          title: formData.values.title,
          keywords: Object.values(formData.values.keywords),
          attachedFiles: files,
          anonymous: Boolean(formData.values.anonymous),
          account: globalProps.account
        });
        this.initializeForm();
      }
    }
  };

  initializeForm = () => {
    const { form } = this.props;
    this.props.dispatch(
      initialize(form, {
        title: '',
        keywords: {},
        text: '',
        anonymous: false,
        files: []
      })
    );
    this.setState({ opened: false });
  };

  render() {
    const { formData, globalProps: { siteConf, account }, classes } = this.props;
    const { opened } = this.state;
    const authorPicture = account.picture;
    const keywords = {};
    siteConf.keywords.forEach((keyword) => {
      keywords[keyword] = keyword;
    });
    const withAnonymous = siteConf.anonymisation;
    let hasText = false;
    let files = [];
    let selectedKeywords = {};
    let anonymousSelected = false;
    let canSubmit = false;
    if (formData && formData.values) {
      hasText = formData.values.text;
      files = formData.values.files ? formData.values.files : [];
      files = files.filter((file) => {
        return file;
      });
      selectedKeywords = formData.values.keywords ? formData.values.keywords : {};
      anonymousSelected = withAnonymous && Boolean(formData.values.anonymous);
      canSubmit = formData.values.title && Object.keys(selectedKeywords).length > 0 && hasText;
    }
    return (
      <div
        ref={(container) => {
          this.container = container;
        }}
        className={classes.fromContainer}
      >
        <div className={classes.left}>
          {anonymousSelected
            ? <Avatar classes={{ root: classes.avatar }} className={classes.anonymousAvatar}>
              <Icon className={'mdi-set mdi-guy-fawkes-mask'} />
            </Avatar>
            : <Avatar classes={{ root: classes.avatar }} ize={30} src={authorPicture ? `${authorPicture.url}/profil` : ''} />}
        </div>
        <div className={classes.form}>
          {opened &&
            <Field
              props={{
                placeholder: I18n.t('forms.createIdea.titleHelper')
              }}
              name="title"
              component={renderTextInput}
            />}
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
                  [classes.placeholderActive]: !hasText
                })}
                aria-hidden="true"
                role="presentation"
                tabIndex="-1"
              >
                {opened ? I18n.t('forms.createIdea.textPlaceholderOpened') : I18n.t('forms.createIdea.textPlaceholder')}
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

          {opened && [
            <div className={classes.addonContainer}>
              <Field
                props={{
                  label: (
                    <label className={classes.label} htmlFor="keywords">
                      <IconButton className={classes.button}>
                        <Icon className={'mdi-set mdi-tag-multiple'} />
                      </IconButton>
                      {I18n.t('forms.createIdea.keywords')}
                    </label>
                  ),
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
              <div className={classes.addon}>
                <Field
                  props={{
                    node: (
                      <Tooltip title={I18n.t('forms.attachFiles')} placement="bottom">
                        <IconButton className={classes.button}>
                          <AttachFileIcon />
                        </IconButton>
                      </Tooltip>
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
                      classes: classes
                    }}
                    name="anonymous"
                    component={renderAnonymousCheckboxField}
                    type="boolean"
                  />
                  : null}
              </div>
            </div>,
            <div className={classes.action}>
              <SendIcon
                onClick={canSubmit ? this.handleSubmit : undefined}
                size={22}
                className={classNames(classes.submit, {
                  [classes.submitActive]: canSubmit
                })}
              />
            </div>
          ]}
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
        const { formData, globalProps: { siteConf } } = ownProps;
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
                state: siteConf.supportIdeas ? ['submitted_support', 'published'] : ['published'],
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