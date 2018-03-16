/* eslint-disable react/no-array-index-key, no-confusing-arrow */
import React from 'react';
import { Field, reduxForm } from 'redux-form';
import { Translate, I18n } from 'react-redux-i18n';
import classNames from 'classnames';
import { connect } from 'react-redux';
import { graphql } from 'react-apollo';
import { withStyles } from 'material-ui/styles';
import InsertDriveFileIcon from 'material-ui-icons/InsertDriveFile';
import { find as findUrls } from 'linkifyjs';

import { formatText } from '../../../../utils/textFormatter';
import Button, { CancelButton } from '../../../styledComponents/Button';
import { renderTextBoxField, renderFilesListField } from '../../utils';
import FilesPickerPreview from '../../widgets/FilesPickerPreview';
import CommentMenu from '../common/CommentMenu';
import { renderMenuItem } from '../../../common/menu/MenuList';
import { edit } from '../../../../graphql/processes/commentProcess';
import { editMutation } from '../../../../graphql/processes/commentProcess/edit';

const styles = {
  container: {
    paddingTop: 5,
    paddingBottom: 5
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
    backgroundColor: 'white',
    '&:focus-within': {
      border: '2px solid #848484'
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
    left: 10,
    paddingRight: 40
  },
  actions: {
    display: 'flex',
    paddingTop: 5
  },
  button: {
    marginRight: '5px !important'
  }
};

export class DumbEditCommentForm extends React.Component {
  constructor(props, context) {
    super(props, context);
    this.filesPicker = null;
    this.editor = null;
  }

  handleSubmit = () => {
    const { formData, valid, context, onSubmit } = this.props;
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
      const plainComment = this.editor.getPlainText();
      const formattedComment = formatText(plainComment);
      this.props.editComment({
        context: context,
        text: plainComment,
        formattedText: formattedComment,
        urls: findUrls(plainComment)
          .filter((link) => {
            return link.type === 'url';
          })
          .map((link) => {
            return link.href;
          }),
        attachedFiles: newFiles,
        oldFiles: oldFiles
      });
      if (onSubmit) onSubmit();
    }
  };

  render() {
    const { action, formData, placeholder, onSubmit, classes, theme } = this.props;
    const hasComment = formData && formData.values && formData.values.comment;
    let files = formData && formData.values && formData.values.files ? formData.values.files : [];
    files = files.filter((file) => {
      return file;
    });
    const canSubmit = files.length > 0 || hasComment;
    return (
      <div className={classes.container}>
        <FilesPickerPreview
          files={files}
          getPicker={() => {
            return this.filesPicker;
          }}
        />
        <div className={classes.inputContainer}>
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
          <div className={classNames('inline-editor', classes.textField)}>
            <Field
              props={{
                onCtrlEnter: this.handleSubmit,
                initRef: (editor) => {
                  this.editor = editor;
                }
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
              {placeholder || <Translate value="forms.comment.textPlaceholder" name={'...'} />}
            </div>
          </div>
        </div>
        <div className={classes.actions}>
          <CancelButton onClick={onSubmit} className={classes.button}>
            {I18n.t('forms.cancel')}
          </CancelButton>
          <Button onClick={canSubmit ? this.handleSubmit : undefined} background={theme.palette.success[500]}>
            {I18n.t(action.submission)}
          </Button>
        </div>
      </div>
    );
  }
}

// Decorate the form component
const EditCommentReduxForm = reduxForm({ destroyOnUnmount: false })(DumbEditCommentForm);

const mapStateToProps = (state, props) => {
  return {
    formData: state.form[props.form]
  };
};

const EditCommentForm = graphql(editMutation, {
  props: function (props) {
    return {
      editComment: edit(props)
    };
  }
})(EditCommentReduxForm);

export default withStyles(styles, { withTheme: true })(connect(mapStateToProps)(EditCommentForm));