/* eslint-disable react/no-array-index-key, no-confusing-arrow */
import React from 'react';
import { Field, reduxForm, initialize } from 'redux-form';
import { connect } from 'react-redux';
import { graphql } from 'react-apollo';
import { I18n } from 'react-redux-i18n';
import classNames from 'classnames';
import SendIcon from 'material-ui-icons/Send';
import { withStyles } from 'material-ui/styles';
import AttachFileIcon from 'material-ui-icons/AttachFile';
import IconButton from 'material-ui/IconButton';
import Icon from 'material-ui/Icon';
import Tooltip from 'material-ui/Tooltip';

import FilesPickerPreview from '../../widgets/FilesPickerPreview';
import SelectChipPreview from '../../widgets/SelectChipPreview';
import {
  renderTextInput,
  renderTextBoxField,
  renderAnonymousCheckboxField,
  renderFilesListField,
  renderSelect
} from '../../utils';
import UserAvatar from '../../../user/UserAvatar';
import { PROCESSES } from '../../../../processes';
import { filterActions } from '../../../../utils/processes';
import { create, createAndPublish } from '../../../../graphql/processes/ideaProcess';
import { createMutation } from '../../../../graphql/processes/ideaProcess/create';
import { createAndPublishMutation } from '../../../../graphql/processes/ideaProcess/createAndPublish';

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
    button: {
      height: 40,
      width: 40,
      color: '#808080'
    },
    avatar: {
      borderRadius: 4,
      marginTop: 1
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
    this.editor = null;
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
    const processNodes = PROCESSES.ideamanagement.nodes;
    if (valid) {
      let files = formData.values.files || [];
      files = files.filter((file) => {
        return file;
      });
      const keywords = formData.values.keywords;
      const text = this.editor.getHTMLText();
      if (action.nodeId === processNodes.createAndPublish.nodeId) {
        this.props.createAndPublishIdea({
          text: text,
          title: formData.values.title,
          keywords: keywords ? Object.values(formData.values.keywords) : [],
          attachedFiles: files,
          anonymous: Boolean(formData.values.anonymous),
          account: globalProps.account
        });
        this.initializeForm();
      }
      if (action.nodeId === processNodes.create.nodeId) {
        this.props.createIdea({
          text: text,
          title: formData.values.title,
          keywords: keywords ? Object.values(formData.values.keywords) : [],
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
    this.editor.clear();
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
    const { formData, globalProps: { site, account, rootActions }, classes } = this.props;
    const ideamanagementProcess = PROCESSES.ideamanagement;
    const creationActions = filterActions(rootActions, {
      processId: ideamanagementProcess.id,
      nodeId: [ideamanagementProcess.nodes.create.nodeId, ideamanagementProcess.nodes.createAndPublish.nodeId]
    });
    const { opened } = this.state;
    const authorPicture = account && account.picture;
    const keywords = {};
    site.keywords.forEach((keyword) => {
      keywords[keyword] = keyword;
    });
    const withAnonymous = site.anonymisation;
    let hasText = false;
    let files = [];
    let selectedKeywords = {};
    let anonymousSelected = false;
    let canSubmit = false;
    if (formData && formData.values) {
      hasText = this.editor && this.editor.getHTMLText();
      files = formData.values.files ? formData.values.files : [];
      files = files.filter((file) => {
        return file;
      });
      const keywordsRequired = site.keywordsRequired;
      const keywordsSatisfied = !keywordsRequired || (keywordsRequired && Object.keys(selectedKeywords).length > 0);
      selectedKeywords = formData.values.keywords ? formData.values.keywords : {};
      anonymousSelected = withAnonymous && Boolean(formData.values.anonymous);
      canSubmit = formData.values.title && keywordsSatisfied && hasText;
    }
    return (
      <div
        ref={(container) => {
          this.container = container;
        }}
        className={classes.fromContainer}
      >
        <div className={classes.left}>
          <UserAvatar
            isAnonymous={anonymousSelected}
            picture={authorPicture}
            title={account && account.title}
            classes={{ avatar: classes.avatar }}
          />
        </div>
        <div className={classes.form}>
          {opened &&
            <Field
              props={{
                placeholder: I18n.t('forms.idea.titleHelper')
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
            <div className={classNames('inline-editor', classes.textField)}>
              <Field
                props={{
                  onCtrlEnter: this.handleSubmit,
                  initRef: (editor) => {
                    this.editor = editor;
                  },
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
                {opened ? I18n.t('forms.idea.textPlaceholderOpened') : I18n.t('forms.idea.textPlaceholder')}
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
                    label: (
                      <Tooltip title={I18n.t('forms.idea.keywords')} placement="top">
                        <IconButton className={classes.button}>
                          <Icon className={'mdi-set mdi-tag-multiple'} />
                        </IconButton>
                      </Tooltip>
                    ),
                    options: keywords,
                    canAdd: site.canAddKeywords,
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
                      <Tooltip title={I18n.t('forms.attachFiles')} placement="top">
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
              {creationActions.map((action, key) => {
                return (
                  <IconButton
                    key={key}
                    onClick={
                      canSubmit
                        ? () => {
                          this.handleSubmit(action);
                        }
                        : undefined
                    }
                    className={classes.action}
                  >
                    <SendIcon
                      size={22}
                      className={classNames(classes.submit, {
                        [classes.submitActive]: canSubmit
                      })}
                    />
                  </IconButton>
                );
              })}
            </div>}
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

const CreateIdeaForm = graphql(createAndPublishMutation, {
  props: function (props) {
    return {
      createAndPublishIdea: createAndPublish(props)
    };
  }
})(
  graphql(createMutation, {
    props: function (props) {
      return {
        createIdea: create(props)
      };
    }
  })(CreateIdeaReduxForm)
);

export default withStyles(styles, { withTheme: true })(connect(mapStateToProps)(CreateIdeaForm));