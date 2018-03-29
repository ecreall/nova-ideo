/* eslint-disable react/no-array-index-key, no-confusing-arrow */
import React from 'react';
import { Field, reduxForm, initialize } from 'redux-form';
import { Translate, I18n } from 'react-redux-i18n';
import classNames from 'classnames';
import { connect } from 'react-redux';
import { graphql } from 'react-apollo';
import SendIcon from 'material-ui-icons/Send';
import { withStyles } from 'material-ui/styles';
import InsertDriveFileIcon from 'material-ui-icons/InsertDriveFile';
import IconButton from 'material-ui/IconButton';
import { find as findUrls } from 'linkifyjs';

import { formatText } from '../../../../utils/textFormatter';
import { renderTextBoxField, renderAnonymousCheckboxField, renderFilesListField } from '../../utils';
import FilesPickerPreview from '../../widgets/FilesPickerPreview';
import CommentMenu from './CommentMenu';
import { renderMenuItem } from '../../../common/menu/MenuList';
import { comment } from '../../../../graphql/processes/common';
import { commentMutation } from '../../../../graphql/processes/common/comment';

const styles = (theme) => {
  return {
    container: {
      backgroundColor: 'white',
      paddingLeft: 20,
      paddingRight: 20,
      borderRadius: 6
    },
    containerAddon: {
      boxShadow: '0 -1px 0 rgba(0,0,0,.1)'
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
      backgroundColor: 'white',
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
    this.editor = null;
  }

  handleSubmit = () => {
    const { globalProps, formData, valid, context, action, onSubmit } = this.props;
    if (valid) {
      let files = formData.values.files || [];
      files = files.filter((file) => {
        return file;
      });
      const plainComment = this.editor.getPlainText();
      const formattedComment = formatText(plainComment);
      this.props
        .commentObject({
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
          attachedFiles: files,
          anonymous: Boolean(formData.values.anonymous),
          account: globalProps.account,
          action: `${action.processId}.${action.nodeId}`
        })
        .then(() => {
          if (onSubmit) onSubmit();
        });
      this.initializeForm();
    }
  };

  initializeForm = () => {
    const { formData, form } = this.props;
    const anonymous = formData && formData.values && Boolean(formData.values.anonymous);
    this.editor.clear();
    this.props.dispatch(
      initialize(form, {
        comment: '',
        anonymous: anonymous,
        files: []
      })
    );
  };

  render() {
    const { formData, channel, isDiscuss, title, globalProps: { site }, autoFocus, placeholder, classes, theme } = this.props;
    const hasComment = this.editor && this.editor.getPlainText();
    let files = formData && formData.values && formData.values.files ? formData.values.files : [];
    files = files.filter((file) => {
      return file;
    });
    const isDiscussChannel = channel ? channel.isDiscuss : isDiscuss;
    const withAnonymous = site.anonymisation && !isDiscussChannel;
    const anonymousSelected = withAnonymous && formData && formData.values && Boolean(formData.values.anonymous);
    const channelTitle = channel ? channel.title : title;
    const canSubmit = files.length > 0 || hasComment;
    return (
      <div className={classNames(classes.container, { [classes.containerAddon]: files.length > 0 })}>
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
          <div className={classNames('inline-editor', classes.textField)}>
            <Field
              props={{
                onCtrlEnter: this.handleSubmit,
                autoFocus: autoFocus,
                initRef: (editor) => {
                  this.editor = editor;
                }
              }}
              withRef
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
              {placeholder || <Translate value="forms.comment.textPlaceholder" name={channelTitle || '...'} />}
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
          <IconButton onClick={canSubmit ? this.handleSubmit : undefined} className={classes.action}>
            <SendIcon
              size={22}
              className={classNames(classes.submit, {
                [classes.submitActive]: canSubmit
              })}
            />
          </IconButton>
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

const CommentForm = graphql(commentMutation, {
  props: function (props) {
    return {
      commentObject: comment(props)
    };
  }
})(CommentReduxForm);

export default withStyles(styles, { withTheme: true })(connect(mapStateToProps)(CommentForm));