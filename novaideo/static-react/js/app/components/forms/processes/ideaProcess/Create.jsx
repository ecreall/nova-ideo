/* eslint-disable react/no-array-index-key, no-confusing-arrow */
import React from 'react';
import { Field, reduxForm, initialize } from 'redux-form';
import { connect } from 'react-redux';
import { graphql } from 'react-apollo';
import { I18n } from 'react-redux-i18n';
import classNames from 'classnames';
import { withStyles } from 'material-ui/styles';
import AttachFileIcon from 'material-ui-icons/AttachFile';
import IconButton from 'material-ui/IconButton';
import Icon from 'material-ui/Icon';
import Tooltip from 'material-ui/Tooltip';
import Moment from 'moment';

import FilesPickerPreview from '../../widgets/FilesPickerPreview';
import SelectChipPreview from '../../widgets/SelectChipPreview';
import {
  renderTextInput,
  renderRichTextField,
  renderAnonymousCheckboxField,
  renderFilesListField,
  renderSelect
} from '../../utils';
import UserAvatar from '../../../user/UserAvatar';
import { PROCESSES } from '../../../../processes';
import { filterActions } from '../../../../utils/processes';
import { getFormattedDate } from '../../../../utils/globalFunctions';
import { create, createAndPublish } from '../../../../graphql/processes/ideaProcess';
import { createMutation } from '../../../../graphql/processes/ideaProcess/create';
import { createAndPublishMutation } from '../../../../graphql/processes/ideaProcess/createAndPublish';
import Button, { CancelButton } from '../../../styledComponents/Button';
import Form from '../../Form';

