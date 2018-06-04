/* eslint-disable react/no-array-index-key, no-confusing-arrow */
import React from 'react';
import { Field, reduxForm, initialize } from 'redux-form';
import { connect } from 'react-redux';
import { graphql } from 'react-apollo';
import { I18n } from 'react-redux-i18n';
import classNames from 'classnames';
import { withStyles } from '@material-ui/core/styles';
import AttachFileIcon from '@material-ui/icons/AttachFile';
import IconButton from '@material-ui/core/IconButton';
import Icon from '@material-ui/core/Icon';
import Tooltip from '@material-ui/core/Tooltip';
import Zoom from '@material-ui/core/Zoom';
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
import { filterActions, getEntityIcon } from '../../../../utils/processes';
import { getFormattedDate } from '../../../../utils/globalFunctions';
import { create, createAndPublish } from '../../../../graphql/processes/ideaProcess';
import Create from '../../../../graphql/processes/ideaProcess/mutations/Create.graphql';
import CreateAndPublish from '../../../../graphql/processes/ideaProcess/mutations/CreateAndPublish.graphql';
import Button, { CancelButton } from '../../../styledComponents/Button';
import Form from '../../Form';

const styles = (theme) => {
  return {
    textContainer: {
      marginTop: 20
    },
    addon: {
      display: 'flex',
      flexDirection: 'row',
      alignItems: 'center',
      marginRight: 15
    },
    button: {
      height: 40,
      width: 40,
      color: theme.palette.primary[500]
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
      fontSize: 30,
      fontWeight: 900,
      paddingTop: 3,
      paddingLeft: 0,
      lineHeight: 'normal',
      '&::placeholder': {
        fontSize: 30,
        fontWeight: 900
      },
      '&::-webkit-input-placeholder': {
        fontSize: 30,
        fontWeight: 900
      },
      '&::-moz-placeholder': {
        fontSize: 30,
        fontWeight: 900
      },
      '&::-ms-input-placeholder': {
        fontSize: 30,
        fontWeight: 900
      }
    },
    formTitle: {
      flexGrow: 1
    },
    header: {
      display: 'flex',
      flexDirection: 'column',
      margin: '0 10px',
      position: 'relative'
    },
    headerTitle: {
      fontSize: 15,
      color: '#2c2d30',
      fontWeight: 900,
      display: 'flex',
      lineHeight: 'normal'
    },
    titleContainer: {
      display: 'flex'
    },
    headerAddOn: {
      color: '#999999ff',
      fontSize: 12,
      lineHeight: 'normal'
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
      color: theme.palette.primary[500]
    },
    maskChecked: {
      color: theme.palette.warning[700]
    },
    titleInputContainer: {
      fontSize: 34,
      color: '#2c2d30',
      fontWeight: 900,
      paddingTop: 3,
      lineHeight: 'normal',
      display: 'flex',
      alignItems: 'baseline'
    },
    closeBtn: {
      '&::after': {
        display: 'block',
        position: 'absolute',
        top: '50%',
        right: 'auto',
        bottom: 'auto',
        left: -4,
        height: 20,
        transform: 'translateY(-50%)',
        borderRadius: 0,
        borderRight: '1px solid #e5e5e5',
        content: '""',
        color: '#2c2d30'
      }
    },
    icon: {
      fontSize: 34
    },
    iconDesabled: {
      color: '#989898'
    }
  };
};

export class DumbCreateIdeaForm extends React.Component {
  filesPicker = null;

  keywordsPicker = null;

  form = null;

  editor = null;

  closeForm = () => {
    this.form.close();
  };

