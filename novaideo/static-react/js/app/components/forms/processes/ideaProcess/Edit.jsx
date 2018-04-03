/* eslint-disable react/no-array-index-key, no-confusing-arrow */
import React from 'react';
import { Field, reduxForm, initialize } from 'redux-form';
import { connect } from 'react-redux';
import { graphql } from 'react-apollo';
import { I18n } from 'react-redux-i18n';
import { withStyles } from 'material-ui/styles';
import AttachFileIcon from 'material-ui-icons/AttachFile';
import IconButton from 'material-ui/IconButton';
import Icon from 'material-ui/Icon';
import Tooltip from 'material-ui/Tooltip';
import Moment from 'moment';

import FilesPickerPreview from '../../widgets/FilesPickerPreview';
import SelectChipPreview from '../../widgets/SelectChipPreview';
import { renderTextInput, renderRichTextField, renderFilesListField, renderSelect } from '../../utils';
import UserAvatar from '../../../user/UserAvatar';
import { PROCESSES } from '../../../../processes';
import { getFormattedDate } from '../../../../utils/globalFunctions';
import { getEntityIcon } from '../../../../utils/processes';
import { edit } from '../../../../graphql/processes/ideaProcess';
import { editMutation } from '../../../../graphql/processes/ideaProcess/edit';
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
      lineHeight: 'normal'
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
      height: 40,
      width: 40,
      color: '#808080'
    },
    maskChecked: {
      color: theme.palette.warning[700]
    },
    titleInputContainer: {
      fontSize: 42,
      color: '#2c2d30',
      fontWeight: 900,
      paddingTop: 3,
      lineHeight: 'normal',
      display: 'flex',
      alignItems: 'baseline'
    }
  };
};

export class DumbEditIdeaForm extends React.Component {
  constructor(props) {
    super(props);
    this.filesPicker = null;
    this.keywordsPicker = null;
    this.form = null;
    this.editor = null;
  }

  handleSubmit = () => {
    const { formData, valid, idea, action } = this.props;
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
      if (action.nodeId === processNodes.edit.nodeId) {
        this.props.editIdea({
          context: idea,
          text: htmlText,
          title: formData.values.title,
          keywords: keywords ? Object.values(formData.values.keywords) : [],
          attachedFiles: newFiles,
          oldFiles: oldFiles
        });
        this.initializeForm();
      }
    }
  };

  initializeForm = () => {
    const { form } = this.props;
    this.closeForm();
    this.props.dispatch(
      initialize(form, {
        title: '',
        keywords: {},
        text: '',
        attachedFiles: []
      })
    );
  };

  closeForm = () => {
    this.form.close();
  };

  render() {
    const { idea, formData, isAnonymous, globalProps: { site, account }, action, onClose, classes, theme } = this.props;
    const authorPicture = account.picture;
    const keywords = {};
    site.keywords.forEach((keyword) => {
      keywords[keyword] = keyword;
    });
    let files = [];
    let selectedKeywords = {};
    if (formData && formData.values) {
      files = formData.values.files ? formData.values.files : [];
      files = files.filter((file) => {
        return file;
      });
      selectedKeywords = formData.values.keywords ? formData.values.keywords : {};
    }
    const date = getFormattedDate(Moment(), 'date.format3');
    const authorTitle = isAnonymous ? account.mask.title : account.title;
    const IdeaIcon = getEntityIcon(idea.__typename);
    return (
      <Form
        initRef={(form) => {
          this.form = form;
        }}
        transition={false}
        fullScreen
        open
        onClose={onClose}
        appBar={[
          <div className={classes.titleContainer}>
            <UserAvatar
              isAnonymous={isAnonymous}
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

          <div className={classes.formTitle}>
            {I18n.t(action.description)}
          </div>,

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
          <Button onClick={this.handleSubmit} background={theme.palette.success[500]} className={classes.buttonFooter}>
            {I18n.t(action.submission)}
          </Button>
        ]}
      >
        <div className={classes.form}>
          <div className={classes.titleInputContainer}>
            <IdeaIcon className={classes.icon} />
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
                }
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
const EditIdeaReduxForm = reduxForm()(DumbEditIdeaForm);

const mapStateToProps = (state, props) => {
  return {
    formData: state.form[props.form],
    globalProps: state.globalProps
  };
};

const EditIdeaForm = graphql(editMutation, {
  props: function (props) {
    return {
      editIdea: edit(props)
    };
  }
})(EditIdeaReduxForm);

export default withStyles(styles, { withTheme: true })(connect(mapStateToProps)(EditIdeaForm));