const styles = (theme) => {
  return {
    fromContainer: {
      padding: '15px 11px',
      backgroundColor: 'whitesmoke',
      border: 'solid 1px rgba(0,0,0,.1)',
      borderBottom: 'none',
      display: 'flex'
    },
    inputContainer: {
      display: 'flex',
      justifyContent: 'center',
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
      flexDirection: 'column',
      marginLeft: 15,
      paddingLeft: 10
    },
    placeholder: {
      color: '#000',
      opacity: '.375',
      textOverflow: 'ellipsis',
      overflow: 'hidden',
      whiteSpace: 'nowrap',
      fontStyle: 'normal',
      pointerEvents: 'none',
      maxHeight: '100%'
    },
    textContainer: {
      marginTop: 20
    },
    addon: {
      display: 'flex',
      flexDirection: 'row',
      alignItems: 'center'
    },
    addonContainer: {
      display: 'flex',
      flexDirection: 'row',
      justifyContent: 'space-between'
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
      marginTop: 20
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
    },
    buttonFooter: {
      marginLeft: '5px !important'
    },
    titleRoot: {
      boxShadow: 'none',
      border: 'none',
      backgroundColor: 'transparent'
    },
    titleInput: {
      color: '#2c2d30',
      fontSize: 42,
      fontWeight: 900,
      paddingTop: 3,
      lineHeight: 'normal',
      '&::placeholder': {
        fontSize: 40
      },
      '&::-webkit-input-placeholder': {
        fontSize: 40
      },
      '&::-moz-placeholder': {
        fontSize: 40
      },
      '&::-ms-input-placeholder': {
        fontSize: 40
      }
    },
    formTitle: {
      flexGrow: 1
    },
    header: {
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'flex-start',
      margin: '0 10px',
      position: 'relative'
    },
    headerTitle: {
      fontSize: 15,
      color: '#2c2d30',
      fontWeight: 900,
      lineHeight: 'normal'
    },
    titleContainer: {
      display: 'flex'
    },
    headerAddOn: {
      color: '#999999ff',
      fontSize: 12,
      lineHeight: 'normal',
      fontWeight: 'initial'
    },
    title: {
      display: 'flex',
      fontSize: 15,
      color: '#2c2d30',
      fontWeight: '900',
      cursor: 'pointer',
      '&:hover': {
        textDecoration: 'underline'
      }
    },
    filesPreviewContainer: {
      padding: 0
    },
    filesPreviewImage: {
      height: 35
    },
    filesPreviewFileIcon: {
      fontSize: '31px !important'
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

export class DumbCreateIdeaForm extends React.Component {
  constructor(props) {
    super(props);
    this.filesPicker = null;
    this.keywordsPicker = null;
    this.form = null;
    this.editor = null;
  }

  closeForm = () => {
    const { onClose } = this.props;
    this.form.close();
    if (onClose) onClose();
  };

  openForm = () => {
    this.form.open();
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
      const htmlText = this.editor.getHTMLText();
      if (action.nodeId === processNodes.createAndPublish.nodeId) {
        this.props.createAndPublishIdea({
          text: htmlText,
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
          text: htmlText,
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
    this.props.dispatch(
      initialize(form, {
        title: '',
        keywords: {},
        text: '',
        anonymous: false,
        files: []
      })
    );
    this.form.close();
  };

  closeForm = () => {
    this.form.close();
  };

  render() {
    const { formData, globalProps: { site, account, rootActions }, classes, theme } = this.props;
    const ideamanagementProcess = PROCESSES.ideamanagement;
    const creationActions = filterActions(rootActions, {
      processId: ideamanagementProcess.id,
      nodeId: [ideamanagementProcess.nodes.create.nodeId, ideamanagementProcess.nodes.createAndPublish.nodeId]
    });
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
    const date = getFormattedDate(Moment(), 'date.format3');
    const authorTitle = account && (anonymousSelected ? account.mask.title : account.title);
    return [
      <div className={classes.fromContainer}>
        <div className={classes.left}>
          <UserAvatar
            isAnonymous={anonymousSelected}
            picture={authorPicture}
            title={account && account.title}
            classes={{ avatar: classes.avatar }}
          />
        </div>
        <div className={classes.inputContainer} onClick={this.openForm}>
          <div className={classes.placeholder}>
            {I18n.t('forms.idea.textPlaceholder')}
          </div>
        </div>
      </div>,
      <Form
        initRef={(form) => {
          this.form = form;
        }}
        fullScreen
        onClose={this.closeForm}
        appBar={[
          <div className={classes.titleContainer}>
            <UserAvatar
              isAnonymous={anonymousSelected}
              picture={authorPicture}
              title={authorTitle}
              classes={{ avatar: classes.avatar }}
            />
            <div className={classes.header}>
              <span className={classes.title}>
                {authorTitle}
              </span>
              <span className={classes.headerAddOn}>
                {date}
              </span>
            </div>
          </div>,

          <div className={classes.formTitle}>Add a proposal</div>,

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
        ]}
        footer={[
          <FilesPickerPreview
            classes={{
              container: classes.filesPreviewContainer,
              image: classes.filesPreviewImage,
              fileIcon: classes.filesPreviewFileIcon
            }}
            files={files}
            getPicker={() => {
              return this.filesPicker;
            }}
          />,
          <CancelButton onClick={this.closeForm}>
            {I18n.t('forms.cancel')}
          </CancelButton>,
          creationActions.map((action, key) => {
            return (
              <Button
                key={key}
                onClick={
                  canSubmit
                    ? () => {
                      this.handleSubmit(action);
                    }
                    : undefined
                }
                background={theme.palette.success[500]}
                className={classes.buttonFooter}
              >
                {I18n.t(action.submission)}
              </Button>
            );
          })
        ]}
      >
        <div className={classes.form}>
          <Field
            props={{
              placeholder: I18n.t('forms.idea.titleHelper'),
              classes: {
                root: classes.titleRoot,
                input: classes.titleInput
              }
            }}
            name="title"
            component={renderTextInput}
            onChange={() => {}}
          />
          <SelectChipPreview
            items={selectedKeywords}
            onItemDelete={(id) => {
              this.keywordsPicker.toggleOption(false, id);
            }}
          />
          <div className={classes.textContainer}>
            <Field
              props={{
                initRef: (editor) => {
                  this.editor = editor;
                },
                placeholder: I18n.t('forms.idea.textPlaceholderOpened')
              }}
              name="text"
              component={renderRichTextField}
              type="text"
              withRef
              onChange={() => {}}
            />
          </div>
        </div>
      </Form>
    ];
  }
}

// Decorate the form component
const CreateIdeaReduxForm = reduxForm({ destroyOnUnmount: false })(DumbCreateIdeaForm);

const mapStateToProps = (state, props) => {
  return {
    formData: state.form[props.form],
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