  handleSubmit = (action) => {
    const { context, formData, valid, globalProps } = this.props;
    // context if transformation (transform a comment in to idea)
    const processNodes = PROCESSES.ideamanagement.nodes;
    if (valid) {
      const files = formData.values.files || [];
      const newFiles = files.filter((file) => {
        return file && !file.oid;
      });

      const oldFiles = files
        .filter((file) => {
          return file && file.oid;
        })
        .map((file) => {
          return file.oid;
        });

      const keywords = formData.values.keywords;
      const htmlText = this.editor.getHTMLText();
      const plainText = this.editor.getPlainText();
      if (action.nodeId === processNodes.createAndPublish.nodeId) {
        this.props.createAndPublishIdea({
          context: context,
          text: htmlText,
          plainText: plainText,
          title: formData.values.title,
          keywords: keywords ? Object.values(formData.values.keywords) : [],
          attachedFiles: newFiles,
          oldFiles: oldFiles,
          anonymous: Boolean(formData.values.anonymous),
          account: globalProps.account
        });
        this.initializeForm();
      }
      if (action.nodeId === processNodes.create.nodeId) {
        this.props.createIdea({
          context: context,
          text: htmlText,
          plainText: plainText,
          title: formData.values.title,
          keywords: keywords ? Object.values(formData.values.keywords) : [],
          attachedFiles: newFiles,
          oldFiles: oldFiles,
          anonymous: Boolean(formData.values.anonymous),
          account: globalProps.account
        });
        this.initializeForm();
      }
    }
  };

  initializeForm = () => {
    const { form, context } = this.props;
    this.props.dispatch(
      initialize(
        form,
        !context
          ? {
            title: '',
            keywords: {},
            text: '',
            anonymous: false,
            files: []
          }
          : undefined
      )
    );
    this.closeForm();
  };

  render() {
    const {
      formData,
      globalProps: { site, account, rootActions },
      onClose,
      classes,
      theme
    } = this.props;
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
    let hasTitle = false;
    if (formData && formData.values) {
      hasText = this.editor && !this.editor.isEmpty();
      files = formData.values.files ? formData.values.files : [];
      files = files.filter((file) => {
        return file;
      });
      const keywordsRequired = site.keywordsRequired;
      const keywordsSatisfied = !keywordsRequired || (keywordsRequired && Object.keys(selectedKeywords).length > 0);
      selectedKeywords = formData.values.keywords ? formData.values.keywords : {};
      anonymousSelected = withAnonymous && Boolean(formData.values.anonymous);
      hasTitle = formData.values.title;
      canSubmit = hasTitle && keywordsSatisfied && hasText;
    }
    const date = getFormattedDate(Moment(), 'date.format3');
    const authorTitle = account && (anonymousSelected ? account.mask.title : account.title);
    const IdeaIcon = getEntityIcon('Idea');
    return (
      <Form
        initRef={(form) => {
          this.form = form;
        }}
        open
        withDrawer
        fullScreen
        transition={Zoom}
        onClose={onClose}
        classes={{
          closeBtn: classes.closeBtn
        }}
        appBar={[
          <div className={classes.titleContainer}>
            <UserAvatar
              isAnonymous={anonymousSelected}
              picture={authorPicture}
              title={authorTitle}
              classes={{ avatar: classes.avatar }}
            />
            <div className={classes.header}>
              <span className={classes.headerTitle}>{authorTitle}</span>
              <span className={classes.headerAddOn}>{date}</span>
            </div>
          </div>,

          <div className={classes.formTitle}>{I18n.t('forms.idea.addProposal')}</div>,

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
            {withAnonymous ? (
              <Field
                props={{
                  classes: classes
                }}
                name="anonymous"
                component={renderAnonymousCheckboxField}
                type="boolean"
              />
            ) : null}
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
          <CancelButton onClick={this.closeForm}>{I18n.t('forms.cancel')}</CancelButton>,
          creationActions.map((action, key) => {
            return (
              <Button
                key={key}
                disabled={!canSubmit}
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
          <div className={classes.titleInputContainer}>
            <IdeaIcon className={classNames(classes.icon, { [classes.iconDesabled]: !hasTitle })} />
            <Field
              props={{
                placeholder: I18n.t('forms.idea.titleHelper'),
                autoFocus: true,
                classes: {
                  root: classes.titleRoot,
                  input: classes.titleInput
                }
              }}
              name="title"
              component={renderTextInput}
              onChange={() => {}}
            />
          </div>
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
    );
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

const CreateIdeaForm = graphql(CreateAndPublish, {
  props: function (props) {
    return {
      createAndPublishIdea: createAndPublish(props)
    };
  }
})(
  graphql(Create, {
    props: function (props) {
      return {
        createIdea: create(props)
      };
    }
  })(CreateIdeaReduxForm)
);

export default withStyles(styles, { withTheme: true })(connect(mapStateToProps)(CreateIdeaForm));